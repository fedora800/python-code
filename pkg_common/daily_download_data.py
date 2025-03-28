from datetime import datetime
import pandas as pd
from loguru import logger
import mod_yfinance as m_yfn
import mod_utils_db as m_udb
import mod_others as m_oth
from sqlalchemy import text


def main():
  m_oth.fn_set_logger(False)

  my_db_uri = "postgresql://postgres:postgres@localhost:5432/dbs_invest"
  #my_db_uri = "postgresql://postgres:Inesh#2012@localhost:5432/dbs_invest"
  sa_engine = m_udb.fn_create_database_engine_sqlalchemy(my_db_uri)
  logger.debug(my_db_uri)


  #lst_symbols = ['PLTR']            # test for 1 symbol
  #lst_symbols = ['SPY']
  # 25 largest S&P 500 index constituents by weighting
  #lst_symbols = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'TSLA', 'GOOG', 'BRK-B', 'META', 'UNH', 'XOM', 'LLY', 'JPM', 'JNJ', 'V', 'PG', 'MA', 'AVGO', 'HD', 'CVX', 'MRK', 'ABBV', 'COST', 'PEP', 'ADBE']
  #lst_symbols = ['META', 'TSLA', 'XOM']
  #lst_symbols = ['VMID.L','VUKE.L','VUSA.L']
  #lst_symbols = ['CSPX.L', 'EQQQ.L', 'IITU.L', 'ISF.L', 'SWDA.L', 'VHVG.L', 'VUAG.L', 'VUSA.L', 'VWRL.L', 'VWRP.L']

  # for SPY exclusively
  logger.info("First download and insert latest prices for benchmark SPY ...")
  df_ohlcv_symbol = m_yfn.fn_sync_price_data_in_table_for_symbol("YFINANCE", sa_engine, "SPY", pd.DataFrame())
  logger.debug(df_ohlcv_symbol)
  
  # now download and insert latest prices for our list of symbols
  logger.info("Now download and insert latest prices for our list of symbols ...")
  #dct_params = {}
  #sql_query = """select symbol from viw_instrument_us_sp500_constituents"""
  #dct_params = {"sympattern_1": "J%"}
  #sql_query = """select * from tbl_instrument where symbol like :sympattern_1"""
  #sql_query = """select * from viw_instrument_us_sp500_constituents where symbol like :sympattern_1"""
  #dct_params = {"sympattern_1": "[K-O]%"}
  #dct_params = {"sympattern_1": "[P-Z]%"}
  #sql_query = """select * from viw_instrument_us_sp500_constituents where symbol like :sympattern_1"""
  dct_params = {"sympattern_1": "I%"}
  sql_query = """select * from viw_instrument_in_us_top100_etfs_by_aum where symbol like :sympattern_1"""
  df_symbols= m_udb.fn_run_conn_sqlalchemy_query(sa_engine, sql_query, dct_params)
  df_symbols = df_symbols[["symbol"]]
  lst_symbols = df_symbols["symbol"].tolist()
  symbol_count = len(lst_symbols)
  logger.info("lst_symbols = {}", lst_symbols)

  # batch download data for multiple symbols in a single request
  start_date = datetime.strptime('2024-12-01', '%Y-%m-%d')
  df_prices_mult_symbols = m_yfn.fn_get_historical_data_multiple_symbols_single_request(lst_symbols, start_date)
  print(df_prices_mult_symbols.head())  # Display the first few rows
  df_prices_symbol = {}     # Dictionary to store individual DataFrames
  #for symbol in lst_symbols:
  for idx, symbol in enumerate(lst_symbols, start=1):     # loop with index and start index at 1
    print(""); print(f"------------- lst_symbols : FOR LOOP ({idx} of {symbol_count}) ------{symbol}------------------------")
    df_ohlcv_symbol = df_prices_mult_symbols[symbol].copy()    # Extract data for a single symbol
    print("df_ohlcv_symbol = ", df_ohlcv_symbol.head())
    print("Head for ", symbol, " df_ohlcv_symbol = ", df_ohlcv_symbol.head())
    if m_udb.fn_check_symbol_exists_in_instrument_table(sa_engine, symbol):
      wildcard_value_1 = symbol
      sql_query = "SELECT * FROM viw_price_data_stats_by_symbol WHERE symbol = :wildcard_value_1;"
      df_prices_from_db = m_udb.fn_get_symbol_price_data_stats_from_database(sa_engine, symbol)
      print("df_xx = ", df_prices_from_db)
      df_ohlcv_symbol = m_yfn.fn_sync_price_data_in_table_for_symbol("YFINANCE", sa_engine, symbol, pd.DataFrame())
      print(df_ohlcv_symbol)
    else:
      print("!!! SYMBOL NOT FOUND - ", symbol, "  !!! - skipping this lst_symbols loop..." )

# main
if __name__ == "__main__":
  main()
