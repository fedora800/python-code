
/*
--------------------------------------------------------------------------------

-- L01 - tbl_exchange_data
-- L02 - tbl_gics_sector
-- L03A - tbl_instrument - S&P500 constituents
-- L03B - tbl_instrument - US ETFs
-- L03C - tbl_instrument - UK ETFs
-- L03D - tbl_instrument - IN NIFTY 200 Stocks
-- L03E - tbl_instrument - Top US 100 ETFs by Assets under management
-- L03F - tbl_instrument - example INSERT statements
-- L04A - tbl_price_data_1day - USA
-- L04B - tbl_price_data_1day - UK
-- L05 - tbl_symbol_filters

--------------------------------------------------------------------------------
*/

-- L01 - tbl_exchange_data
\echo "Loading into table tbl_exchange"
\copy tbl_exchange FROM '~/git-projects/python-code/timescaledb/data/instrument_lists/tbl_exchange_data.csv' DELIMITER ',' CSV HEADER;

-- L02 - tbl_gics_sector
\echo "Loading into table tbl_gics_sector"
\copy tbl_gics_sector FROM '~/git-projects/python-code/timescaledb/data/instrument_lists/tbl_gics_mapping.csv' DELIMITER ',' CSV HEADER;


-- L03A - tbl_instrument - S&P500 constituents
\echo "Loading into table tbl_instrument - S&P500 constituents"
\copy tbl_instrument (symbol, name, sector_code, sub_industry_code, exchange_code, asset_type, country_code, data_source, note_1) FROM '~/git-projects/python-code/timescaledb/data/instrument_lists/tbl_instrument_data_sp500_symbols.csv' DELIMITER ',' CSV HEADER;


-- L03B - tbl_instrument - US ETFs
-- this is a list of all (around 1917 ) US ETFS from Scan > All ETFs watchlist scan file download from ThinkorSwim
-- $ dos2unix thinkorswim_instrument_data.csv 
-- $ sed -i 's/$/,ETF,UNKNOWN,THINKORSWIM/' thinkorswim_instrument_data.csv 
-- $ sed -i 's/\(Symbol,.*\)\(ETF.*\)/\1asset_type,exchange_code,data_source/' thinkorswim_instrument_data.csv 
\echo "Loading into table tbl_instrument - US ETFs"
\copy tbl_instrument (symbol, name, sector, industry, sub_industry, asset_type, exchange_code, data_source) FROM '~/git-projects/python-code/timescaledb/data/instrument_lists/tbl_instrument_data_etf_thinkorswim.csv' DELIMITER ',' CSV HEADER;

-- L03C - tbl_instrument - UK ETFs
-- this is a list i massaged from Trading212 website JSON data
\echo "Loading into table tbl_instrument - UK ETFs"
\copy tbl_instrument (symbol, name, exchange_code, asset_type, data_source) FROM '~/git-projects/python-code/timescaledb/data/instrument_lists/tbl_instrument_UK_etfs_trading212.csv' DELIMITER ',' CSV HEADER;

-- https://etfdb.com/compare/market-cap/  top 100 etfs by assets
-- awk -F',' '{print $1","$2",US,ETF"}' /tmp/aaa | sort > /tmp/bbb
-- COPY tmp_tbl_instrument (symbol, name, country_code, asset_type) FROM '/tmp/bbb' DELIMITER ',' CSV HEADER;
-- but it will not copy everything as symbols will already exist so we need to do the temp table thing

-- this is a list i got as csv from Investing.com website 
  \copy tbl_instrument (symbol, name, sector, industry, sub_industry, exchange_code, asset_type, note_1) from '~/git-projects/python-code/timescaledb/data/instrument_lists/tbl_instrument_UK_etfs_investing_com.csv' DELIMITER ',' CSV HEADER;
-- will need to do the below for now to clean it further - 
update tbl_instrument set note_1='MOST-ACTIVE;', country_code='UK' where exchange_code='LSE' and data_source is null and note_1='INVESTING-COM'

-- L03D - tbl_instrument - IN NIFTY 200 Stocks
-- https://www.nseindia.com/products-services/indices-nifty200-index   - provides a csv file
-- $ awk -F',' 'NR==1 {print $3","$1",exchange_code,asset_type,data_source,note_1"} NR>1 {print $3".NS,"$1",NSE,STOCK,NSEINDIA-COM,NIFTY200"}' ind_nifty200list.csv  > tbl_instrument_NSE_nifty200.csv
\echo "Loading into table tbl_instrument - IN NIFTY 200 Stocks"
\copy tbl_instrument (symbol, name, exchange_code, asset_type, data_source, note_1) FROM '~/git-projects/python-code/timescaledb/data/instrument_lists/tbl_instrument_NSE_nifty200.csv' DELIMITER ',' CSV HEADER;

-- L03E - tbl_instrument - Top US 100 ETFs by Assets under management
--go to https://stockanalysis.com/etf/screener/
--and 'Edit View' to only pick these columns -
--Symbol ;Fund Name ;Asset Class ;Assets; Holdings ;Exp. Ratio
--paste them into vim (tab is the seperator), do it on 2nd page also to get a total of 100 symbols
--replace it with semi-colon(;) and remove the commas.
--then replace all ; with ,
--Symbol ,Fund Name ,Asset Class ,Assets, Holdings ,Exp. Ratio
--SPY,SPDR S&P 500 ETF Trust,Equity,615.14B,504,0.09%
--VOO,Vanguard S&P 500 ETF,Equity,589.30B,507,0.03%
--IVV,iShares Core S&P 500 ETF,Equity,581.55B,507,0.03%
--$ awk -F',' 'NR==1 {print "symbol,name,asset_type,data_source,note_1"} NR>1 {print $1","$2",ETF,STOCKANALYSIS-COM, US_TOP_100_BY_AUM ; aum="$4"; hldgs="$5"; expratio="$6}' temp-1.csv > temp.csv

-- do these 3 steps as there is SPY symbol duplicate. otherwise just remove SPY from my above file.
--CREATE TEMP TABLE temp_instrument (
--    symbol TEXT,
--    name TEXT,
--    asset_type typ_asset_type,
--    data_source typ_data_source,
--    note_1 TEXT
--);
--COPY temp_instrument (symbol, name, asset_type, data_source,note_1)
--FROM 'C:\mytmp\downloads\temp.csv'
--DELIMITER ','
--CSV HEADER;
--INSERT INTO tbl_instrument (symbol, name, asset_type, data_source, note_1)
--SELECT symbol, name, asset_type, data_source, note_1
--FROM temp_instrument
--ON CONFLICT (symbol) DO NOTHING;

-- L03F - tbl_instrument - example INSERT statements
/*
insert into tbl_instrument(symbol, name, exchange_code, asset_type, country_code, data_source, note_1) 
  values ('PLTR','Palantir Technologies Inc', 'NASDAQ', 'STOCK', 'US', 'YFINANCE','');
insert into tbl_instrument(symbol, name, exchange_code, asset_type, country_code, data_source, note_1) 
  values ('VUKE.L','Vanguard FTSE 100 UCITS ETF (VUKE)', 'LSE', 'STOCK', 'UK', 'YFINANCE','');
-- https://swingtradebot.com/stocks-tagged-as/41811-ibd-50
insert into tbl_instrument(symbol, name, asset_type, country_code, data_source, note_1) 
  values ('ALAB','Astera Labs', 'STOCK', 'US', 'ONLINE_BLOG','IBD50-04Feb2025');
*/

-- L04A - tbl_price_data_1day - USA
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

-- L04B - tbl_price_data_1day - UK
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

-- L05 - tbl_symbol_filters
INSERT INTO public.tbl_symbol_filters(filter_name, filter_query, filter_description, deleted)
	VALUES ('RS-UK-ETF-List', 
          'select * from viw_price_data_uk_most_traded', 'Most active around 50 UK ETFs', False);
INSERT INTO public.tbl_symbol_filters(filter_name, filter_query, filter_description, deleted)
	VALUES ('RS-US-ETF-List', 
          'select * from viw_price_data_us_etfs_most_traded', 'Most active around 50 US ETFs', False);
INSERT INTO public.tbl_symbol_filters(filter_name, filter_query, filter_description, category, deleted)
  VALUES ('RS-scan-uk-above-sma50', 
          'select * from viw_tmp_001', 'UK ETFs most traded above sma_50', 'scans', False);
INSERT INTO public.tbl_symbol_filters(filter_name, filter_query, filter_description, category, deleted)
	VALUES ('SS-scan-test1', 
          $$select symbol as pd_symbol, name, note_1 from tbl_instrument where symbol in ('SPY', 'META', 'TSLA', 'XOM')$$, 'some symbols of interest/testing', 'scans', False);
INSERT INTO public.tbl_symbol_filters(filter_name, filter_query, filter_description, category, deleted)
	VALUES ('SS-US-CRS-above-0', 
          $$select pd_symbol, name, exchange_code, crs_50 from viw_latest_price_data_by_symbol where note_1='SP500' and crs_50 > 0$$, 'US SP500 stocks with CRS above 0', 'scans', False);
INSERT INTO public.tbl_symbol_filters(filter_name, filter_query, filter_description, category, deleted)
	VALUES ('SS-US-TOP100-AUM-ETFS-CRS-above-0', 
          $$select pd_symbol, name, exchange_code, crs_50 from viw_latest_price_data_by_symbol where pd_symbol in (select symbol from viw_instrument_in_us_top100_etfs_by_aum) and crs_50 > 0$$, 'US TOP100 AUM ETFS stocks with CRS above 0', 'scans', False);


/*
insert into tbl_symbol_filters (filter_name, filter_query, filter_description, deleted) values ('RS-UK-ETF-1', $$select symbol, name  from viw_instrument_uk_equities where note_1 like '%MOST-ACTIVE%' and deleted=False;$$, 'UK most traded around top 50 etfs', False);

 insert into tbl_symbol_filters (filter_name, filter_query, filter_description, deleted) values ('RS-US-ETFs', $$select symbol, name  from viw_instrument_us_etfs where symbol like '%P%Y%' and deleted=False;$$, 'US some etfs', False);
*/







