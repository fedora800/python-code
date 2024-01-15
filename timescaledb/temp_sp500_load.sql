
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/AAPL.csv' DELIMITER ',' CSV HEADER;

