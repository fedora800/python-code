

$ PGPASSWORD=postgres psql -U postgres -h localhost -d dbs_invest


--------------------------------------------------------------------------------

select * from tbl_instrument;
select count(*) from tbl_instrument;

select * from tbl_instrument 
where 
symbol like '%RS%' and note_1='SP500';

select exchange_code, count(*) from tbl_instrument
group by exchange_code;

select exchange_code, asset_type, note_1, data_source, count(*) 
from tbl_instrument
group by exchange_code, asset_type, note_1, data_source;

delete from tbl_instrument 
where 
--data_source='THINKORSWIM'
--symbol like '%RS%' and note_1='SP500';

--  SELECT * FROM tbl_instrument WHERE exchange_code='LSE' and asset_type='ETF';
select * from viw_instrument_uk_equities
where symbol like 'B%'
order by symbol


--------------------------------------------------------------------------------

select pd_symbol, min(pd_time), max(pd_time), count(*)
from tbl_price_data_1day
where
--sma_200 is null
--rsi_14 is not null
--where sma_200 is null
--pd_symbol like 'A%'
pd_symbol in ('SPY', 'MCO')
--AND pd_symbol in (select symbol from tbl_instrument where exchange_code='LSE')
group by pd_symbol
order by pd_symbol;

select * from tbl_price_data_1day where pd_symbol='META'
order by pd_time DESC;

delete from tbl_price_data_1day 
where 
pd_symbol='META'
--AND pd_time < NOW() - INTERVAL '30 days';  --older
AND pd_time > NOW() - INTERVAL '30 days';   --newer

delete from tbl_price_data_1day where pd_symbol in (select symbol from tbl_instrument where asset_type='STOCK' and symbol like '%RS%' and note_1='SP500');

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


--- NEED TO CREATE VIEW BELOW I THINK FOR THE SCAN ---

select * from viw_latest_price_data_by_symbol 
where 
pd_time > CURRENT_DATE - INTERVAL '3 days'
and close > sma_50
and pd_symbol in (select pd_symbol from viw_latest_price_data_by_symbol)
order by pd_time desc;


CREATE OR REPLACE VIEW viw_tmp_001 AS 
  select * from viw_latest_price_data_by_symbol 
  where 
  pd_time > CURRENT_DATE - INTERVAL '3 days'
  and close > sma_50
  and pd_symbol in (select pd_symbol from viw_latest_price_data_by_symbol)
  order by pd_time desc;




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
