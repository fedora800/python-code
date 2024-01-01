
/*
--------------------------------------------------------------------------------

/* x01 - typ_asset_type */
/* T00.5 - tbl_exchange */
T01 - tbl_instrument
T02 - tbl_price_data_1day

I01 - idx_instrument_time

--------------------------------------------------------------------------------
*/

/* x01 - typ_asset_type */
CREATE TYPE typ_asset_type AS ENUM (
  'STOCK', 
  'ETF'
);

/* T00.5 - tbl_exchange */
CREATE TABLE IF NOT EXISTS tbl_exchange (
  exchange_code TEXT PRIMARY KEY,
  name TEXT NOT NULL
);

/* T01 - tbl_instrument */
CREATE TABLE IF NOT EXISTS tbl_instrument (
  ins_id SERIAL PRIMARY KEY,
  symbol TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  industry TEXT,
  exchange_code TEXT REFERENCES tbl_exchange(exchange_code),
  asset_type typ_asset_type,
  dtime_created  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  dtime_updated  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  note_1 TEXT
);

/* T02 - tbl_price_data_1day */
CREATE TABLE IF NOT EXISTS tbl_price_data_1day (
--   pd_ins_id INTEGER REFERENCES tbl_instrument (ins_id),
   pd_symbol TEXT REFERENCES tbl_instrument (symbol),
   pd_time TIMESTAMPTZ NOT NULL,
   open   DOUBLE PRECISION NOT NULL,
   high   DOUBLE PRECISION NOT NULL,
   low    DOUBLE PRECISION NOT NULL,
   close  DOUBLE PRECISION NOT NULL,
   volume INTEGER  NOT NULL,
--  vendor_id INTEGER REFERENCES data_vendors(vendor_id),
--   PRIMARY KEY (pd_ins_id, vendor_id, dtime)
--   PRIMARY KEY (pd_ins_id, pd_time)
   PRIMARY KEY (pd_symbol, pd_time)
);

/* Convert the standard table into a hypertable partitioned on the time column using the create_hypertable() function provided by Timescale. */
SELECT create_hypertable('tbl_price_data_1day', 'pd_time');

/* I01 - idx_instrument_time -- might not be required as the table has this combination as the primary key */ 
-- CREATE INDEX idx_instrument_time ON tbl_price_data_1day (pd_symbol, pd_time DESC);

