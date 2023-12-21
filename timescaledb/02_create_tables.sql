
/*
--------------------------------------------------------------------------------

T01 - tbl_instrument
T02 - tbl_price_data_1day

I01 - idx_instrument_time

--------------------------------------------------------------------------------
*/


/* T01 - tbl_instrument */
CREATE TABLE IF NOT EXISTS tbl_instrument (
  ins_id SERIAL PRIMARY KEY,
  symbol TEXT NOT NULL,
  name TEXT NOT NULL,
  industry TEXT
);


/* T02 - tbl_price_data_1day */
CREATE TABLE IF NOT EXISTS tbl_price_data_1day (
   pd_ins_id INTEGER NOT NULL,
   dtime  TIMESTAMPTZ NOT NULL,
   open   DOUBLE PRECISION NOT NULL,
   high   DOUBLE PRECISION NOT NULL,
   low    DOUBLE PRECISION NOT NULL,
   close  DOUBLE PRECISION NOT NULL,
   volume INTEGER  NOT NULL,
   PRIMARY KEY (pd_ins_id, dtime),
   CONSTRAINT fk_instrument FOREIGN KEY (pd_ins_id) REFERENCES tbl_instrument (ins_id)
);

/* Convert the standard table into a hypertable partitioned on the time column using the create_hypertable() function provided by Timescale. */
SELECT create_hypertable('tbl_price_data_1day', 'dtime');

/* I01 - idx_instrument_time */
CREATE INDEX idx_instrument_time ON tbl_price_data_1day (pd_ins_id, dtime DESC);

