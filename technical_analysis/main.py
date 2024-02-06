import pandas as pd
import mod_technical_indicators as m_ti
#from pkg_common import mod_utils_db as m_udb
import mod_utils_db as m_udb
from sqlalchemy import text


#benchmark_symbol_file = "/tmp/SPY.csv"
#benchmark_symbol = "SPY"
#symbol="MSFT"
#symbol_file = "/tmp/MSFT.csv"
symbol="AAPL"
symbol_file = "c:\\mytmp\\downloads\\AAPL.csv"
my_db_uri = "postgresql://postgres:postgres@localhost:5432/dbs_invest"
fetch_from="table"

#df_benchmark_symbol = pd.read_csv(benchmark_symbol_file)
#df_benchmark_symbol['Date'] = pd.to_datetime(df_benchmark_symbol['Date'])     # convert Date to a datetime object
#print(f"BENCHMARK = {benchmark_symbol} and df = {df_benchmark_symbol.tail(3)}")

if fetch_from == "file":
  # --- fetch from csv file ---
  print(f"Symbol = {symbol} and csvfile = {symbol_file}")
  df_symbol = pd.read_csv(symbol_file)
  df_symbol.drop(columns=["Open", "High", "Low", "Volume"], inplace=True)
  df_symbol['Date'] = pd.to_datetime(df_symbol['Date'])     # convert Date to a datetime object
  df_symbol.rename(columns={'Symbol': 'symbol', 'Close': 'close'}, inplace=True)
  print(f"changed df = {df_symbol.tail(3)}")
elif fetch_from == "table":
  # --- fetch from csv file ---
  print(f"connecting to db with conn string = {my_db_uri}")
  db_conn = m_udb.create_database_engine_sqlalchemy(my_db_uri)
  print(db_conn)
  sql_query = text("""select * from tbl_price_data_1day where pd_symbol= :param""").bindparams(param="AAPL")
  df_symbol = m_udb.run_conn_sql_query(db_conn, sql_query)
  #print(df_symbol)

m_ti.fn_01_relative_strength_indicator(df_symbol)
#fn_02_comparative_relative_strength_CRS_indicator(benchmark_symbol: str, df_benchmark_symbol: pd.DataFrame, symbol: str, df_symbol: pd.DataFrame) -> pd.DataFrame:
df_symbol.to_sql(name="tbl_price_data_1day", con=db_conn, if_exists="append", index=False)
