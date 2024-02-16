from datetime import datetime

import mod_yfinance as m_yfn
import mod_utils_db as m_udb




def test_fn_get_historical_data_symbol_list(lst_symbols: list, write_to_file: bool):
  data_venue = "YFINANCE"
  start_date = datetime(2022, 1, 1)
  end_date = datetime(2022, 12, 31)




def main():
  data_venue = "YFINANCE"
  symbol="AAPL"
  FILE_EXTN ='.csv'
  start_date = datetime(2022, 1, 1)
  end_date = datetime(2022, 12, 31)

  #df = m_yfn.fn_get_historical_data_symbol(data_venue, symbol, start_date, end_date, True)


  # this will be the full S&P 500 index constituents list
  #csv_file_path = 'sp500_constituents.csv'  # Replace with the actual path to your CSV file
  # 25 largest S&P 500 index constituents by weighting
  # AAPL, MSFT, AMZN, NVDA, GOOGL, TSLA, GOOG, BRK-B, META, UNH, XOM, LLY, JPM, JNJ, V, PG, MA, AVGO, HD, CVX, MRK, ABBV, COST, PEP, ADBE
  #lst_symbols = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'TSLA', 'GOOG', 'BRK-B', 'META', 'UNH', 'XOM', 'LLY', 'JPM', 'JNJ', 'V', 'PG', 'MA', 'AVGO', 'HD', 'CVX', 'MRK', 'ABBV', 'COST', 'PEP', 'ADBE']
  #lst_symbols = ['META', 'TSLA', 'XOM']
  #lst_symbols = ['V3AB.L','V3AM.L','V3MB.L','V3MM.L','VAGP.L','VAGS.L','VALW.L','VAPX.L','VCPA.L','VDPG.L','VECP.L','VEGB.L','VEMT.L','VERG.L','VERX.L','VETY.L','VEUR.L','VEVE.L','VFEG.L','VFEM.L','VGER.L','VGOV.L','VGPA.L','VGVA.L','VHVG.L','VHYG.L','VHYL.L','VJPB.L','VJPN.L','VMID.L','VMIG.L','VNRG.L','VNRT.L','VPNG.L','VUAG.L','VUCP.L','VUKE.L','VUKG.L','VUSA.L','VUSC.L','VUTA.L','VUTY.L','VWRL.L','VWRP.L']
  #lst_symbols = ['VMID.L','VUKE.L','VUSA.L']
  #lst_symbols = ['SPY']
  #lst_symbols = ['CSPX.L', 'EQQQ.L', 'IITU.L', 'ISF.L', 'SWDA.L', 'VHVG.L', 'VUAG.L', 'VUSA.L', 'VWRL.L', 'VWRP.L']
  #m_yfn.fn_get_historical_data_list_of_symbols(data_venue, lst_symbols, start_date, end_date, True)

  my_db_uri = "postgresql://postgres:Inesh#2012@localhost:5432/dbs_invest"
  engine = m_udb.fn_create_database_engine_sqlalchemy(my_db_uri)
  m_yfn.fn_sync_price_data_in_table_for_symbol("YFINANCE", engine, "VWRL.L")



# main
if __name__ == "__main__":
  main()
