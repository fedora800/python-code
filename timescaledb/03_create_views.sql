/*
 --------------------------------------------------------------------------------
 -- General
-- viw_instrument_table_summary
-- viw_latest_price_data_by_symbol

 -- viw_instrument_uk_equities
 -- viw_instrument_us_equities
 -- V03 - viw_price_data_stats_by_symbol 
 -- V04 - viw_instrument_us_etfs
 -- V05 - viw_instrument_us_sp500_constituents
 -- viw_instrument_in_nifty200_constituents
 -- V06 - viw_instrument_price_data_records_count
 -- viw_price_data_uk_most_traded
 -- viw_price_data_us_most_traded
 

 --------------------------------------------------------------------------------
 */

-- General

-- gives a count of records in tbl_instrument grouped by various fields
\echo "Creating VIEW viw_instrument_table_summary";
CREATE OR REPLACE VIEW viw_instrument_table_summary AS
SELECT
  country_code,
  exchange_code,
  asset_type,
  note_1,
  data_source,
  deleted,
  COUNT(*) AS num_records
FROM
  tbl_instrument
GROUP BY
  country_code,
  exchange_code,
  asset_type,
  note_1,
  data_source,
  deleted;



-- V01 - viw_latest_price_data_by_symbol 
-- use this view when we want to get only the latest price data record by pd_time for each symbol
\echo "Creating VIEW viw_latest_price_data_by_symbol";
CREATE OR REPLACE VIEW viw_latest_price_data_by_symbol AS 
WITH tmp_ranked_tbl_price_data_1day AS (
  SELECT 
	  *,    
	  ROW_NUMBER() OVER (
      PARTITION BY pd_symbol
      ORDER BY pd_time DESC
    ) AS latest_row_num_by_symbol
  FROM tbl_price_data_1day
  WHERE 
    pd_time >= CURRENT_DATE - INTERVAL '30 days'
 --   AND pd_symbol in ('AAPL', 'PLTR', 'SPY')
)
SELECT A.*, B.name, B.exchange_code, B.asset_type, B.country_code, B.sector_code, B.industry_code, B.sub_industry_code, B.data_source, B.note_1 
FROM tmp_ranked_tbl_price_data_1day A, tbl_instrument B
WHERE 
A.pd_symbol = B.symbol
and B.deleted = false 
and A.latest_row_num_by_symbol = 1
ORDER BY B.symbol;


-- viw_instrument_uk_equities
-- use this view when we want to get all the instruments which are UK EQUITIES
\echo "Creating VIEW viw_instrument_uk_equities";
CREATE OR REPLACE VIEW viw_instrument_uk_equities AS
SELECT *
FROM tbl_instrument
WHERE 
  country_code = 'UK'
  and deleted=false
order by symbol;



--  viw_instrument_us_equities
-- use this view when we want to get all the instruments which are US EQUITIES
\echo "Creating VIEW viw_instrument_us_equities";
CREATE OR REPLACE VIEW viw_instrument_us_equities AS
SELECT *
FROM tbl_instrument
WHERE 
  country_code = 'US'
  and deleted=false
order by symbol;

-- V03 - viw_price_data_stats_by_symbol 
-- use this view when we want to see oldest and latest records by time and count of records for each symbol as well as other stats
\echo "Creating VIEW viw_price_data_stats_by_symbol";
CREATE OR REPLACE VIEW viw_price_data_stats_by_symbol AS 
WITH tmp_pricedata AS (
  SELECT pd_symbol,
    MIN(pd_time) as oldest_rec_pd_time,
    MAX(pd_time) as latest_rec_pd_time,
    COUNT(*) as num_records,
    -- Calculate the difference between the max and min pd_time in days
    EXTRACT(DAY FROM (MAX(pd_time) - MIN(pd_time))) AS time_difference_in_days,
    -- Calculate the difference between max(pd_time) and today in days
    EXTRACT(DAY FROM (CURRENT_DATE - MAX(pd_time))) AS days_since_latest,
    -- Calculate weekdays only (excluding weekends) between min and max pd_time
    (SELECT COUNT(*) 
     FROM generate_series(MIN(pd_time)::DATE, MAX(pd_time)::DATE, '1 day'::INTERVAL) AS series(date)
     WHERE EXTRACT(DOW FROM series.date) NOT IN (0, 6)) AS weekdays_between_oldest_and_latest
  FROM tbl_price_data_1day
  GROUP BY pd_symbol
  ORDER BY pd_symbol
)
SELECT t_P.pd_symbol,
  t_I.name,
  t_I.exchange_code,
  t_I.asset_type,
  t_P.oldest_rec_pd_time,
  t_P.latest_rec_pd_time,
  t_P.num_records,
  t_P.time_difference_in_days, -- Add the calculated difference between max and min pd_time in days
  t_P.days_since_latest, -- Add the calculated difference between max(pd_time) and today in days
  t_P.weekdays_between_oldest_and_latest -- Add the calculated weekdays difference
FROM tbl_instrument t_I,
  tmp_pricedata t_P
WHERE t_I.symbol = t_P.pd_symbol
  AND t_I.deleted = false
ORDER BY t_I.symbol;


-- V04 - viw_instrument_us_etfs
-- use this view when we want to get all the instruments which are US ETFs
\echo "Creating VIEW viw_instrument_us_etfs";
CREATE OR REPLACE VIEW viw_instrument_us_etfs AS
SELECT *
FROM tbl_instrument
WHERE 
  asset_type = 'ETF'
  and deleted=false
ORDER BY symbol;


-- V05 - viw_instrument_us_sp500_constituents
-- use this view when we want to get all the instruments which are in the S&P500 index
\echo "Creating VIEW viw_instrument_us_sp500_constituents";
CREATE OR REPLACE VIEW viw_instrument_us_sp500_constituents AS
SELECT *
FROM tbl_instrument
WHERE asset_type = 'STOCK'
  and note_1 = 'SP500'
  and deleted=false
ORDER BY symbol;

-- viw_instrument_in_nifty200_constituents
-- use this view when we want to get all the instruments which are in the NIFTY 200 index
\echo "Creating VIEW viw_instrument_in_nifty200_constituents";
CREATE OR REPLACE VIEW viw_instrument_in_nifty200_constituents AS
SELECT *
FROM tbl_instrument
WHERE exchange_code = 'NSE'
  and asset_type = 'STOCK'
  and note_1 = 'NIFTY200'
  and deleted=false
ORDER BY symbol;

-- viw_instrument_in_us_top100_etfs_by_aum
-- use this view when we want to get the top 100 US ETF instruments by assets under management
\echo "Creating VIEW viw_instrument_in_us_top100_etfs_by_aum";
CREATE OR REPLACE VIEW viw_instrument_in_us_top100_etfs_by_aum AS
SELECT *
FROM tbl_instrument
WHERE 
  asset_type = 'ETF'
  and note_1 like '%US_TOP_100_BY_AUM%'
  and deleted=false
ORDER BY symbol;

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



-- viw_price_data_uk_most_traded
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
      v_UK.sector_code,
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
  sector_code,
  AVG(volume) AS avg_volume_over_last_30_days
FROM tmp_latest_30_days_data
WHERE row_num <= 5
GROUP BY symbol,
  name,
  exchange_code,
  asset_type,
  sector_code
HAVING AVG(volume) > 50000
ORDER BY symbol
LIMIT 50;


-- viw_price_data_us_most_traded
-- use this view to get a list of 50 symbols from US ETFs which have the most volume over the last 30 days and are the most active
\echo "Creating VIEW viw_price_data_us_most_traded";
CREATE OR REPLACE VIEW viw_price_data_us_most_traded AS 
WITH tmp_latest_30_days_data AS (
    SELECT v_US.symbol,
      t_PD.pd_time,
      t_PD.close,
      t_PD.volume,
      v_US.name,
      v_US.exchange_code,
      v_US.asset_type,
      v_US.sector_code,
      ROW_NUMBER() OVER (
        PARTITION BY pd_symbol
        ORDER BY pd_time DESC
      ) AS row_num
    FROM tbl_price_data_1day t_PD
      JOIN viw_instrument_us_etfs v_US ON t_PD.pd_symbol = v_US.symbol
    WHERE pd_time > now() - INTERVAL '30 days'
    AND v_US.asset_type = 'ETF'
  )
SELECT symbol,
  name,
  exchange_code,
  asset_type,
  sector_code,
  AVG(volume) AS avg_volume_over_last_30_days
FROM tmp_latest_30_days_data
WHERE row_num <= 5
GROUP BY symbol,
  name,
  exchange_code,
  asset_type,
  sector_code
HAVING AVG(volume) > 50000
ORDER BY symbol
LIMIT 50;


-- V08 - viw_price_data_us_etfs_most_traded
-- use this view to get a list of 50 symbols from US ETFs which have most volume over last 30 days and so are the most active
\echo "Creating VIEW viw_price_data_us_etfs_most_traded";
CREATE OR REPLACE VIEW viw_price_data_us_etfs_most_traded AS 
WITH tmp_latest_30_days_data AS (
    SELECT v_US.symbol,
      t_PD.pd_time,
      t_PD.close,
      t_PD.volume,
      v_US.name,
      v_US.exchange_code,
      v_US.asset_type,
      v_US.sector_code,
      ROW_NUMBER() OVER (
        PARTITION BY pd_symbol
        ORDER BY pd_time DESC
      ) AS row_num
    FROM tbl_price_data_1day t_PD
      JOIN viw_instrument_us_etfs v_US on t_PD.pd_symbol = v_US.symbol
    WHERE pd_time > now() - INTERVAL '30 days'
  )
SELECT symbol,
  name,
  exchange_code,
  asset_type,
  sector_code,
  AVG(volume) AS avg_volume_over_last_30_days
FROM tmp_latest_30_days_data
WHERE row_num <= 5
GROUP BY symbol,
  name,
  exchange_code,
  asset_type,
  sector_code
HAVING AVG(volume) > 50000
ORDER BY AVG(volume) DESC
LIMIT 50;



