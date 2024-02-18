/*
 --------------------------------------------------------------------------------
 
 -- V01 - viw_latest_price_data_by_symbol
 -- V02 - viw_instrument_uk_equities
 -- V03 - viw_price_data_stats_by_symbol 
 -- V04 - viw_instrument_us_etfs
 -- V05 - viw_instrument_us_sp500_constituents
 -- V06 - viw_instrument_price_data_records_count
 -- V07 - viw_price_data_uk_most_traded
 
 --------------------------------------------------------------------------------
 */
-- V01 - viw_latest_price_data_by_symbol 
-- use this view when we want to get only the latest record by pd_time for each symbol
\echo "Creating VIEW viw_latest_price_data_by_symbol";
CREATE OR REPLACE VIEW viw_latest_price_data_by_symbol AS 
WITH recent_price_data AS (
  SELECT pd_symbol,
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
    ROW_NUMBER() OVER (
      PARTITION BY pd_symbol
      ORDER BY pd_time DESC
    ) AS latest_row_num_by_symbol
  FROM tbl_price_data_1day
  WHERE pd_time >= CURRENT_DATE - INTERVAL '15 days'
  ),
symbol_data AS (
	SELECT symbol, name, exchange_code, sector FROM tbl_instrument		
)
SELECT RD.*, SD.*
FROM recent_price_data RD, symbol_data SD
WHERE 
RD.pd_symbol = SD.symbol
AND latest_row_num_by_symbol = 1;


-- V02 - viw_instrument_uk_equities
-- use this view when we want to get all the instruments which are UK EQUITIES
\echo "Creating VIEW viw_instrument_uk_equities";
CREATE OR REPLACE VIEW viw_instrument_uk_equities AS
SELECT *
FROM tbl_instrument
WHERE 
  country_code = 'UK'
  and asset_type = 'ETF'
  and deleted=false;


-- V03 - viw_price_data_stats_by_symbol 
-- use this view when we want to see oldest and latest records by time and count of records for each symbol
\echo "Creating VIEW viw_price_data_stats_by_symbol";
CREATE OR REPLACE VIEW viw_price_data_stats_by_symbol AS 
WITH tmp_pricedata AS (
  SELECT pd_symbol,
    MIN(pd_time) as oldest_rec_pd_time,
    MAX(pd_time) as latest_rec_pd_time,
    COUNT(*) as num_records
  FROM tbl_price_data_1day
  GROUP BY pd_symbol
  ORDER By pd_symbol
)
SELECT t_I.symbol,
  t_I.name,
  t_I.exchange_code,
  t_I.asset_type,
  t_P.*
FROM tbl_instrument t_I,
  tmp_pricedata t_P
WHERE t_I.symbol = t_P.pd_symbol
  and t_I.deleted=false
ORDER BY t_I.symbol;


-- V04 - viw_instrument_us_etfs
-- use this view when we want to get all the instruments which are US ETFs
\echo "Creating VIEW viw_instrument_us_etfs";
CREATE OR REPLACE VIEW viw_instrument_us_etfs AS
SELECT *
FROM tbl_instrument
WHERE exchange_code = 'UNKNOWN'
  and asset_type = 'ETF'
  and data_source = 'THINKORSWIM'
  and deleted=false;


-- V05 - viw_instrument_us_sp500_constituents
-- use this view when we want to get all the instruments which are in the S&P500 index
\echo "Creating VIEW viw_instrument_us_sp500_constituents";
CREATE OR REPLACE VIEW viw_instrument_us_sp500_constituents AS
SELECT *
FROM tbl_instrument
WHERE asset_type = 'STOCK'
  and note_1 = 'SP500'
  and deleted=false;


-- V06 - viw_instrument_price_data_records_count
-- use this view when we want to see how much data we have in the price_data_1day table for each symbol
\echo "Creating VIEW viw_instrument_price_data_records_count";
CREATE OR REPLACE VIEW viw_instrument_price_data_records_count AS
SELECT i.symbol,
  i.exchange_code,
  i.asset_type,
  i.note_1,
  i.data_source,
  COUNT(p.pd_time) AS price_data_rec_count
FROM tbl_instrument i
  LEFT JOIN tbl_price_data_1day p ON i.symbol = p.pd_symbol
WHERE
  i.deleted=false
GROUP BY i.symbol,
  i.exchange_code,
  i.asset_type,
  i.note_1,
  i.data_source
order by i.symbol,
  i.exchange_code,
  i.asset_type,
  i.note_1,
  i.data_source;



-- V07 - viw_price_data_uk_most_traded
-- use this view to get a list of 50 symbols from UK ETFs which have most volume over last 30 days and so are the most active
\echo "Creating VIEW viw_price_data_uk_most_traded";
CREATE OR REPLACE VIEW viw_price_data_uk_most_traded AS 
WITH tmp_latest_30_days_data AS (
    SELECT v_UK.symbol,
      t_PD.pd_time,
      t_PD.close,
      t_PD.volume,
      v_UK.name,
      v_UK.exchange_code,
      v_UK.asset_type,
      ROW_NUMBER() OVER (
        PARTITION BY pd_symbol
        ORDER BY pd_time DESC
      ) AS row_num
    FROM tbl_price_data_1day t_PD
      JOIN viw_instrument_uk_equities v_UK on t_PD.pd_symbol = v_UK.symbol
    WHERE pd_time > now() - INTERVAL '30 days'
  )
SELECT symbol,
  name,
  exchange_code,
  asset_type,
  AVG(volume) AS avg_volume_over_last_30_days
FROM tmp_latest_30_days_data
WHERE row_num <= 5
GROUP BY symbol,
  name,
  exchange_code,
  asset_type
HAVING AVG(volume) > 50000
ORDER BY AVG(volume) DESC
LIMIT 50;
