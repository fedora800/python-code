
/*
--------------------------------------------------------------------------------

-- TY01 - typ_asset_type
-- TY02 - typ_data_source
-- TY03 - typ_country_code

-- T01 - tbl_exchange
-- T02 - tbl_instrument
-- T03 - tbl_price_data_1day

I01 - idx_tbl_price_data_1day_symbol_time 
*/

--------------------------------------------------------------------------------

-- TY01 - typ_asset_type
\echo "Creating TYPE typ_asset_type"
CREATE TYPE typ_asset_type AS ENUM (
  'EQUITY_FUNDS',
  'ETF',
  'STOCK'
);

-- TY02 - typ_data_source
\echo "Creating TYPE typ_data_source"
CREATE TYPE typ_data_source AS ENUM (
  'YFINANCE',
  'THINKORSWIM',
  'TRADING212',
  'TEMPORARY'
);


-- TY03 - typ_country_code
\echo "Creating TYPE typ_country_code"
CREATE TYPE typ_country_code AS ENUM (
  'IN',
  'UK',
  'US'
);

--------------------------------------------------------------------------------

-- T01 - tbl_exchange
\echo "Creating TABLE tbl_exchange"
CREATE TABLE IF NOT EXISTS tbl_exchange (
  exchange_code TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  note_1 TEXT
);

-- T02 - tbl_instrument
\echo "Creating TABLE tbl_insrument"
CREATE TABLE IF NOT EXISTS tbl_instrument (
  ins_id SERIAL PRIMARY KEY,
  symbol TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  exchange_code TEXT REFERENCES tbl_exchange(exchange_code),
  asset_type typ_asset_type,
  country_code typ_country_code,
  dtime_created  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  dtime_updated  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  sector TEXT,
  industry TEXT,
  sub_industry TEXT,
  data_source typ_data_source,
  deleted BOOLEAN DEFAULT false,
  note_1 TEXT
);

-- T03 - tbl_price_data_1day
\echo "Creating TABLE tbl_price_data_1day";
CREATE TABLE IF NOT EXISTS tbl_price_data_1day (
--   pd_ins_id INTEGER REFERENCES tbl_instrument (ins_id),
   pd_symbol      TEXT REFERENCES tbl_instrument (symbol),
   pd_time        TIMESTAMPTZ NOT NULL,
   open           NUMERIC(10,2) NOT NULL,
   high           NUMERIC(10,2) NOT NULL,
   low            NUMERIC(10,2) NOT NULL,
   close          NUMERIC(10,2) NOT NULL,
   volume         INTEGER  NOT NULL,
   ema_5          NUMERIC(10,2) NULL,
   ema_13         NUMERIC(10,2) NULL,
   sma_50         NUMERIC(10,2) NULL,
   sma_200        NUMERIC(10,2) NULL,
   rsi_14         NUMERIC(10,2) NULL,
   macd_sig_hist  TEXT NULL,
   dm_dp_adx      TEXT NULL,
   crs_50         NUMERIC(3,3) NULL,
--  vendor_id INTEGER REFERENCES data_vendors(vendor_id),
--   PRIMARY KEY (pd_ins_id, vendor_id, dtime)
--   PRIMARY KEY (pd_ins_id, pd_time)
   PRIMARY KEY (pd_symbol, pd_time)
);

/* I01 - idx_tbl_price_data_1day_symbol_time -- so will be default criteria on SELECT */
CREATE INDEX idx_tbl_price_data_1day_symbol_time
  ON tbl_price_data_1day (pd_symbol ASC, pd_time ASC);

/* Convert the standard table into a hypertable partitioned on the time column using the create_hypertable() function provided by Timescale. */
\echo "Creating hypertable for  tbl_price_data_1day"
SELECT create_hypertable('tbl_price_data_1day', 'pd_time');


\echo creating table
select count(*) from tbl_instrument;

