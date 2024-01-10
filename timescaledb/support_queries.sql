
--------------------------------------------------------------------------------

select * from tbl_instrument;
select count(*) from tbl_instrument;

--------------------------------------------------------------------------------

select pd_symbol, min(pd_time), max(pd_time), count(*) 
from tbl_price_data_1day 
--where sma_200 is null
group by pd_symbol;

select * from tbl_price_data_1day where pd_symbol='META';

delete from tbl_price_data_1day where pd_symbol='META';

#truncate table tbl_price_data_1day;

--------------------------------------------------------------------------------

\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM' ~/git-projects/python-code/timescaledb/tbl_price_data_1day_data.csv' DELIMITER ',' CSV HEADER;
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/AAPL.csv' DELIMITER ',' CSV HEADER;

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
