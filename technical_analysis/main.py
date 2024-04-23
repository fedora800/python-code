import pandas as pd
from sqlalchemy import update, select, Table, MetaData, text

#import technical_analysis.mod_technical_indicators as m_ti
import mod_technical_indicators as m_ti
#from pkg_common import mod_others as m_oth
from pkg_common import mod_utils_db as m_udb
#from pkg_common import mod_yfinance as m_yfn

#benchmark_symbol_file = "/tmp/SPY.csv"
#benchmark_symbol_file = "c:\\mytmp\\downloads\\SPY.csv"
benchmark_symbol = "SPY"
symbol="TSLA"
#symbol_file = "/tmp/MSFT.csv"
#symbol="AAPL"
#symbol_file = "c:\\mytmp\\downloads\\AAPL.csv"
my_db_uri = "postgresql://postgres:Inesh#2012@localhost:5432/dbs_invest"
#my_db_uri = "postgresql://postgres:postgres@localhost:5432/dbs_invest"
fetch_from="table"


if fetch_from == "file":
  # --- fetch from csv file ---
  print(f"Symbol = {symbol} and csvfile = {symbol_file}")
  df_symbol = pd.read_csv(symbol_file)
  df_symbol.drop(columns=["Open", "High", "Low", "Volume"], inplace=True)
  df_symbol['Date'] = pd.to_datetime(df_symbol['Date'])     # convert Date to a datetime object
  df_symbol.rename(columns={'Symbol': 'symbol', 'Close': 'close'}, inplace=True)
  print(f"changed df = {df_symbol.tail(3)}")
  df_benchmark_symbol = pd.read_csv(benchmark_symbol_file)
  df_benchmark_symbol['Date'] = pd.to_datetime(df_benchmark_symbol['Date'])     # convert Date to a datetime object
  print(f"BENCHMARK = {benchmark_symbol} and df = {df_benchmark_symbol.tail(3)}")
elif fetch_from == "table":
  # --- fetch from csv file ---
  print(f"connecting to db with conn string = {my_db_uri}")
  engine = m_udb.fn_create_database_engine_sqlalchemy(my_db_uri)
  print(engine)
  sql_query = text("""select * from tbl_price_data_1day where pd_symbol= :param""").bindparams(param=symbol)
  df_symbol = m_udb.run_conn_sql_query(engine, sql_query)
  sql_query = text("""select * from tbl_price_data_1day where pd_symbol= :param""").bindparams(param=benchmark_symbol)
  df_benchmark_symbol = m_udb.run_conn_sql_query(engine, sql_query)
  #print(df_symbol)

# -----------------------------------------------------
# print("---- IND 01 ---- RSI ----")
# df_return = m_ti.fn_relative_strength_indicator(df_symbol)
# #fn_02_comparative_relative_strength_CRS_indicator(benchmark_symbol: str, df_benchmark_symbol: pd.DataFrame, symbol: str, df_symbol: pd.DataFrame) -> pd.DataFrame:
# #df_symbol.to_sql(name="tbl_price_data_1day", con=engine, if_exists="append", index=False)

# #     pd_symbol   pd_time    open   high     low   close     volume ema_5  ema_13  sma_50  sma_200  rsi_14

# ps_last_row = df_return.iloc[-1]
# #  where pd_symbol = df/symbol and pd_time = df/time and close = df/close
# print(f"---ps_last_row={ps_last_row}-----")
# lr_symbol = ps_last_row["pd_symbol"]
# lr_pd_time = ps_last_row["pd_time"]
# lr_close = ps_last_row["close"]
# lr_rsi_14 = ps_last_row["rsi_14"]

# print(f"==out== lr_symbol={lr_symbol} lr_pd_time={lr_pd_time} lr_close={lr_close} lr_rsi_14={lr_rsi_14} ===")

# print("---- IND 02 ---- MACD ----")
# df_return = m_ti.fn_macd_indicator(df_symbol, "macd_sig_hist")
# ps_last_row = df_return.iloc[-1]
# print(f"---ps_last_row={ps_last_row}-----")
# lr_symbol = ps_last_row["pd_symbol"]
# lr_pd_time = ps_last_row["pd_time"]
# lr_close = ps_last_row["close"]
# lr_macd_sig_hist = ps_last_row["macd_sig_hist"]
# print(f"==out== lr_symbol={lr_symbol} lr_pd_time={lr_pd_time} lr_close={lr_close} lr_macd_sig_hist={lr_macd_sig_hist}===")


# print("---- IND 03 ---- CRS ----")
# sql_query = text("""select * from tbl_price_data_1day where pd_symbol= :param""").bindparams(param="SPY")
# df_benchmark_symbol = m_udb.run_conn_sql_query(engine, sql_query)
# df_return = m_ti.fn_comparative_relative_strength_CRS_indicator(benchmark_symbol, df_benchmark_symbol, symbol, df_symbol, "crs")
# ps_last_row = df_return.iloc[-1]
# print(f"---ps_last_row={ps_last_row}-----")
# lr_symbol = ps_last_row["pd_symbol"]
# lr_pd_time = ps_last_row["pd_time"]
# lr_close = ps_last_row["close"]
# lr_crs = ps_last_row["crs"]
# print(f"==out== lr_symbol={lr_symbol} lr_pd_time={lr_pd_time} lr_close={lr_close} lr_crs={lr_crs}===")


# print("---- IND 04 ---- ADX ----")
# df_return = m_ti.fn_adx_indicator(df_symbol, "dm_dp_adx")
# ps_last_row = df_return.iloc[-1]
# print(f"---ps_last_row={ps_last_row}-----")
# lr_symbol = ps_last_row["pd_symbol"]
# lr_pd_time = ps_last_row["pd_time"]
# lr_close = ps_last_row["close"]
# lr_dm_dp_adx = ps_last_row["dm_dp_adx"]
# print(f"==out== lr_symbol={lr_symbol} lr_pd_time={lr_pd_time} lr_close={lr_close} lr_dm_dp_adx={lr_dm_dp_adx}===")
# -----------------------------------------------------

lst_tmp_symbols = [
  "AGBP.L",
  "EMGU.L",
  "EMIM.L"
#
#  "EXCS.L",
#  "IASH.L",
#  "IBTG.L",
#  "IBTL.L",
#  "IDTG.L",
#  "IGLT.L",
#  "IGTM.L",
#  "IIND.L",
#  "INRG.L",
#  "ISF.L",
#  "ITPG.L",
#  "IUKP.L",
#  "IUSA.L",
#  "MIDD.L",
#  "VUSA.L",
#  "WQDS.L"
]

for loop_symbol in lst_tmp_symbols:
  print(f"--- X444--- Computing indicators for {loop_symbol} ----------")
#  df_return = m_ti.fn_compute_all_required_indicators(benchmark_symbol, df_benchmark_symbol, symbol, df_symbol)
#  m_yfn.sync_price_data_in_table_for_symbol("YFINANCE", engine, loop_symbol)

  sql_query = text("""select * from tbl_price_data_1day where pd_symbol= :param""").bindparams(param=loop_symbol)
  df_loop_symbol = m_udb.run_conn_sql_query(engine, sql_query)
  df_return = m_ti.fn_compute_all_required_indicators(benchmark_symbol, df_benchmark_symbol, loop_symbol, df_loop_symbol)

  ps_last_row = df_return.iloc[-1]
  print("Inserting these values :", ps_last_row)
  
  # Assuming metadata is the metadata object used to create the table in the separate process
  metadata = MetaData()
  
  # Reflect the existing table from the database
  tbl_price_data_1day = Table('tbl_price_data_1day', metadata, autoload_with=engine)
  
  print("---200--- running UPDATE statement ----")
  
  # Create an update statement
  update_statement = (
      update(tbl_price_data_1day)
      .values(
          rsi_14=ps_last_row["rsi_14"],
          macd_sig_hist=ps_last_row["macd_sig_hist"],
          dm_dp_adx=ps_last_row["dm_dp_adx"],
          crs_50=ps_last_row["crs_50"]
      )
      .where(
          (tbl_price_data_1day.c.pd_symbol == ps_last_row["pd_symbol"]) &
          (tbl_price_data_1day.c.pd_time == ps_last_row["pd_time"]) &
          (tbl_price_data_1day.c.close == ps_last_row["close"])
      )
  )
  print("--------------update query=",str(update_statement))
  
  try:
      with engine.connect() as connection:
          result = connection.execute(update_statement)
          num_rows_updated = result.rowcount
          connection.commit()  # commit the changes
  
      if num_rows_updated > 0:
          print(f"Number of rows updated: {num_rows_updated}")
      else:
          print("No rows updated.")
  
  except Exception as e:
      print(f"Error during update: {e}")
  


print("---100--- now run a SELECT to verify if the cUPDATE statement has been applied on the table ----")
# Assuming tbl_price_data_1day is your SQLAlchemy Table object
select_statement = select(tbl_price_data_1day).where(
    (tbl_price_data_1day.c.pd_symbol == ps_last_row["pd_symbol"]) &
    (tbl_price_data_1day.c.pd_time == ps_last_row["pd_time"]) &
    (tbl_price_data_1day.c.close == ps_last_row["close"])
)

with engine.connect() as connection:
    result = connection.execute(select_statement)
    updated_row = result.fetchone()

if updated_row:
    print(f"Updated row: {updated_row}")
else:
    print("Row not found.")






