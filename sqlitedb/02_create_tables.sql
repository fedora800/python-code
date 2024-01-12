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