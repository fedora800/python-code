
/*
--------------------------------------------------------------------------------

L01 - tbl_exchange_data
L02 - tbl_instrument

--------------------------------------------------------------------------------
*/

/* L01 - tbl_exchange_data */
\copy tbl_exchange FROM './tbl_exchange_data.csv' DELIMITER ',' CSV HEADER;


/* L02 - tbl_instrument */
\copy tbl_instrument (symbol, name, industry, exch_code, asset_type) FROM './tbl_instrument.csv' DELIMITER ',' CSV HEADER;
