
# https://pypi.org/project/yfinance/
# https://analyzingalpha.com/yfinance-python

from loguru import logger
import yfinance as yf
import pandas as pd
import csv
from requests.exceptions import HTTPError
from datetime import datetime, timezone, timedelta



def read_csv_into_list(file_path, has_header=True):
    """
    Read a CSV file and store its contents in a list.

    Parameters:
    - file_path (str): The path to the CSV file.
    - has_header (bool, optional): Specify if the CSV file has a header row. Defaults to True.

    Returns:
    list: A list containing rows from the CSV file.
    """

    lst_csv_data = []

    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        # Skip the header row if present
        if has_header:
            next(csvreader)

        # Iterate over rows and append them to the list
        for row in csvreader:
           # lst_csv_data.append(row)
            lst_csv_data.extend(row)  # single-column file so we just extend the value into the list

    return lst_csv_data


def get_historical_data_symbol(df):

  """ Download price data from the data venue.
      Symbol and the timeframe will be passed by upstream function

  Parameters:
  a 1 row df containing the symbol name, start date, end date and number of records alredy in table

  Returns:
  dataframe containing latest price data (that is not in our tables) for that symbol 

  """
  data_venue = "YFINANCE"
  symbol = df.at[0,"pd_symbol"]
  oldest_price_date = df.at[0,"oldest_rec_pd_time"]
  latest_price_date = df.at[0,"latest_rec_pd_time"]
  num_records = df.at[0,"num_records"]
  logger.debug("symbol={} oldest_price_date={} latest_price_date={} num_records={}", symbol, oldest_price_date, latest_price_date, num_records)

  # do not re-download data that already exists
  # Convert the date strings to datetime objects 
  latest_price_date = pd.to_datetime(latest_price_date)
  next_day = latest_price_date + timedelta(days=1)      # just start from the next day of the latest price date
  start_date = next_day.replace(tzinfo=timezone.utc)    # get till yesterday
  end_date = datetime.now() - timedelta(days=1)
  logger.info("Downloading from {} for symbol={} start_date={} end__date={}", data_venue, symbol, start_date, end_date)
  df_prices = yf.download(symbol, start=start_date, end=end_date)
  '''
             Date        Open        High        Low         Close       Adj Close    Volume
             2023-02-15  176.210007  178.820007  175.000000  177.419998  176.321732   815900
             2023-02-16  175.000000  177.279999  174.720001  176.220001  175.129166   679300
             2023-02-17  176.419998  177.330002  175.000000  177.130005  176.033524  1829500
  '''
  print(df_prices)
  return df_prices


def get_historical_data_batch_of_symbols():

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
  #lst_symbols = read_csv_into_list(csv_file_path, has_header=False)
  # 25 largest S&P 500 index constituents by weighting
  # AAPL, MSFT, AMZN, NVDA, GOOGL, TSLA, GOOG, BRK-B, META, UNH, XOM, LLY, JPM, JNJ, V, PG, MA, AVGO, HD, CVX, MRK, ABBV, COST, PEP, ADBE
  #lst_symbols = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'TSLA', 'GOOG', 'BRK-B', 'META', 'UNH', 'XOM', 'LLY', 'JPM', 'JNJ', 'V', 'PG', 'MA', 'AVGO', 'HD', 'CVX', 'MRK', 'ABBV', 'COST', 'PEP', 'ADBE']
  #lst_symbols = ['META', 'TSLA', 'XOM']
  #lst_symbols = ['V3AB.L','V3AM.L','V3MB.L','V3MM.L','VAGP.L','VAGS.L','VALW.L','VAPX.L','VCPA.L','VDPG.L','VECP.L','VEGB.L','VEMT.L','VERG.L','VERX.L','VETY.L','VEUR.L','VEVE.L','VFEG.L','VFEM.L','VGER.L','VGOV.L','VGPA.L','VGVA.L','VHVG.L','VHYG.L','VHYL.L','VJPB.L','VJPN.L','VMID.L','VMIG.L','VNRG.L','VNRT.L','VPNG.L','VUAG.L','VUCP.L','VUKE.L','VUKG.L','VUSA.L','VUSC.L','VUTA.L','VUTY.L','VWRL.L','VWRP.L']
  #lst_symbols = ['VMID.L','VUKE.L','VUSA.L']
  lst_symbols = ['SPY']
  print('symbols to download = ', lst_symbols)

  start_date = datetime.datetime(2023, 1, 1)
  end_date = datetime.datetime(2024, 1, 14)
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
    output_file = "timescaledb/data/" + sym + ".csv"
    #output_file = "/tmp/" + sym + ".csv"
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


