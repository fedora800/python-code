
# https://pypi.org/project/yfinance/
# https://analyzingalpha.com/yfinance-python

import sys
import platform
import time
import requests


from loguru import logger
import yfinance as yf
import pandas as pd
import csv
from requests.exceptions import HTTPError
from datetime import datetime, timedelta


if platform.system() == "Windows":
  #logger.debug("mod_yfinance.py - Running on Windows")
  sys.path.append("H:\\git-projects\\python-code")
  sys.path.append("H:\\git-projects\\python-code\\streamlit_code")
elif platform.system() == "Linux":
  #logger.debug("mod_yfinance.py - Running on Linux")
  sys.path.append("~/git-projects/python-code")
  sys.path.append("~/git-projects/python-code/streamlit_code")
  sys.path.append("/home/cloud_user/git-projects/python-code/streamlit_code")
else:
  print("Operating system not recognized")

#logger.debug(sys.path)

import mod_utils_db as m_udb
import mod_utils_date as m_udt
import mod_others as m_oth
#from sqlalchemy import text


def read_csv_into_list(file_path, has_header=True):
  """
  Read a CSV file and store its contents in a list.

  Parameters:
  - file_path (str): The path to the CSV file.
  - has_header (bool, optional): Specify if the CSV file has a header row. Defaults to True.

  Returns:
  list: A list containing rows from the CSV file.
  """

  lst_symbols = []

  with open(file_path, 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    # Skip the header row if present
    if has_header:
      next(csvreader)

    # Iterate over rows and append them to the list
    for row in csvreader:
      if row:  # Check if the row is not empty
          col_1 = row[0]
          lst_symbols.append(col_1)
      # lst_csv_data.append(row)
      #lst_symbols.extend(row)  # single-column file so we just extend the value into the list

  return lst_symbols



def fn_download_historical_data_for_one_symbol(data_venue: str, symbol: str, start_date: datetime, end_date: datetime, write_to_file: bool) -> pd.DataFrame:
  """
  Retrieves historical data for just a single symbol from a data venue.

  Parameters:
  - data_venue (str): The string representing the data venue.
  - symbol (str): The symbol for whom we want to download data
  - start_date (datetime): The start date for the historical data.
  - end_date (datetime): The end date for the historical data.

  Returns:
  Any: pandas dataframe

  Example:
  >>> get_historical_data_symbol("YFINANCE", "AAPL", datetime(2022, 1, 1), datetime(2022, 12, 31))
  """

  #data_venue = "YFINANCE"
  # symbol = df.at[0,"pd_symbol"]
  # oldest_price_date = df.at[0,"oldest_rec_pd_time"]
  # latest_price_date = df.at[0,"latest_rec_pd_time"]
  logger.debug("---------- fn_download_historical_data_for_symbol ---- STARTED ----------")
  logger.debug("Received arguments : data_venue={} symbol={} start_date={} end_date={} write_to_file={}", data_venue, symbol, start_date, end_date, write_to_file)

  # # Convert the date strings to datetime objects and zero out time component
  # start_date = oldest_price_date.replace(hour=0, minute=0, second=0, microsecond=0)
  # #latest_price_date = pd.to_datetime(latest_price_date)
  # end_date = latest_price_date.replace(hour=0, minute=0, second=0, microsecond=0)

#  # do not re-download data that already exists
#  next_day = latest_price_date + timedelta(days=1)      # just start from the next day of the latest price date
#  if not oldest_price_date:
#    start_date = next_day.replace(tzinfo=timezone.utc)    # get till yesterday
#  end_date = datetime.now() - timedelta(days=1)

  logger.info("Downloading from Data Venue {} for symbol={} start_date={} end_date={}", data_venue, symbol, start_date, end_date)
  #logger.info("Downloading from {} for symbol={} start_date={} end_date={}", data_venue, symbol, oldest_price_date, latest_price_date)
  tm_before_download = time.time()

  try:
    session = requests.Session()
    session.verify = False  # Disable SSL verification 
    logger.warning("Disabling SSL Verification and downloading ...")
    df_prices = yf.download(symbol, start=start_date, end=end_date, rounding=True, session=session)
    # yf.download() does not raise exceptions – Instead, it prints errors to the console and returns an empty DataFrame.

    '''
        Date        Open        High        Low         Close       Adj Close    Volume
        2023-02-15  176.210007  178.820007  175.000000  177.419998  176.321732   815900
        2023-02-16  175.000000  177.279999  174.720001  176.220001  175.129166   679300
        2023-02-17  176.419998  177.330002  175.000000  177.130005  176.033524  1829500

              Open   High    Low  Close    Volume
              XOM    XOM    XOM    XOM       XOM
2021-01-04  35.12  34.74  35.16  35.80  27764700
2021-01-05  35.45  35.44  36.86  37.96  44035100
2021-01-06  37.63  37.03  37.80  38.21  36484800
2021-01-07  38.13  37.73  38.09  38.61  29528100
2021-01-08  38.30  38.09  38.52  38.82  28628200        
    '''

    if df_prices is None or df_prices.empty:
      raise ValueError(f"Failed to download data for {symbol}. DataFrame is empty.")

  except Exception as e:
    logger.error("An error occurred while downloading data: {}", e)
    return None
  
  tm_after_download = time.time()
  tm_taken_for_download_secs = tm_after_download - tm_before_download 
  tm_taken_for_download_secs  = "{:.3f}".format(tm_taken_for_download_secs)
  logger.debug("Time taken for download (secs) = {}", tm_taken_for_download_secs)

  m_oth.fn_df_print_first_last_rows(df_prices, 5, 'ALL_COLS')
  print(f"--DataFrame Shape: {df_prices.shape} rows and columns--")
  print(f"--df.columns = {df_prices.columns}--")
  print(f"--type(df.columns) = {type(df_prices.columns)}--")

  # Now convert/format the dataframe to our required format
  df_prices.columns = df_prices.columns.droplevel(1)        # Flatten MultiIndex columns by dropping the second level ('XOM')
  df_prices = df_prices.reset_index()                       # Reset the index to make 'Date' a column
  df_prices.rename(columns={'index': 'Date'}, inplace=True)
  df_prices = df_prices[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]   # Reorder columns to match the desired format

  m_oth.fn_df_print_first_last_rows(df_prices, 5, 'ALL_COLS')
  print(f"--DataFrame Shape: {df_prices.shape} rows and columns--")
  print(f"--df.columns = {df_prices.columns}--")
  print(f"--type(df.columns) = {type(df_prices.columns)}--")

  if write_to_file:
    FILE_EXTN =".csv"
    csv_file_path = symbol + FILE_EXTN
    df_prices.to_csv(csv_file_path, index=False)
    logger.info("DataFrame has been written to {} ...", csv_file_path)

  logger.debug("---------- fn_download_historical_data_for_symbol ---- COMPLETED ----------")
  return df_prices
  



def fn_get_historical_data_loop_symbols_list(data_venue: str, lst_symbols: list, start_date: datetime, end_date: datetime, write_to_file: bool) -> pd.DataFrame:

  # this will take 1 symbol at a time from the symbols list and download data from the data_venue for it
  # can cause venue to deny our requests if we have a bunch of symbols

  logger.debug("Received arguments : data_venue={} write_to_file={} start_date={} end_date={} lst_symbols={}", data_venue, write_to_file, start_date, end_date, lst_symbols)

  for symbol in lst_symbols:
    logger.debug("symbol={}", symbol)
    fn_download_historical_data_for_one_symbol(data_venue, symbol, start_date, end_date, write_to_file)



def fn_get_historical_data_multiple_symbols_single_request(lst_symbols: list, start_date: datetime, session: requests.Session) -> pd.DataFrame:

  """
  Fetch historical stock data for multiple symbols using yfinance in a single API call.

  :param symbols: List of stock symbols (e.g., ['AAPL', 'MSFT', 'IBM'])
  :param start_date: Start date for historical data in 'YYYY-MM-DD' format.
  :return: Pandas DataFrame containing stock data.

Ticker            AAPL                                                      MSFT                                                       IBM
Price             Open        High         Low       Close    Volume        Open        High         Low       Close    Volume        Open        High         Low       Close   Volume
Date
2024-12-02  237.270004  240.789993  237.160004  239.589996  48137100  421.570007  433.000000  421.309998  430.980011  20207200  227.500000  228.380005  225.509995  227.389999  2655900
2024-12-03  239.809998  242.759995  238.899994  242.649994  38861000  429.839996  432.470001  427.739990  431.200012  18302000  227.240005  229.110001  226.669998  229.000000  3163800
2024-12-04  242.869995  244.110001  241.250000  243.009995  44383900  433.029999  439.670013  432.630005  437.420013  26009400  230.000000  233.740005  229.350006  233.490005  4104200
2024-12-05  243.990005  244.539993  242.130005  243.039993  40033900  437.920013  444.660004  436.170013  442.619995  21697800  233.550003  236.520004  233.460007  234.750000  4791100
2024-12-06  242.910004  244.630005  242.080002  242.839996  36870600  442.299988  446.100006  441.769989  443.570007  18821000  234.429993  238.380005  234.220001  238.039993  4028400

  """

  df_prices_mult_symbols = yf.download(lst_symbols, start=start_date, group_by='ticker', session=session)
  #print(df_prices_mult_symbols.head())

  return df_prices_mult_symbols





def get_other_data():


  '''
  # get historical market data
  df_hist = msft.history(period="1mo")
  print("---- hist = ", df_hist)
  
  # show meta information about the history (requires history() to be called first)
  print("---- history metadata = ", msft.history_metadata)
  
  # show actions (dividends, splits, capital gains)
  msft.actions
  msft.dividends
  msft.splits
  msft.capital_gains  # only for mutual funds & etfs
  '''
  
  msft = yf.Ticker("MSFT")
  
  # get all stock info
  #print(msft.info)
  
  multi_tickers = yf.Tickers("INRG.L NUCG.L UKDV.L")
  print("datatype of multi_tickers =", type(multi_tickers))
  print("datatype of multi_tickers.tickers['INRG.L'] =", type(multi_tickers.tickers['INRG.L']))
  #print(multi_tickers.tickers['INRG.L'].info)
  #print(multi_tickers.tickers['NUCG.L'].info)
  print(multi_tickers.tickers['UKDV.L'].info)
  
  dct_ticker_info = multi_tickers.tickers['UKDV.L'].info
  
  print("---- dct_ticker_info items ----")
  for k,v in dct_ticker_info.items():
    print(k, "->", v)
  
  df = pd.DataFrame.from_dict(dct_ticker_info,orient='index')
  df = df.reset_index()
  print("---- df ----")
  print(df)
  
  '''
  {'phone': '+353 1 776 3000', 'maxAge': 86400, 'priceHint': 2, 'previousClose': 10.089, 'open': 10.158, 'dayLow': 10.06, 'dayHigh': 10.158, 'regularMarketPreviousClose': 10.089, 'regularMarketOpen': 10.158, 'regularMarketDayLow': 10.06, 'regularMarketDayHigh': 10.158, 'trailingPE': 0.12165763, 'volume': 4197, 'regularMarketVolume': 4197, 'averageVolume': 8713, 'averageVolume10days': 7461, 'averageDailyVolume10Day': 7461, 'bid': 10.066, 'ask': 10.2, 'bidSize': 0, 'askSize': 0, 'yield': 0.0387, 'totalAssets': 108225024, 'fiftyTwoWeekLow': 8.787, 'fiftyTwoWeekHigh': 11.0, 'fiftyDayAverage': 9.484134, 'twoHundredDayAverage': 9.728753, 'navPrice': 10.08857, 'currency': 'GBP', 'ytdReturn': 0.0581014, 'beta3Year': 1.04, 'fundFamily': 'State Street Global Advisors Europe Limited', 'fundInceptionDate': 1330387200, 'legalType': 'Exchange Traded Fund', 'threeYearAverageReturn': 0.032389, 'fiveYearAverageReturn': 0.0403198, 'exchange': 'LSE', 'quoteType': 'ETF', 'symbol': 'UKDV.L', 'underlyingSymbol': 'UKDV.L', 'shortName': 'SSGA SPDR ETFS EUROPE I PLC SPD', 'longName': 'SPDR S&P UK Dividend Aristocrats UCITS ETF', 'firstTradeDateEpochUtc': 1330416000, 'timeZoneFullName': 'Europe/London', 'timeZoneShortName': 'GMT', 'uuid': '257b74d6-04c8-3278-8b39-b6b405510a71', 'messageBoardId': 'finmb_170253830', 'trailingPegRatio': None}
  '''
  
  # show share count
  msft.get_shares_full(start="2022-01-01", end=None)
  
  # show financials:
  # - income statement
  msft.income_stmt
  msft.quarterly_income_stmt
  # - balance sheet
  msft.balance_sheet
  msft.quarterly_balance_sheet
  # - cash flow statement
  msft.cashflow
  msft.quarterly_cashflow
  # see `Ticker.get_income_stmt()` for more options
  
  # show holders
  msft.major_holders
  msft.institutional_holders
  msft.mutualfund_holders
  
  # Show future and historic earnings dates, returns at most next 4 quarters and last 8 quarters by default. 
  # Note: If more are needed use msft.get_earnings_dates(limit=XX) with increased limit argument.
  msft.earnings_dates
  
  # show ISIN code - *experimental*
  # ISIN = International Securities Identification Number
  msft.isin
  
  # show options expirations
  msft.options
  
  # show news
  msft.news
  
  # get option chain for specific expiration
  opt = msft.option_chain('YYYY-MM-DD')
  # data available via: opt.calls, opt.puts
  print(opt)

# List of S&P 500 tickers
tickers = ['AAPL', 'MSFT', 'GOOGL']


def get_stock_info(symbol):
    # if symbol does not exist, handle gracefully and return None, else return ticker info object

  # new version of yfinance needs SSL verification and i had bunch of issues from my office network
  # so using unsafe_session
  # this will circumvent SSL verification with warnings
  unsafe_session = requests.session()
  unsafe_session.verify = False

  try:
      print(f"--- get_stock_info() ---{symbol}---")
      ticker = yf.Ticker(symbol)
      dct_info = ticker.info

      # Print all available fields
      #for key, value in dct_info.items():
      #  print(f"key/value    {key}: {value}")

      print("longname=", dct_info.get('longName'))
      print("industry=", dct_info.get('industry'))
      print("sector=", dct_info.get('sector'))
      print("previousClose=", dct_info.get('previousClose'))
      return dct_info
  except HTTPError as e:
      if e.response.status_code == 404:
          print(f"Symbol '{symbol}' not found.")
      else:
          print(f"An error occurred: {e}")
      return None

#        # Example usage
#        symbol = 'TSLA'
#        stock_info = get_stock_info(symbol)
#        
#        if stock_info:
#            print("Stock Information:")
#            for key, value in stock_info.items():
#                print(f"{key}: {value}")



def fn_sync_price_data_in_table_for_symbol(data_venue: str, dbconn, symbol: str) -> pd.DataFrame:
  """
  Synchronize the price data for a symbol in a table in the database.

  TODO: check if i need the sybmol to exist in tbl_instrument
  If the symbol does not exist, create it.
  If the symbol already exists, update it with the latest price data. 

  Summary:
  It checks if there's existing price data for the symbol in the database.
  If data exists, it checks for missing recent data (more than 1 day) and downloads the missing data if necessary.
  If the symbol is a benchmark symbol (SPY), it skips downloading data if there are less than 2 days of missing data.
  If no data exists for the symbol, it downloads historical price data for the symbol with a default lookback period (approximately 1 year + 200 days).
  It modifies the downloaded data according to specific requirements and inserts it into the database table.
  Finally, it returns a pandas DataFrame containing the newly inserted data.

  Parameters:
  - data_venue (str): The string representing the data venue.
  - dbconn : handle to db
  - symbol (str): The string representing the symbol.
  
  Returns:
  - pandas dataframe containing ONLY THAT data which was INSERTED into the table

  Example:
  >> fn_sync_price_data_in_table_for_symbol("YFINANCE", dbconn, "AAPL")
  """
  dt_default_start_date = datetime(2024, 1, 1)
  
  logger.log("MYNOTICE", "START: LOG-TAG-003 : Synchronizing price data from data feed into table {}", symbol)
  m_oth.fn_inspect_caller_functions()
  logger.debug("Received arguments : data_venue={} dbconn={} symbol={}", data_venue, dbconn, symbol)
  df_return = pd.DataFrame()

  # check if there is any price data at all in the database for this symbol and fetch it into a df
  df_sym_stats = m_udb.fn_get_symbol_price_data_stats_from_database(dbconn, symbol)
  if not df_sym_stats.empty:
    logger.debug("--IF 1-- df_sym_stats is not empty")
    dt_oldest_record_time = df_sym_stats["oldest_rec_pd_time"].iloc[0].date()
    dt_latest_record_date = df_sym_stats["latest_rec_pd_time"].iloc[0].date()
    dt_today = datetime.now().date()
    diff_days = m_udt.compute_date_difference(dt_latest_record_date, dt_today, "WORKING")
    # df_is not empty but there could be a few recent days/weeks missing, so check for that
    if diff_days > 1:
      logger.debug("--IF 2-- diff_days > 1")
      logger.trace("df_sym_stats is not empty, but missing some days of recent data")
      logger.log("MYNOTICE", "Number of days of missing data = {}. So now fetch and insert this missing recent data into price data table ", diff_days)
      dt_start_date = m_udt.get_date_with_zero_time(dt_latest_record_date)
      dt_start_date += timedelta(days=1)
      dt_end_date = m_udt.get_date_with_zero_time(dt_today)

      # If the symbol passed was the benchmark symbol, then check if we have latest data (<2 missing is fine) for it already, and if so, don't download it again
      if symbol == 'SPY':
        if diff_days <= 2:
          logger.warning("SPECIAL SITUATION: symbol is the BENCHMARK symbol {} but diff_days is just under 2 days. So we are going to skip download for it ...", symbol)
          return df_return
        else:
          logger.warning("SPECIAL SITUATION: symbol is the BENCHMARK symbol {} but diff_days is more than 2 days.. So proceeding to download for it ...", symbol)
      else:
        logger.debug("Not a benchmark symbol")

      df_downloaded_missing_price_data = fn_download_historical_data_for_one_symbol('YFINANCE', symbol, dt_start_date, dt_end_date, False)
      if df_downloaded_missing_price_data is None:
        return None
      print("---sync---01-----", df_downloaded_missing_price_data.head)
      df_downloaded_missing_price_data = m_oth.fn_modify_dataframe_per_our_requirements(symbol, df_downloaded_missing_price_data)
      print("---sync---02-----", df_downloaded_missing_price_data.head)
      logger.debug("Now inserting the missing data into the table")
      df_return = m_udb.fn_insert_symbol_price_data_into_db(dbconn, symbol, df_downloaded_missing_price_data, "tbl_price_data_1day", True)
    else:
      logger.debug("--ELSE 2-- diff_days < 1")
      logger.debug("df_sym_stats is not empty but negligible number of days of missing data = {}. Not downloading.", diff_days)
      df_return = m_udb.fn_get_table_data_for_symbol(dbconn, symbol, dt_oldest_record_time, dt_latest_record_date)
      logger.debug("--ELSE 2-- diff_days < 1 ---END -- df=", df_return)
  else:
    logger.debug("--ELSE 1-- df_sym_stats is empty meaning there is no price data in the table")
    logger.trace("df_sym_stats is empty for symbol = {}", symbol)
    logger.warning("Price data not available for symbol {} in database", symbol)
    '''
    # commented this out for now and will use a hard-coded start_date time.
    # get roughly 1 year of historical data plus go further back and get another 200 days
    # that is because we dont want the SMA_200 plot to just start in the middle of the chart
    # so we are looking at around 565 days of data in total
    dt_start_date = datetime.now() - timedelta(days=365) - timedelta(days=200)
    '''
    dt_start_date = dt_default_start_date
    #dt_end_date = datetime.now() - timedelta(days=1)     # commenting out for now as seems to be not downloading yesterday prices
    dt_end_date = datetime.now()
    dt_start_date = dt_start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    dt_end_date = dt_end_date.replace(hour=0, minute=0, second=0, microsecond=0)
    logger.info("Downloading historical price data with a default lookback period...")
    df_sym_downloaded_price_data = fn_download_historical_data_for_one_symbol("YFINANCE", symbol, dt_start_date, dt_end_date, False)
    df_sym_downloaded_price_data = m_oth.fn_modify_dataframe_per_our_requirements(symbol, df_sym_downloaded_price_data)
    logger.debug("--ELSE 1-- modified df_sym_downloaded_price_data prepared for insertion into table :")
    m_oth.fn_df_print_first_last_rows(df_sym_downloaded_price_data, 3, 'ALL_COLS')

    # now  insert them into price data table
    #m_udb.fn_insert_symbol_price_data_into_db(dbconn, symbol, df_sym_downloaded_price_data, "tbl_price_data_1day", True)
    df_return = m_udb.fn_insert_symbol_price_data_into_db(dbconn, symbol, df_sym_downloaded_price_data, "tbl_price_data_1day", True)

  m_oth.fn_df_print_first_last_rows(df_return, 3, 'ALL_COLS')
  logger.log("MYNOTICE", "END: LOG-TAG-003 : End of Synchronizing price data from data feed into table {}", symbol)
  return df_return


def fn_disable_session_for_ssl() -> requests.Session:
  unsafe_session = requests.session()
  unsafe_session.verify = False
  logger.warning("Session is disabled for SSL verification")
  return unsafe_session



def fn_get_data_without_using_ssl(symbol):
  # once i upgraded yfinance module to version 0.2.51 (from 0.1.xx), started getting SSL CERTIFICATE type errors when trying from my office network.
  # so found this way online to get data, which works
  # https://stackoverflow.com/questions/79189727/how-to-disable-or-ignore-the-ssl-for-the-yfinance-package

  unsafe_session = requests.session()
  unsafe_session.verify = False

  print(f"---- fetching without ssl from yfinance for symbol {symbol} ----")
  df = yf.download(symbol, start='2024-01-01', end='2025-01-01', session=unsafe_session)
  print(df)

  # NOTE: 0.2.5 atleast, i saw the below format, which is a MultiIndex format, so if want to use we will have to convert some of it
  # Price           Close       High        Low       Open    Volume
  # Ticker            WMT        WMT        WMT        WMT       WMT
  # Date
  # 2024-01-02  52.467781  52.550126  51.776071  51.795835  23539800
  # 2024-01-03  52.471073  52.800461  52.349201  52.625887  18756000
  # ...               ...        ...        ...        ...       ...
  # 2024-12-30  90.570000  91.070000  90.129997  90.730003   9790200
  # 2024-12-31  90.349998  90.940002  90.059998  90.570000  11267700