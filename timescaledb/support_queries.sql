

select * from tbl_instrument;
select count(*) from tbl_instrument;

--------------------------------------------------------------------------------

select pd_symbol, min(pd_time), max(pd_time), count(*) 
from tbl_price_data_1day 
group by pd_symbol;

#truncate table tbl_price_data_1day;

--------------------------------------------------------------------------------

\copy tbl_price_data_1day (pd_time,pd_symbol,close,high,low,open,volume) FROM '~/git-projects/python-code/timescaledb/tbl_price_data_1day_data.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,close,high,low,open,volume) FROM '~/git-projects/python-code/AAPL.csv' DELIMITER ',' CSV HEADER;

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
