
/*
--------------------------------------------------------------------------------
01 CREATE DATABASE db_invest

--------------------------------------------------------------------------------
*/


/* 01 CREATE DATABASE db_invest */
-- do this manually outside this script
-- CREATE DATABASE db_invest;


CREATE TABLE IF NOT EXISTS raw_trade_data (
   time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
   symbol text NOT NULL,
   price double PRECISION NOT NULL,
   quantity double PRECISION NOT NULL
);


SELECT create_hypertable('raw_trade_data','time');



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


At the psql prompt, use the COPY command to transfer data into your Timescale instance. If the .csv files aren't in your current directory, specify the file paths in these commands:
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



