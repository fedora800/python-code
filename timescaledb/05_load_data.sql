
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
\copy tbl_exchange FROM '~/git-projects/python-code/timescaledb/data/instrument_lists/tbl_exchange_data.csv' DELIMITER ',' CSV HEADER;


-- L02A - tbl_instrument - S&P500 constituents
\echo "Loading into table tbl_instrument"
\copy tbl_instrument (symbol, name, industry, exchange_code, asset_type, data_source, note_1) FROM '~/git-projects/python-code/timescaledb/data/instrument_lists/tbl_instrument_data_sp500_symbols.csv' DELIMITER ',' CSV HEADER;


-- L02B - tbl_instrument - US ETFs
-- this is a list of all (around 1917 ) US ETFS from Scan > All ETFs watchlist scan file download from ThinkorSwim
-- $ dos2unix thinkorswim_instrument_data.csv 
-- $ sed -i 's/$/,ETF,UNKNOWN,THINKORSWIM/' thinkorswim_instrument_data.csv 
-- $ sed -i 's/\(Symbol,.*\)\(ETF.*\)/\1asset_type,exchange_code,data_source/' thinkorswim_instrument_data.csv 
\echo "Loading into table tbl_instrument"
\copy tbl_instrument (symbol, name, sector, industry, sub_industry, asset_type, exchange_code, data_source) FROM '~/git-projects/python-code/timescaledb/data/instrument_lists/tbl_instrument_data_etf_thinkorswim.csv' DELIMITER ',' CSV HEADER;

-- L02C - tbl_instrument - UK ETFs
-- this is a list i massaged from Trading212 website JSON data
\echo "Loading into table tbl_instrument"
\copy tbl_instrument (symbol, name, exchange_code, asset_type, data_source) FROM '~/git-projects/python-code/timescaledb/data/instrument_lists/tbl_instrument_UK_etfs_trading212.csv' DELIMITER ',' CSV HEADER;

-- this is a list i got as csv from Investing.com website 
  \copy tbl_instrument (symbol, name, sector, industry, sub_industry, exchange_code, asset_type, note_1) from '~/git-projects/python-code/timescaledb/data/instrument_lists/tbl_instrument_UK_etfs_investing_com.csv' DELIMITER ',' CSV HEADER;
-- will need to do the below for now to clean it further - 
update tbl_instrument set note_1='MOST-ACTIVE;', country_code='UK' where exchange_code='LSE' and data_source is null and note_1='INVESTING-COM'


-- L03A - tbl_price_data_1day - USA
\echo "Loading into table tbl_price_data_1day -- 2 year price data for around 25 S&P500 symbols - USA "
-- awk -F',' 'BEGIN {OFS=",";} {print $1, $2, $4, $5, $6, $7, $8;}' sp500_quotes_data.csv > tbl_price_data_1day_data.csv 
--\copy tbl_price_data_1day (pd_symbol,pd_time,open,high,low,close, volume) FROM './tbl_price_data_1day_data.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/AAPL.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/MSFT.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/AMZN.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/NVDA.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/GOOGL.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/TSLA.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/GOOG.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/META.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/UNH.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/XOM.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/LLY.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/JPM.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/JNJ.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/V.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/PG.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/MA.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/AVGO.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/HD.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/CVX.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/MRK.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/ABBV.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/COST.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/PEP.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/ADBE.csv' DELIMITER ',' CSV HEADER;

-- L03B - TBL_PRICE_DATA_1DAY - UK
\echo "Loading into table tbl_price_data_1day -- 2 year price data for 4 ETFS - UK "
--\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/uk_etfs/VHYG.L.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/uk_etfs/VMID.L.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/uk_etfs/VUKE.L.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/uk_etfs/VUSA.L.csv' DELIMITER ',' CSV HEADER;


--\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/uk_etfs/VUSA.L.csv' DELIMITER ',' CSV HEADER WITH (FORMAT CSV, NULL '', country_code 'UK');

PREFIX="\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '"
SUFFIX="' DELIMITER ',' CSV HEADER;"

# \copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '/tmp/5ESG.L.csv' DELIMITER ',' CSV HEADER;

for FNAME in *.L.csv
do
  echo ${PREFIX}/tmp/${FNAME}${SUFFIX}
done


