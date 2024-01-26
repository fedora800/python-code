
/*
--------------------------------------------------------------------------------

-- L01 - tbl_exchange_data
-- L02A - tbl_instrument - S&P500 constituents
-- L02B - tbl_instrument - US ETFs
-- L02C - tbl_instrument - UK ETFs
-- L03A - tbl_price_data_1day - USA
-- L03B - tbl_price_data_1day - UK

--------------------------------------------------------------------------------
*/

-- L01 - tbl_exchange_data
\echo "Loading into table tbl_exchange"
\copy tbl_exchange FROM '~/git-projects/python-code/timescaledb/data/tbl_exchange_data.csv' DELIMITER ',' CSV HEADER;


-- L02A - tbl_instrument - S&P500 constituents
\echo "Loading into table tbl_instrument"
\copy tbl_instrument (symbol, name, industry, exchange_code, asset_type, data_source, note_1) FROM '~/git-projects/python-code/timescaledb/data/tbl_instrument_data_sp500_symbols.csv' DELIMITER ',' CSV HEADER;


-- L02B - tbl_instrument - US ETFs
-- this is a list of all (around 1917 ) US ETFS from Scan > All ETFs watchlist scan file download from ThinkorSwim
-- $ dos2unix thinkorswim_instrument_data.csv 
-- $ sed -i 's/$/,ETF,UNKNOWN,THINKORSWIM/' thinkorswim_instrument_data.csv 
-- $ sed -i 's/\(Symbol,.*\)\(ETF.*\)/\1asset_type,exchange_code,data_source/' thinkorswim_instrument_data.csv 
\echo "Loading into table tbl_instrument"
\copy tbl_instrument (symbol, name, sector, industry, sub_industry, asset_type, exchange_code, data_source) FROM '~/git-projects/python-code/timescaledb/data/tbl_instrument_data_etf_thinkorswim.csv' DELIMITER ',' CSV HEADER;

-- L02C - tbl_instrument - UK ETFs
-- this is a list i massaged from Trading212 website JSON data
\echo "Loading into table tbl_instrument"
\copy tbl_instrument (symbol, name, exchange_code, asset_type, data_source) FROM '~/git-projects/python-code/timescaledb/data/instrument_lists/tbl_instrument_UK_etfs_trading212.csv' DELIMITER ',' CSV HEADER

-- L03A - tbl_price_data_1day - USA
\echo "Loading into table tbl_price_data_1day -- 2 year price data for around 25 S&P500 symbols - USA "
-- awk -F',' 'BEGIN {OFS=",";} {print $1, $2, $4, $5, $6, $7, $8;}' sp500_quotes_data.csv > tbl_price_data_1day_data.csv 
--\copy tbl_price_data_1day (pd_symbol,pd_time,open,high,low,close, volume) FROM './tbl_price_data_1day_data.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/AAPL.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/MSFT.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/AMZN.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/NVDA.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/GOOGL.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/TSLA.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/GOOG.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/BRK-B.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/META.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/UNH.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/XOM.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/LLY.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/JPM.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/JNJ.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/V.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/PG.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/MA.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/AVGO.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/HD.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/CVX.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/MRK.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/ABBV.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/COST.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/PEP.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/ADBE.csv' DELIMITER ',' CSV HEADER;

-- L03B - TBL_PRICE_DATA_1DAY - UK
\echo "Loading into table tbl_price_data_1day -- 2 year price data for 4 ETFS - USA "
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/VHYG.L.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/VMID.L.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/VUKE.L.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/VUSA.L.csv' DELIMITER ',' CSV HEADER;


