

$ PGPASSWORD=postgres psql -U postgres -h localhost -d dbs_invest


--------------------------------------------------------------------------------
---- INSTRUMENT RELATED ----
select * from tbl_instrument;
select count(*) from tbl_instrument;

select * from tbl_instrument 
where 
--symbol like '%RS%' and note_1='SP500';
--symbol in ('CSPX.L', 'EQQQ.L', 'IITU.L', 'ISF.L', 'SWDA.L', 'VHVG.L', 'VUAG.L', 'VUSA.L', 'VWRL.L', 'VWRP.L') 
symbol in ('SPY', 'VWRL.L', 'VUSA.L', 'HACK')
--and country_code='UK'

select exchange_code, count(*) from tbl_instrument
group by exchange_code;

select country_code, exchange_code, asset_type, note_1, data_source, deleted, count(*) 
from tbl_instrument
--where 
--country_code='UK' 
group by country_code, exchange_code, asset_type, note_1, data_source, deleted;

delete from tbl_instrument 
where 
--data_source='THINKORSWIM'
--symbol like '%RS%' and note_1='SP500';

--  SELECT * FROM tbl_instrument WHERE exchange_code='LSE' and asset_type='ETF';
select * from viw_instrument_uk_equities
where symbol like 'B%'
order by symbol

update tbl_instrument
set 
--note_1='MOST-ACTIVE;'
country_code='UK' 
where
exchange_code='LSE'
and data_source='INVESTING-COM'
and data_source='TRADING212'
and symbol in (
'VWRL.L', 'VERX.L', 'V3AB.L', 'VHVG.L', 'VUAG.L', 'VWRP.L', 'VMID.L', 'VEVE.L',
'VFEM.L', 'VHYL.L', 'VJPN.L', 'V3AM.L', 'VUKG.L', 'VALW.L', 'V3MB.L'
)


--------------------------------------------------------------------------------
---- PRICE DATA RELATED ----

select pd_symbol, min(pd_time), max(pd_time), count(*)
from tbl_price_data_1day
where
--sma_200 is null
--rsi_14 is not null
--where sma_200 is null
--pd_symbol like 'A%'
pd_symbol in ('SPY', 'VWRL.L', 'VUSA.L', 'HACK')
--AND pd_symbol in (select symbol from tbl_instrument where exchange_code='LSE')
group by pd_symbol
order by pd_symbol;


select * from viw_price_data_stats_by_symbol
where
symbol in (
--'V3AB.L','V3AM.L','V3MB.L','V3MM.L','VAGP.L'
'CSPX.L', 'EQQQ.L', 'IITU.L', 'ISF.L', 'SWDA.L', 'VHVG.L', 'VUAG.L', 'VUSA.L', 'VWRL.L', 'VWRP.L'
);

--select * from tbl_price_data_1day 
select pd_symbol, pd_time, close, rsi_14, macd_sig_hist, dm_dp_adx, crs_50
from tbl_price_data_1day
where 
pd_symbol='VWRL.L'
--and pd_time between '2023-05-01' and '2023-07-01'
order by pd_time DESC
limit 20;

delete from tbl_price_data_1day 
where 
pd_symbol='VWRL.L'
--AND pd_time < NOW() - INTERVAL '30 days';  --older
AND pd_time > NOW() - INTERVAL '30 days';   --newer

delete from tbl_price_data_1day where pd_symbol in (select symbol from tbl_instrument where asset_type='STOCK' and symbol like '%RS%' and note_1='SP500');

delete from tbl_price_data_1day 
where pd_symbol ='WQDS.L'
and pd_time = '2023-11-16' 

#truncate table tbl_price_data_1day;

select * from tbl_price_data_1day 
where 
pd_symbol IN ('VUSA.L', 'IUKP.L') 
and pd_time > '2024-02-06' 
order by pd_time desc;


select * from viw_latest_price_data_by_symbol 
where pd_symbol in ( 
 'AGBP.L',
  'EMGU.L',
  'EMIM.L'
)
-- and pd_time > '2024-02-06' order by pd_time desc;



INSERT INTO tbl_price_data_1day (
  pd_symbol, pd_time, open, high, low, close, volume, ema_5, ema_13, sma_50, sma_200, rsi_14
)
SELECT
  pd_symbol, 
  pd_time + INTERVAL '1 day', -- Increment the date by 1 day
  open,   high,   low,   close,   volume,   ema_5,   ema_13,   sma_50,   sma_200,   rsi_14
FROM
  tbl_price_data_1day
WHERE
  pd_symbol = 'SPY' -- Replace with the specific symbol you are interested in
ORDER BY
  pd_time DESC
LIMIT 1;



--- NEED TO CREATE VIEW BELOW I THINK FOR THE SCAN ---

select * from viw_latest_price_data_by_symbol 
where 
pd_time > CURRENT_DATE - INTERVAL '3 days'
and close > sma_50
and pd_symbol in (select pd_symbol from viw_latest_price_data_by_symbol)
order by pd_time desc;

CREATE OR REPLACE VIEW viw_tmp_001 AS
  select pd_symbol,
    name,
    DATE(pd_time) as price_date,
    close,
    ema_13,
    sma_50,
    volume,
    sector
  from viw_latest_price_data_by_symbol
  where pd_time > CURRENT_DATE - INTERVAL '4 days'
    and close > sma_50
    and pd_symbol in (
      select symbol from viw_instrument_uk_equities
      where note_1 is not null    
	)
  order by pd_symbol;


update tbl_instrument
set note_1 = 'MOST-ACTIVE;'
where
symbol in 
('3KWE.L', '3LNG.L', '3NGL.L', '3SNV.L', '3UKS.L', 'AGGU.L', 'CNYA.L', 'CSPX.L', 'DHYA.L', 'DS2P.L', 'DTLA.L', 'FLOA.L', 'HCHS.L', 'IB01.L', 'IBTA.L', 'IDTL.L', 'IHYA.L', 'IMBA.L', 'ISLQDA.L', 'ISMIDD.L', 'ISNDIA.L', 'IUAA.L', 'IUVL.L', 'JGRE.L', 'JMRE.L', 'JPEA.L', 'LGUG.L', 'LNGA.L', 'PAJP.L', 'RIEU.L', 'SAEM.L', 'SDIA.L', 'SPL3.L', 'SUK2.L', 'SUOE.L', 'SUSM.L', 'V3AA.L', 'V3AB.L', 'V3AM.L', 'V3MB.L', 'VALW.L', 'VERX.L', 'VEVE.L', 'VFEM.L', 'VHVG.L', 'VHYL.L', 'VILX.L', 'VIXL.L', 'VJPN.L', 'VMID.L', 'VUAG.L', 'VUKG.L', 'VWRL.L', 'VWRP.L');

update tbl_instrument set country_code='UK' where country_code is null and exchange_code='LSE' and asset_type='ETF' and note_1 like '%MOST-ACTIVE%';


--------------------------------------------------------------------------------

\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM' ~/git-projects/python-code/timescaledb/tbl_price_data_1day_data.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/AAPL.csv' DELIMITER ',' CSV HEADER;

--------------------------------------------------------------------------------
postgres=# SELECT name, setting FROM pg_settings WHERE setting LIKE '/%';
          name           |                 setting
-------------------------+-----------------------------------------
 config_file             | /etc/postgresql/14/main/postgresql.conf
 data_directory          | /var/lib/postgresql/14/main
 external_pid_file       | /var/run/postgresql/14-main.pid
 hba_file                | /etc/postgresql/14/main/pg_hba.conf
 ident_file              | /etc/postgresql/14/main/pg_ident.conf
 ssl_cert_file           | /etc/ssl/certs/ssl-cert-snakeoil.pem
 ssl_key_file            | /etc/ssl/private/ssl-cert-snakeoil.key
 stats_temp_directory    | /var/run/postgresql/14-main.pg_stat_tmp
 unix_socket_directories | /var/run/postgresql

--------------------------------------------------------------------------------
