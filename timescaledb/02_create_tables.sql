
/*
--------------------------------------------------------------------------------

-- TY01 - typ_asset_type
-- TY02 - typ_data_source
-- TY03 - typ_country_code

-- T01 - tbl_exchange
-- T02 - tbl_gics_sector
-- T03 - tbl_instrument
-- T04 - tbl_price_data_1day
-- T05 - tbl_symbol_filters

-- I01 - idx_tbl_price_data_1day_symbol_time 

*/

--------------------------------------------------------------------------------

-- TY01 - typ_asset_type
\echo "Dropping and Creating TYPE typ_asset_type"
DROP TYPE IF EXISTS typ_asset_type CASCADE;
CREATE TYPE typ_asset_type AS ENUM (
  'EQUITY_FUNDS',
  'ETF',
  'STOCK'
);

-- TY02 - typ_data_source
\echo "Dropping and Creating TYPE typ_data_source"
DROP TYPE IF EXISTS typ_data_source CASCADE;
CREATE TYPE typ_data_source AS ENUM (
  'INVESTING-COM',
  'MANUAL',
  'NSEINDIA-COM',
  'ONLINE_BLOG',
  'STOCKANALYSIS-COM',
  'TEMPORARY',
  'THINKORSWIM',
  'TRADING212',
  'YFINANCE'
);


-- TY03 - typ_country_code
\echo "Dropping and Creating TYPE typ_country_code"
DROP TYPE IF EXISTS typ_country_code CASCADE;
CREATE TYPE typ_country_code AS ENUM (
  'IN',
  'UK',
  'US'
);

--------------------------------------------------------------------------------

-- T01 - tbl_exchange
\echo "Dropping and Creating TABLE tbl_exchange"
DROP TABLE IF EXISTS tbl_exchange CASCADE;
CREATE TABLE IF NOT EXISTS tbl_exchange (
  exchange_code TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  country_code typ_country_code DEFAULT 'US' NOT NULL,
  note_1 TEXT DEFAULT NULL
);


-- T02 - tbl_gics_sector
-- https://en.wikipedia.org/wiki/Global_Industry_Classification_Standard
-- https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
\echo "Dropping and Creating TABLE tbl_gics_sector"
DROP TABLE IF EXISTS tbl_gics_sector CASCADE;
CREATE TABLE IF NOT EXISTS tbl_gics_sector (
  sector_code INTEGER NOT NULL,
  sector_name VARCHAR(255) NOT NULL,
  industry_group_code INTEGER NOT NULL,
  industry_group_name VARCHAR(255) NOT NULL,
  industry_code INTEGER NOT NULL,
  industry_name VARCHAR(255) NOT NULL,
  sub_industry_code INTEGER PRIMARY KEY,
  sub_industry_name VARCHAR(255) NOT NULL,
  UNIQUE (sector_code, industry_group_code, industry_code, sub_industry_code)
);

/*
Above UNIQUE is sufficient per chatgpt, so remove this after testing
ALTER TABLE your_table
ADD CONSTRAINT sector_hierarchy_unique 
UNIQUE (sector_code, industry_group_code, industry_code, sub_industry_code);
*/


-- T03 - tbl_instrument
\echo "Dropping and Creating TABLE tbl_insrument"
DROP TABLE IF EXISTS tbl_instrument CASCADE;
CREATE TABLE IF NOT EXISTS tbl_instrument (
  ins_id SERIAL PRIMARY KEY,
  symbol TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  exchange_code TEXT REFERENCES tbl_exchange(exchange_code),
  asset_type typ_asset_type,
  dividend_yield NUMERIC(5,2),
  country_code typ_country_code,
  dtime_created  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  dtime_updated  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  sector_code INTEGER,
  industry_group_code INTEGER,
  industry_code INTEGER,
  sub_industry_code INTEGER,
  data_source typ_data_source,
  deleted BOOLEAN DEFAULT false,
  note_1 TEXT,
  FOREIGN KEY (sector_code, industry_group_code, industry_code, sub_industry_code) 
    REFERENCES tbl_gics_sector(sector_code, industry_group_code, industry_code, sub_industry_code) 
);

-- T04 - tbl_price_data_1day
\echo "Dropping and Creating TABLE tbl_price_data_1day";
DROP TABLE IF EXISTS tbl_price_data_1day CASCADE;
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
   crs_50         NUMERIC(5,3) NULL,
--  vendor_id INTEGER REFERENCES data_vendors(vendor_id),
--   PRIMARY KEY (pd_ins_id, vendor_id, dtime)
--   PRIMARY KEY (pd_ins_id, pd_time)
   PRIMARY KEY (pd_symbol, pd_time)
);

-- T05 - tbl_symbol_filters
\echo "Dropping and Creating TABLE tbl_symbol_filters"
DROP TABLE IF EXISTS tbl_symbol_filters CASCADE;
CREATE TABLE IF NOT EXISTS tbl_symbol_filters (
  filter_id SERIAL PRIMARY KEY,
  filter_name TEXT UNIQUE NOT NULL,
  filter_query TEXT UNIQUE NOT NULL,
  filter_description TEXT NOT NULL,
  category TEXT,
  deleted BOOLEAN DEFAULT false
);

--------------------------------------------------------------------------------

-- I01 - idx_tbl_price_data_1day_symbol_time -- so will be default criteria on SELECT */
\echo "Dropping and Creating INDEX idx_tbl_price_data_1day_symbol_time"
DROP INDEX IF EXISTS idx_tbl_price_data_1day_symbol_time;
CREATE INDEX idx_tbl_price_data_1day_symbol_time
  ON tbl_price_data_1day (pd_symbol ASC, pd_time ASC);

--------------------------------------------------------------------------------

/* Convert the standard table into a hypertable partitioned on the time column using the create_hypertable() function provided by Timescale. */
\echo "Converting tbl_price_data_1day into a hypertable partitioned on pd_time"
SELECT create_hypertable('tbl_price_data_1day', 'pd_time');


\echo creating table
select count(*) from tbl_instrument;


