
/*
--------------------------------------------------------------------------------

-- V01 - viw_latest_price_data_by_symbol
-- V02 - viw_instrument_uk_equities
-- V03 - viw_price_data_stats_by_symbol 
-- V04 - viw_instrument_us_etfs
-- V05 - viw_instrument_us_sp500_constituents
-- V06 - viw_instrument_price_data_records_count

--------------------------------------------------------------------------------
*/


-- V01 - viw_latest_price_data_by_symbol 
-- use this view when we want to get only the latest record by pd_time for each symbol
\echo "Creating VIEW viw_latest_price_data_by_symbol";
CREATE OR REPLACE VIEW viw_latest_price_data_by_symbol AS
WITH recent_data AS (
  SELECT
      pd_symbol,
      pd_time,
      open,
      high,
      low,
      close,
      volume,
      ema_5,
      ema_13,
      sma_50,
      sma_200,
      ROW_NUMBER() OVER (PARTITION BY pd_symbol ORDER BY pd_time DESC) AS latest_row_num_by_symbol
  FROM tbl_price_data_1day
  WHERE pd_time >= CURRENT_DATE - INTERVAL '15 days'
)
SELECT *
FROM recent_data
WHERE latest_row_num_by_symbol = 1;


-- V02 - viw_instrument_uk_equities
-- use this view when we want to get all the instruments which are UK EQUITIES
\echo "Creating VIEW viw_instrument_uk_equities";
CREATE OR REPLACE VIEW viw_instrument_uk_equities AS
SELECT *
FROM tbl_instrument
WHERE exchange_code='LSE' and asset_type='ETF';


-- V03 - viw_price_data_stats_by_symbol 
-- use this view when we want to see oldest and latest records by time and count of records for each symbol
\echo "Creating VIEW viw_price_data_stats_by_symbol";
CREATE OR REPLACE VIEW viw_price_data_stats_by_symbol AS
SELECT
  pd_symbol,
  MIN(pd_time) as oldest_rec_pd_time,
  MAX(pd_time) as latest_rec_pd_time,
  COUNT(*) as num_records
FROM tbl_price_data_1day
GROUP BY pd_symbol
ORDER By pd_symbol;

-- V04 - viw_instrument_us_etfs
-- use this view when we want to get all the instruments which are US ETFs
\echo "Creating VIEW viw_instrument_us_etfs";
CREATE OR REPLACE VIEW viw_instrument_us_etfs AS
SELECT *
FROM tbl_instrument
WHERE exchange_code='UNKNOWN' and asset_type='ETF' and data_source='THINKORSWIM';


-- V05 - viw_instrument_us_sp500_constituents
-- use this view when we want to get all the instruments which are in the S&P500 index
\echo "Creating VIEW viw_instrument_us_sp500_constituents";
CREATE OR REPLACE VIEW viw_instrument_us_sp500_constituents AS
SELECT *
FROM tbl_instrument
WHERE asset_type='STOCK' and note_1='SP500';

-- V06 - viw_instrument_price_data_records_count
-- use this view when we want to see how much data we have in the price_data_1day table for each symbol
\echo "Creating VIEW viw_instrument_price_data_records_count";
CREATE OR REPLACE VIEW viw_instrument_price_data_records_count AS
SELECT
  i.symbol,
  i.exchange_code,
  i.asset_type,
  i.note_1,
  i.data_source,
  COUNT(p.pd_time) AS price_data_rec_count
FROM
  tbl_instrument i
LEFT JOIN
  tbl_price_data_1day p ON i.symbol = p.pd_symbol
GROUP BY
  i.symbol, 
  i.exchange_code,
  i.asset_type,
  i.note_1,
  i.data_source
order by  
  i.symbol, 
  i.exchange_code,
  i.asset_type,
  i.note_1,
  i.data_source
;
