
# https://pypi.org/project/yfinance/
# https://analyzingalpha.com/yfinance-python

from loguru import logger
import yfinance as yf
import pandas as pd
import csv
from requests.exceptions import HTTPError
from datetime import datetime, timedelta
#import technical_analysis.mod_utils_db as m_udb
import mod_utils_db as m_udb
import mod_utils_date as m_udt
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



def get_historical_data_symbol(data_venue: str, symbol: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
  """
  Retrieves historical data for a symbol from a data venue.

  Parameters:
  - data_venue (str): The string representing the data venue.
  - symbol (str): The string representing the symbol.
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
  logger.info("Received arguments : data_venue={} symbol={} start_date={} end_date={}", data_venue, symbol, start_date, end_date)

  # # Convert the date strings to datetime objects and zero out time component
  # start_date = oldest_price_date.replace(hour=0, minute=0, second=0, microsecond=0)
  # #latest_price_date = pd.to_datetime(latest_price_date)
  # end_date = latest_price_date.replace(hour=0, minute=0, second=0, microsecond=0)

#  # do not re-download data that already exists
#  next_day = latest_price_date + timedelta(days=1)      # just start from the next day of the latest price date
#  if not oldest_price_date:
#    start_date = next_day.replace(tzinfo=timezone.utc)    # get till yesterday
#  end_date = datetime.now() - timedelta(days=1)

  logger.info("Downloading from {} for symbol={} start_date={} end_date={}", data_venue, symbol, start_date, end_date)
  #logger.info("Downloading from {} for symbol={} start_date={} end_date={}", data_venue, symbol, oldest_price_date, latest_price_date)
  df_prices = yf.download(symbol, start=start_date, end=end_date)
  '''
      Date        Open        High        Low         Close       Adj Close    Volume
      2023-02-15  176.210007  178.820007  175.000000  177.419998  176.321732   815900
      2023-02-16  175.000000  177.279999  174.720001  176.220001  175.129166   679300
      2023-02-17  176.419998  177.330002  175.000000  177.130005  176.033524  1829500
  '''
  #print(df_prices)
  df_head_foot = pd.concat([df_prices.head(1), df_prices.tail(1)])
  logger.debug("Downloaded - head/foot rows = {}", df_head_foot)
  logger.info("TODO: print how much time it took to download and well as how many rows ....")

  return df_prices


def get_historical_data_into_csv_files_for_batch_of_symbols():

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
  

  # this will be the full S&P 500 index constituents list
  #csv_file_path = 'sp500_constituents.csv'  # Replace with the actual path to your CSV file
  csv_file_path = "/tmp/file1.csv"
  lst_symbols = read_csv_into_list(csv_file_path, has_header=False)

  # 25 largest S&P 500 index constituents by weighting
  # AAPL, MSFT, AMZN, NVDA, GOOGL, TSLA, GOOG, BRK-B, META, UNH, XOM, LLY, JPM, JNJ, V, PG, MA, AVGO, HD, CVX, MRK, ABBV, COST, PEP, ADBE
  #lst_symbols = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'TSLA', 'GOOG', 'BRK-B', 'META', 'UNH', 'XOM', 'LLY', 'JPM', 'JNJ', 'V', 'PG', 'MA', 'AVGO', 'HD', 'CVX', 'MRK', 'ABBV', 'COST', 'PEP', 'ADBE']
  #lst_symbols = ['META', 'TSLA', 'XOM']
  #lst_symbols = ['V3AB.L','V3AM.L','V3MB.L','V3MM.L','VAGP.L','VAGS.L','VALW.L','VAPX.L','VCPA.L','VDPG.L','VECP.L','VEGB.L','VEMT.L','VERG.L','VERX.L','VETY.L','VEUR.L','VEVE.L','VFEG.L','VFEM.L','VGER.L','VGOV.L','VGPA.L','VGVA.L','VHVG.L','VHYG.L','VHYL.L','VJPB.L','VJPN.L','VMID.L','VMIG.L','VNRG.L','VNRT.L','VPNG.L','VUAG.L','VUCP.L','VUKE.L','VUKG.L','VUSA.L','VUSC.L','VUTA.L','VUTY.L','VWRL.L','VWRP.L']
  lst_symbols = ['VMID.L','VUKE.L','VUSA.L']
  #lst_symbols = ['SPY']
  print('symbols to download = ', lst_symbols)

  start_date = datetime(2023, 1, 1)
  end_date = datetime.now().date() - timedelta(days=1)
  for sym in lst_symbols:
    print('\ndownloading for ', sym)

    # get historical market data and write to csv file
    df_prices = yf.download(sym, start=start_date, end=end_date)
    print(df_prices.head(3), df_prices.tail(3))
    df_prices.insert(0, "Symbol", sym) # add Symbol as 2nd column after date
    #df_prices['Symbol'] = sym   # but this will add as the last column of df
    df_prices.drop(columns=['Adj Close'], inplace=True)
    #print("modified df so as to be able to insert into postgres table : \n", df_prices.head(1))
    #output_file = "timescaledb/data/sp500symbols/" + sym + ".csv"
    #output_file = "timescaledb/data/" + sym + ".csv"
    output_file = "/tmp/" + sym + ".csv"
    df_prices.to_csv(output_file)
    print("created data file - ", output_file)
    
  
  print('--done downloading---')

def get_historical_data_multiple_symbols():

  # this gives output in a non-user-friendly way, see below, i am not sure i want to use it.
  '''
,Close,Close,High,High,Low,Low,Open,Open,Volume,Volume
,AAPL,MSFT,AAPL,MSFT,AAPL,MSFT,AAPL,MSFT,AAPL,MSFT
Date,,,,,,,,,,
2023-12-04,189.42999267578125,369.1400146484375,190.0500030517578,369.5199890136719,187.4499969482422,362.8999938964844,189.97999572753906,369.1000061035156,43389500,32063300
2023-12-05,193.4199981689453,372.5199890136719,194.39999389648438,373.0799865722656,190.17999267578125,365.6199951171875,190.2100067138672,366.45001220703125,66628400,23065000
2023-12-06,192.32000732421875,368.79998779296875,194.75999450683594,374.17999267578125,192.11000061035156,368.0299987792969,194.4499969482422,373.5400085449219,41089700,21182100
2023-12-07,194.27000427246094,370.95001220703125,195.0,371.45001220703125,193.58999633789062,366.32000732421875,193.6300048828125,368.2300109863281,47477700,23118900
  '''

#tickers = yf.Tickers('msft aapl goog')
  df_prices_mult_symbols = yf.download("MSFT AAPL", period="1mo")
  print(df_prices_mult_symbols.head(3))
  df_prices_mult_symbols.drop(columns=['Adj Close'], inplace=True)
  print("modified df so as to be able to insert into postgres table : \n", df_prices_mult_symbols.head(3))
  df_prices_mult_symbols.to_csv('output-data.csv')



def get_other_data():
  
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




def get_stock_info(symbol):
    # if symbol does not exist, handle gracefully and return None, else return ticker info object
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        print("longname=", info.get('longName'))
        print("industry=", info.get('industry'))
        print("sector=", info.get('sector'))
        print("previousClose=", info.get('previousClose'))
        return info
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



def sync_price_data_in_table_for_symbol(data_venue: str, dbconn, symbol: str) -> pd.DataFrame:
  """
  TODO : Retrieves historical data for a symbol from a data venue.
  Then it will check our price data table and see if we have any data and if we have and not recent, it will download the missing data and insert into table.
  If there is no price data in our table, it will downloada  default amount of price data from the data source and insert into the price data table.

  
  Parameters:
  - data_venue (str): The string representing the data venue.
  - dbconn : handle to db
  - symbol (str): The string representing the symbol.
  
  Returns:
  - 2 pandas dataframes. [1st - df containing OHLC prices for the symbol] and [2nd - 1 row df containing some db stats info on the symbol] 

  Example:
  >> sync_price_data_in_table_for_symbol("YFINANCE", dbconn, "AAPL")
  """
  
  logger.debug("---- sync_price_data_in_table_for_symbol ---- STARTED ---")
  logger.debug("Received arguments : data_venue={} dbconn={} symbol={}", data_venue, dbconn, symbol)

  # check if there is any price data in the database for this symbol and fetch it into a df
  df_sym_stats = m_udb.get_symbol_price_data_stats_from_database(
      dbconn, symbol
  )
  if not df_sym_stats.empty:
    dt_latest_record_date = df_sym_stats["latest_rec_pd_time"].iloc[0].date()
    dt_today = datetime.now().date()
    diff_days = m_udt.compute_date_difference(dt_latest_record_date, dt_today, "WORKING")
    # df_is not empty but there could be a few recent days/weeks missing, so check for that
    if diff_days > 1:
      print("--here---888  IF DIFF_DAYS ----")
      logger.debug(
          "Number of days of missing data = {}. Now update the df with correct start and end dates for this missing data ",
          diff_days,
      )
      logger.debug(
          "Now fetch and insert this missing recent data into price data table"
      )

      dt_start_date = m_udt.get_date_with_zero_time(dt_latest_record_date)
      dt_start_date += timedelta(days=1)
      dt_end_date = m_udt.get_date_with_zero_time(dt_today)
      df_downloaded_missing_price_data = get_historical_data_symbol('YFINANCE', symbol, dt_start_date, dt_end_date)
      m_udb.insert_symbol_price_data_into_db(
          dbconn,
          symbol,
          df_downloaded_missing_price_data,
          "tbl_price_data_1day",
      )
    else:
      logger.debug("Negligible number of days of missing data = {}. Not downloading.", diff_days)
  else:
    print("--here---999  IF DF_SYM_STATS EMPTY ----")
    # df_sym_stats empty
    logger.warning(
        "Price data not available for symbol {} in database", symbol
    )
    # get roughly 1 year of historical data plus go further back ang get another 200 days
    # that is because we dont want the SMA_200 plot to just start in the middle of the chart
    # so we are looking at around 565 days of data in total
    dt_start_date = datetime.now() - timedelta(days=365) - timedelta(days=200)
    dt_end_date = datetime.now() - timedelta(days=1)
    dt_start_date = dt_start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    dt_end_date = dt_end_date.replace(hour=0, minute=0, second=0, microsecond=0)
    logger.info("Downloading historical price data with a default lookback period...")
    df_downloaded_price_data = get_historical_data_symbol("YFINANCE", symbol, dt_start_date, dt_end_date)

    # now  insert them into price data table
    m_udb.insert_symbol_price_data_into_db(
        dbconn,
        symbol,
        df_downloaded_price_data,
        "tbl_price_data_1day",
    )

  # now that symbol has been chosen from the dropdown, fetch requisite data for this symbol from db
  df_ohlcv_symbol = m_udb.get_table_data_for_symbol(dbconn, symbol)
  logger.debug("---- sync_price_data_in_table_for_symbol ---- RETURNING ---")
  return df_ohlcv_symbol, df_sym_stats