
/*
--------------------------------------------------------------------------------

-- V01 - viw_latest_price_data_by_symbol
-- V02 - viw_instrument_uk_equities
-- V03 - viw_price_data_stats_by_symbol 

--------------------------------------------------------------------------------
*/


-- V01 - viw_latest_price_data_by_symbol 
-- use this view when we want to get only the latest record by pd_time for each symbol
\echo "Creating VIEW viw_latest_price_data_by_symbol";
CREATE VIEW viw_latest_price_data_by_symbol AS
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
CREATE VIEW viw_instrument_uk_equities AS
SELECT *
FROM tbl_instrument
WHERE exchange_code='UK-EXCH-TODO' and asset_type='EQUITY_FUNDS';


-- V03 - viw_price_data_stats_by_symbol 
-- use this view when we want to see oldest and latest records by time and count of records for each symbol
\echo "Creating VIEW viw_price_data_stats_by_symbol";
CREATE VIEW viw_price_data_stats_by_symbol AS
SELECT
  pd_symbol,
  MIN(pd_time) as oldest_rec_pd_time,
  MAX(pd_time) as latest_rec_pd_time,
  COUNT(*) as num_records
FROM tbl_price_data_1day
GROUP BY pd_symbol
ORDER By pd_symbol;




