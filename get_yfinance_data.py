
# https://pypi.org/project/yfinance/
# https://analyzingalpha.com/yfinance-python

import yfinance as yf
import pandas as pd
import datetime


def get_historical_data():

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
  
  # 25 largest S&P 500 index constituents by weighting
  # AAPL, MSFT, AMZN, NVDA, GOOGL, TSLA, GOOG, BRK.B, META, UNH, XOM, LLY, JPM, JNJ, V, PG, MA, AVGO, HD, CVX, MRK, ABBV, COST, PEP, ADBE
  #lst_symbols = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'TSLA', 'GOOG', 'BRK.B', 'META', 'UNH', 'XOM', 'LLY', 'JPM', 'JNJ', 'V', 'PG', 'MA', 'AVGO', 'HD', 'CVX', 'MRK', 'ABBV', 'COST', 'PEP', 'ADBE']
  lst_symbols = ['META', 'TSLA', 'XOM']
  print('symbols to download = ', lst_symbols)

  start_date = datetime.datetime(2022, 1, 1)
  end_date = datetime.datetime(2023, 12, 31)
  for sym in lst_symbols:
    print('downloading for ', sym)

    # get historical market data and write to csv file
    df_prices = yf.download(sym, start=start_date, end=end_date)
    print(df_prices.head(3))
    df_prices.insert(0, "Symbol", sym) # add Symbol as 2nd column after date
    #df_prices['Symbol'] = sym   # but this will add as the last column of df
    df_prices.drop(columns=['Adj Close'], inplace=True)
    print("modified df so as to be able to insert into postgres table : \n", df_prices.head(3))
    df_prices.to_csv(sym + '.csv')
  
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


def main():

  print('Starting ...')

  get_historical_data()

  #get_historical_data_multiple_symbols()
#  get_other_data()



# --- main ---
if __name__ == '__main__':
  # main(sys.argv)
  main()


