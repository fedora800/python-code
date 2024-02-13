from datetime import datetime

import mod_yfinance as m_yf



def test_fn_get_historical_data_1_symbol(symbol: str, write_to_file: bool):
  """
  Tests the function fn_get_historical_data_symbol()

  """
  

  FILE_EXTN ='.csv'

  df = m_yf.fn_get_historical_data_symbol(data_venue, symbol, start_date, end_date, write_to_file)


def test_fn_get_historical_data_symbol_list(lst_symbols: list, write_to_file: bool):
  data_venue = "YFINANCE"
  start_date = datetime(2022, 1, 1)
  end_date = datetime(2022, 12, 31)




def main():
  data_venue = "YFINANCE"
  start_date = datetime(2022, 1, 1)
  end_date = datetime(2022, 12, 31)
  test_fn_get_historical_data_1_symbol('AAPL', True)
  df = m_yf.fn_get_historical_data_symbol("YFINANCE", "AAPL", start_date, end_date, True)

  lst_symbols = ['CSPX.L', 'EQQQ.L', 'IITU.L', 'ISF.L', 'SWDA.L', 'VHVG.L', 'VUAG.L', 'VUSA.L', 'VWRL.L', 'VWRP.L']
  test_fn_get_historical_data_symbol_list(lst_symbols, True)


# main
if __name__ == "__main__":
  main()