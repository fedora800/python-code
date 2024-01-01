
/*
--------------------------------------------------------------------------------

L01 - tbl_exchange_data
L02 - tbl_instrument
L03 - tbl_price_data_1day

--------------------------------------------------------------------------------
*/

/* L01 - tbl_exchange_data */
\copy tbl_exchange FROM './tbl_exchange_data.csv' DELIMITER ',' CSV HEADER;


/* L02 - tbl_instrument */
\copy tbl_instrument (symbol, name, industry, exchange_code, asset_type) FROM './tbl_instrument_data.csv' DELIMITER ',' CSV HEADER;


/* L03 - tbl_price_data_1day */
#awk -F',' 'BEGIN {OFS=",";} {print $1, $2, $4, $5, $6, $7, $8;}' sp500_quotes_data.csv > tbl_price_data_1day_data.csv 
\copy tbl_price_data_1day (pd_time,pd_symbol,close,high,low,open,volume) FROM './tbl_price_data_1day_data.csv' DELIMITER ',' CSV HEADER;

