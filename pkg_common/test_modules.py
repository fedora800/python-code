from datetime import datetime
import pandas as pd
import sqlalchemy as sa
import certifi
import os
import mod_yfinance as m_yfn
import mod_utils_db as m_udb
import mod_others as m_oth


def test_fn_download_historical_data_for_symbol(symbol):
  data_venue = "YFINANCE"
  file_extn ='.csv'
  start_date = datetime(2021, 1, 1)
  end_date = datetime(2023, 12, 31)

  df = m_yfn.fn_download_historical_data_for_one_symbol(data_venue, symbol, start_date, end_date, True)
  filename=symbol + file_extn
  df.to_csv(filename, index=False)
  print(f"Created csv file from downloaded date - {filename}")
  


def test_fn_download_and_sync_db_loop_for_mult_symbols(sa_engine, session):
  # this will be the full S&P 500 index constituents list
  #csv_file_path = 'sp500_constituents.csv'  # Replace with the actual path to your CSV file
  # 25 largest S&P 500 index constituents by weighting
  # AAPL, MSFT, AMZN, NVDA, GOOGL, TSLA, GOOG, BRK-B, META, UNH, XOM, LLY, JPM, JNJ, V, PG, MA, AVGO, HD, CVX, MRK, ABBV, COST, PEP, ADBE
  #lst_symbols = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'TSLA', 'GOOG', 'BRK-B', 'META', 'UNH', 'XOM', 'LLY', 'JPM', 'JNJ', 'V', 'PG', 'MA', 'AVGO', 'HD', 'CVX', 'MRK', 'ABBV', 'COST', 'PEP', 'ADBE']
  lst_symbols = ['META', 'TSLA', 'XOM']
  #lst_symbols = ['VMID.L','VUKE.L','VUSA.L']
  #lst_symbols = ['XOM']            # test for 1 symbol
  #lst_symbols = ['SPY']
  #lst_symbols = ['CSPX.L', 'EQQQ.L', 'IITU.L', 'ISF.L', 'SWDA.L', 'VHVG.L', 'VUAG.L', 'VUSA.L', 'VWRL.L', 'VWRP.L']
  #lst_symbols = ['DGRO', 'IAU', 'IBIT', 'IEF']
  # UK ETFs most-active list
  # lst_symbols = ('3KWE.L', 'AGGU.L', 'CNYA.L', 'CSPX.L', 'DHYA.L', 'DS2P.L', 'DTLA.L', 'FLOA.L', 'HCHS.L', 'IB01.L', \
  #    'IBTA.L', 'IDTL.L', 'IHYA.L', 'IMBA.L', 'IUAA.L', 'IUVL.L', 'JGRE.L', 'JMRE.L', 'JPEA.L', 'LGUG.L', \
  #    'PAJP.L', 'RIEU.L', 'SAEM.L', 'SDIA.L', 'SPL3.L', 'SUK2.L', 'SUOE.L', 'SUSM.L', 'V3AA.L', 'V3AB.L', 'V3AM.L', 'V3MB.L', 'VALW.L', 'VERX.L', 'VEVE.L', \
  #    'VFEM.L', 'VHVG.L', 'VHYL.L', 'VILX.L', 'VIXL.L', 'VJPN.L', 'VMID.L', 'VUAG.L', 'VUKG.L', 'VWRL.L', 'VWRP.L')

  # temp - part of above list
  # lst_symbols = ('SUOE.L', 'SUSM.L', 'V3AA.L', 'V3AB.L', 'V3AM.L', 'V3MB.L', 'VALW.L', 'VERX.L', 'VEVE.L', \
  #   'VFEM.L', 'VHVG.L', 'VHYL.L', 'VILX.L', 'VIXL.L', 'VJPN.L', 'VMID.L', 'VUAG.L', 'VUKG.L', 'VWRL.L', 'VWRP.L')

  #m_yfn.fn_get_historical_data_list_of_symbols(data_venue, lst_symbols, start_date, end_date, True)    # this puts into a csv file
  #df_ohlcv_symbol = m_yfn.fn_sync_price_data_in_table_for_symbol("YFINANCE", engine, "VWRL.L")
  
  for symbol in lst_symbols:
    print(""); print("---------------------FOR LOOP ------", symbol, " -------------------------------------")
    if m_udb.fn_check_symbol_exists_in_instrument_table(sa_engine, symbol):
      df_ohlcv_symbol = m_yfn.fn_sync_price_data_in_table_for_symbol("YFINANCE", sa_engine, symbol)
      #print(df_ohlcv_symbol)
    else:
      print("!!! SYMBOL NOT FOUND - ", symbol, "  !!! - skipping ..." )

  # for SPY exclusively
  #df_ohlcv_symbol = m_yfn.fn_sync_price_data_in_table_for_symbol("YFINANCE", sa_engine, "SPY")
  #print("----11111--for SPY----", df_ohlcv_symbol)

  # # batch download data for multiple symbols in a single request
  # start_date = '2024-12-01'
  # df_multi = m_yfn.fn_get_historical_data_multiple_symbols_single_request(lst_symbols, start_date, session)
  # print(df_multi.head())  # Display the first few rows
  # symbol_dfs = {}     # Dictionary to store individual DataFrames
  # for symbol in lst_symbols:
  #   print(f"\n---------------------- {symbol} ----------------------")
  #   df_ohlcv_symbol = df_multi[symbol].copy()    # Extract data for a single symbol
  #   symbol_dfs[symbol] = df_ohlcv_symbol
  #   print(f"Head for {symbol}: \n", df_ohlcv_symbol.head())
  #   wildcard_value_1 = symbol
  #   sql_query = "SELECT * FROM viw_price_data_stats_by_symbol WHERE symbol = :wildcard_value_1;"
  #   df_xx = m_udb.fn_get_symbol_price_data_stats_from_database(sa_engine, symbol)
  #   print("df_xx = ", df_xx)
  


def main():
  m_oth.fn_set_logger(False)
  #m_oth.fn_set_logger(True)

  os.environ["SSL_CERT_FILE"] = certifi.where()

  my_db_uri = "postgresql://postgres:postgres@localhost:5432/dbs_invest"
  #my_db_uri = "postgresql://postgres:Inesh#2012@localhost:5432/dbs_invest"
  sa_engine = m_udb.fn_create_database_engine_sqlalchemy(my_db_uri)

  session_nossl = m_yfn.fn_disable_session_for_ssl()
  #m_yfn.get_data_without_using_ssl('IUSB')
  #m_yfn.get_stock_info('IBM')
  #test_fn_download_historical_data_for_symbol('AAPL')
  test_fn_download_and_sync_db_loop_for_mult_symbols(sa_engine, session_nossl)

  # wildcard_value_1 = "%IU%"
  # wildcard_value_2 = "%SB%"
  # sql_query = "SELECT * FROM viw_instrument_in_us_top100_etfs_by_aum WHERE symbol LIKE :param1 OR symbol LIKE :param2;"
  # dct_params = {"param1": wildcard_value_1, "param2": wildcard_value_2}
  # df_symbols= m_udb.fn_run_conn_sqlalchemy_query(sa_engine, sql_query, dct_params)
  # df_symbols = df_symbols[["symbol"]]
  # lst_symbols = df_symbols["symbol"].tolist()
  # print("---xxx---", lst_symbols)
  # for symbol in lst_symbols:
  #   print(""); print("---------------------FOR LOOP ------", symbol, " -------------------------------------")
  #   df_ohlcv_symbol = m_yfn.fn_sync_price_data_in_table_for_symbol("YFINANCE", sa_engine, symbol)


# main
if __name__ == "__main__":
  main()
