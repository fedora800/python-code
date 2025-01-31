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
  # this will be the full S&P 500 index constituents list
  #csv_file_path = 'sp500_constituents.csv'  # Replace with the actual path to your CSV file
  # 25 largest S&P 500 index constituents by weighting
  # AAPL, MSFT, AMZN, NVDA, GOOGL, TSLA, GOOG, BRK-B, META, UNH, XOM, LLY, JPM, JNJ, V, PG, MA, AVGO, HD, CVX, MRK, ABBV, COST, PEP, ADBE
  #lst_symbols = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'TSLA', 'GOOG', 'BRK-B', 'META', 'UNH', 'XOM', 'LLY', 'JPM', 'JNJ', 'V', 'PG', 'MA', 'AVGO', 'HD', 'CVX', 'MRK', 'ABBV', 'COST', 'PEP', 'ADBE']
  #lst_symbols = ['META', 'TSLA', 'XOM']
  #lst_symbols = ['VMID.L','VUKE.L','VUSA.L']
  lst_symbols = ['AAL','AAPL','COF']
  #lst_symbols = ['CSPX.L', 'EQQQ.L', 'IITU.L', 'ISF.L', 'SWDA.L', 'VHVG.L', 'VUAG.L', 'VUSA.L', 'VWRL.L', 'VWRP.L']

  # UK ETFs most-active list
  # lst_symbols = ('3KWE.L', '3LNG.L', '3NGL.L', '3SNV.L', '3UKS.L', 'AGGU.L', 'CNYA.L', 'CSPX.L', 'DHYA.L', 'DS2P.L', 'DTLA.L', 'FLOA.L', 'HCHS.L', 'IB01.L', \
  #   'IBTA.L', 'IDTL.L', 'IHYA.L', 'IMBA.L', 'IUAA.L', 'IUVL.L', 'JGRE.L', 'JMRE.L', 'JPEA.L', 'LGUG.L', 'LNGA.L', \
  #   'PAJP.L', 'RIEU.L', 'SAEM.L', 'SDIA.L', 'SPL3.L', 'SUK2.L', 'SUOE.L', 'SUSM.L', 'V3AA.L', 'V3AB.L', 'V3AM.L', 'V3MB.L', 'VALW.L', 'VERX.L', 'VEVE.L', \
  #   'VFEM.L', 'VHVG.L', 'VHYL.L', 'VILX.L', 'VIXL.L', 'VJPN.L', 'VMID.L', 'VUAG.L', 'VUKG.L', 'VWRL.L', 'VWRP.L')

  #m_yfn.fn_get_historical_data_list_of_symbols(data_venue, lst_symbols, start_date, end_date, True)    # this puts into a csv file
  #df_ohlcv_symbol = m_yfn.fn_sync_price_data_in_table_for_symbol("YFINANCE", engine, "VWRL.L")

  # sql_query = text("""select symbol from viw_instrument_in_us_top100_etfs_by_aum where symbol like 'I%'""")
  # df_symbols = pd.read_sql_query(sql_query, db_conn)
  # logger.debug(df_symbols)
  # print(df_symbols)
  # lst_symbols = df_symbols["symbol"].tolist()
  # for symbol in lst_symbols:
  #   #print(""); print("---------------------FOR LOOP ------", symbol, " -------------------------------------")
  #   logger.info(""); logger.info("---------------------FOR LOOP ------------- {} ----------------", symbol)
  #   df_ohlcv_symbol = m_yfn.fn_sync_price_data_in_table_for_symbol("YFINANCE", db_conn, symbol)
  #   #print(df_ohlcv_symbol)

  # for SPY exclusively
  df_ohlcv_symbol = m_yfn.fn_sync_price_data_in_table_for_symbol("YFINANCE", sa_engine, "SPY")
  print("----11111--for SPY----", df_ohlcv_symbol)
  
  
# main
if __name__ == "__main__":
  main()
