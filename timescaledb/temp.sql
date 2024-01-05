
--------------------------------------------------------------------------------

*** BARD ***

CREATE TABLE exchanges (
    exchange_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT,
    currency TEXT
);

CREATE TABLE securities (
    security_id SERIAL PRIMARY KEY,
    symbol TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    exchange_id INTEGER REFERENCES exchanges(exchange_id),
    type TEXT
);

CREATE TABLE data_vendors (
    vendor_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    website TEXT,
    description TEXT
);

CREATE TABLE daily_prices (
    date DATE NOT NULL PRIMARY KEY,
    security_id INTEGER REFERENCES securities(security_id),
    vendor_id INTEGER REFERENCES data_vendors(vendor_id),
    open_price NUMERIC,
    high_price NUMERIC,
    low_price NUMERIC,
    close_price NUMERIC,
    volume INTEGER
);

SELECT create_hypertable('daily_prices', 'date'); -- Create a hypertable for efficient time-series queries

CREATE TABLE intraday_prices (
    date DATE NOT NULL,
    security_id INTEGER REFERENCES securities(security_id),
    vendor_id INTEGER REFERENCES data_vendors(vendor_id),
    timestamp TIMESTAMPTZ NOT NULL,
    open_price NUMERIC,
    high_price NUMERIC,
    low_price NUMERIC,
    close_price NUMERIC,
    volume INTEGER,
    PRIMARY KEY (date, security_id, vendor_id, timestamp)
);

SELECT create_hypertable('intraday_prices', 'date', chunk_time_interval => interval '1 hour'); -- Create a hypertable with hourly chunks




CREATE VIEW latest_prices AS
SELECT security_id, symbol, name, exchange_id, MAX(timestamp) AS latest_timestamp, close_price
FROM intraday_prices
GROUP BY security_id, symbol, name, exchange_id;

CREATE VIEW security_performance AS
SELECT date, security_id, symbol, name,
       close_price - LAG(close_price, 1) OVER (PARTITION BY security_id ORDER BY date) AS daily_return
FROM daily_prices;

CREATE VIEW market_overview AS
SELECT date, AVG(close_price) AS average_price, SUM(volume) AS total_volume
FROM daily_prices
GROUP BY date;



CREATE INDEX idx_daily_prices_security_id ON daily_prices(security_id);
CREATE INDEX idx_daily_prices_vendor_id ON daily_prices(vendor_id);
CREATE INDEX idx_daily_prices_symbol ON daily_prices USING GIN(symbol gin_trgm_ops); -- For trigram-based text search

CREATE INDEX idx_intraday_prices_security_id ON intraday_prices(security_id);
CREATE INDEX idx_intraday_prices_vendor_id ON intraday_prices(vendor_id);
CREATE INDEX idx_intraday_prices_symbol ON intraday_prices USING GIN(symbol gin_trgm_ops);

CREATE INDEX idx_security_performance_date ON security_performance(date);


--------------------------------------------------------------------------------
*** CHATGPT ***

-- Create the stocks table
CREATE TABLE stocks (
    stock_id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    sector VARCHAR(50)
    -- Add other columns as needed
);

-- Create the exchanges table
CREATE TABLE exchanges (
    exchange_id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
    -- Add other columns as needed
);

-- Create the stock_prices table with hypertable
CREATE TABLE stock_prices (
    price_id SERIAL PRIMARY KEY,
    stock_id INT,
    exchange_id INT,
    price_date TIMESTAMPTZ NOT NULL,
    open_price DECIMAL(15, 2),
    close_price DECIMAL(15, 2),
    high_price DECIMAL(15, 2),
    low_price DECIMAL(15, 2),
    volume INT,
    FOREIGN KEY (stock_id) REFERENCES stocks(stock_id),
    FOREIGN KEY (exchange_id) REFERENCES exchanges(exchange_id)
    -- Add other columns as needed
);

-- Convert stock_prices table to hypertable based on time column
SELECT create_hypertable('stock_prices', 'price_date');

-- Add indexes on columns
CREATE INDEX idx_symbol ON stocks (symbol);
CREATE INDEX idx_price_date ON stock_prices (price_date);

-- Create the stock_summary view
CREATE VIEW stock_summary AS
SELECT
    s.symbol,
    s.company_name,
    sp.price_date,
    sp.close_price
FROM
    stocks s
JOIN
    stock_prices sp ON s.stock_id = sp.stock_id;


--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------



/* Creating a table */
CREATE TABLE candles_1m (
   time   TIMESTAMPTZ NOT NULL,
   open   DOUBLE PRECISION NOT NULL,
   high   DOUBLE PRECISION NOT NULL,
   low    DOUBLE PRECISION NOT NULL,
   close  DOUBLE PRECISION NOT NULL,
   volume DOUBLE PRECISION NOT NULL
);

SELECT create_hypertable('candles_1m', 'time', migrate_data => 'TRUE');

Now you can run the Timescale DB function and queries. So here for example the code that will create 5m bars from your 1-minute bars: 
SELECT time_bucket('5 minutes', time) AS new_time,
  first(open, time) as open,
  MAX(high)   as high,
  MIN(low)    as low, 
  last(close, time) as close, 
  sum(volume) as volume
FROM candles_1m
GROUP BY new_time



----


/* Creates the table which will store stock data */
CREATE TABLE public.stocks_intraday (
    "time" timestamp(0) NOT NULL,
    symbol varchar NULL,
    price_open float8 NULL,
    price_close float8 NULL,
    price_low float8 NULL,
    price_high float8 NULL,
    trading_volume int4 NULL,
);


/* Enable the TimscaleDB extension */
CREATE EXTENSION IF NOT EXISTS timescaledb;

/* 
Turn the 'stocks_intraday' table into a hypertable.
This is important to be able to make use of TimescaleDB features later on.
*/
SELECT create_hypertable('stocks_intraday', 'time');

CREATE TABLE stocks_real_time (
  symbol TEXT NOT NULL,
  price DOUBLE PRECISION NULL,
  day_volume INT NULL
);

Convert the standard table into a hypertable partitioned on the time column using the create_hypertable() function provided by Timescale. You must provide the name of the table and the column in that table that holds the timestamp data to use for partitioning:
SELECT create_hypertable('stocks_real_time', by_range('time'));

Create an index to support efficient queries on the symbol and time columns:
CREATE INDEX ix_symbol_time ON stocks_real_time (symbol, time DESC);


At the psql prompt, use the COPY command to transfer data into your Timescale instance. If the .csv files arent in your current directory, specify the file paths in these commands:
\COPY stocks_real_time from './tutorial_sample_tick.csv' DELIMITER ',' CSV HEADER;


At the psql prompt, create the continuous aggregate to aggregate data every minute:
CREATE MATERIALIZED VIEW one_day_candle
WITH (timescaledb.continuous) AS
    SELECT
        time_bucket('1 day', time) AS bucket,
        symbol,
        FIRST(price, time) AS "open",
        MAX(price) AS high,
        MIN(price) AS low,
        LAST(price, time) AS "close",
        LAST(day_volume, time) AS day_volume
    FROM crypto_ticks
    GROUP BY bucket, symbol;

Set a refresh policy to update the continuous aggregate every day, if there is new data available in the hypertable for the last two days:
SELECT add_continuous_aggregate_policy('one_day_candle',
    start_offset => INTERVAL '3 days',
    end_offset => INTERVAL '1 day',
    schedule_interval => INTERVAL '1 day');

SELECT * FROM one_day_candle
WHERE symbol = 'BTC/USD' AND bucket >= NOW() - INTERVAL '14 days'
ORDER BY bucket;

Querying the continuous aggregate
At the psql prompt, use this query to select all Bitcoin OHLCV data for the past 14 days, by time bucket:
SELECT * FROM one_day_candle
WHERE symbol = 'BTC/USD' AND bucket >= NOW() - INTERVAL '14 days'
ORDER BY bucket;

bucket         | symbol  |  open   |  high   |   low   |  close  | day_volume
------------------------+---------+---------+---------+---------+---------+------------
 2022-11-24 00:00:00+00 | BTC/USD |   16587 | 16781.2 | 16463.4 | 16597.4 |      21803
 2022-11-25 00:00:00+00 | BTC/USD | 16597.4 | 16610.1 | 16344.4 | 16503.1 |      20788
 2022-11-26 00:00:00+00 | BTC/USD | 16507.9 | 16685.5 | 16384.5 | 16450.6 |      12300


Enable compression on the table and pick suitable segment-by and order-by column using the ALTER TABLE command:
ALTER TABLE stocks_real_time 
SET (
    timescaledb.compress, 
    timescaledb.compress_segmentby='symbol', 
    timescaledb.compress_orderby='time DESC'
);

You can manually compress all the chunks of the hypertable using compress_chunk in this manner:
SELECT compress_chunk(c) from show_chunks('stocks_real_time') c;

Now that you have compressed the table you can compare the size of the dataset before and after compression:
SELECT 
    pg_size_pretty(before_compression_total_bytes) as before,
    pg_size_pretty(after_compression_total_bytes) as after
 FROM hypertable_compression_stats('stocks_real_time');

This shows a significant improvement in data usage:
before | after 
--------+-------
694 MB | 75 MB
(1 row)

Add a compression policy
To avoid running the compression step each time you have some data to compress you can set up a compression policy. The compression policy allows you to compress data that is older than a particular age, for example, to compress all chunks that are older than 8 days:
SELECT add_compression_policy('stocks_real_time', INTERVAL '8 days');


--------------------------------------------------------------------------------
## below code for simple moving average

-- Create a new table to store SMA values
CREATE TABLE IF NOT EXISTS tbl_price_data_1day_sma AS
SELECT
    pd_symbol,
    pd_time,
    close,
    AVG(close) OVER (PARTITION BY pd_symbol ORDER BY pd_time ROWS BETWEEN 49 PRECEDING AND CURRENT ROW) AS sma_50_days
FROM
    tbl_price_data_1day;


-- Add a new column for SMA values to the existing table
ALTER TABLE tbl_price_data_1day ADD COLUMN sma_50 DOUBLE PRECISION;

-- Update the existing table with SMA values
WITH sma_values AS (
    SELECT
        pd_symbol,
        pd_time,
        AVG(close) OVER (PARTITION BY pd_symbol ORDER BY pd_time ROWS BETWEEN 49 PRECEDING AND CURRENT ROW) AS sma_50
    FROM
        tbl_price_data_1day
)
UPDATE tbl_price_data_1day
SET sma_50 = sma_values.sma_50
FROM sma_values
WHERE tbl_price_data_1day.pd_symbol = sma_values.pd_symbol
  AND tbl_price_data_1day.pd_time = sma_values.pd_time;
--------------------------------------------------------------------------------

-- below is from chatgpt, gives us the update command to compute sma50 and update the rows
CREATE TABLE IF NOT EXISTS tbl_price_data_1day_sma (
    pd_symbol TEXT,
    pd_time TIMESTAMPTZ NOT NULL,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    volume INTEGER,
    sma_50_days DOUBLE PRECISION  -- 608: New column for SMA values
);

-- Use COPY command to insert data into the table
COPY tbl_price_data_1day_sma (pd_symbol, pd_time, open, high, low, close, volume)
FROM '/path/to/your/data.csv' DELIMITER ',' CSV HEADER;

-- Update the new column with the calculated SMA values
WITH sma_values AS (
    SELECT
        pd_symbol,
        pd_time,
        AVG(close) OVER (PARTITION BY pd_symbol ORDER BY pd_time ROWS BETWEEN 49 PRECEDING AND CURRENT ROW) AS sma_50_days
    FROM
        tbl_price_data_1day_sma
)
UPDATE tbl_price_data_1day_sma
SET sma_50_days = sma_values.sma_50_days
FROM sma_values
WHERE tbl_price_data_1day_sma.pd_symbol = sma_values.pd_symbol
  AND tbl_price_data_1day_sma.pd_time = sma_values.pd_time;

--------------------------------------------------------------------------------


-- below is from chatgpt, gives us the trigger that computes sma50 and updates that field on insert 
-- 609: Create the table with the inherent SMA column
CREATE TABLE IF NOT EXISTS tbl_price_data_1day_sma (
    pd_symbol TEXT,
    pd_time TIMESTAMPTZ NOT NULL,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    volume INTEGER,
    sma_50_days DOUBLE PRECISION  -- 609: New column for SMA values
);

-- Create a function to calculate SMA
CREATE OR REPLACE FUNCTION fnc_calculate_sma()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE tbl_price_data_1day
    SET sma_50 = (
        SELECT AVG(close)
        FROM tbl_price_data_1day_sma t
        WHERE t.pd_symbol = NEW.pd_symbol AND t.pd_time <= NEW.pd_time
        ORDER BY t.pd_time DESC
        LIMIT 50
    )
    WHERE pd_symbol = NEW.pd_symbol AND pd_time = NEW.pd_time;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a trigger to run the function on INSERT
CREATE TRIGGER IF NOT EXISTS trg_update_sma
AFTER INSERT ON tbl_price_data_1day
FOR EACH ROW
EXECUTE FUNCTION fnc_calculate_sma();

--------------------------------------------------------------------------------



--------------------------------------------------------------------------------
