
/*
--------------------------------------------------------------------------------

-- V01 - viw_latest_price_data_by_symbol

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
