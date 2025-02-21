# this for S&P 500 stocks 
# using yahoo finance to dowload quotes
# using ??? for technical analysis

import requests
from bs4 import BeautifulSoup
import yfinance as yf

def get_stock_list():
  # this is the website we're going to scrape from
  print('In get_stock_list ...')
  url = "https://www.malaysiastock.biz/Stock-Screener.aspx"
  response = requests.get(url, headers={'User-Agent':'test'})
  soup = BeautifulSoup(response.content, "html.parser")
  table = soup.find(id = "MainContent2_tbAllStock")
  # return the result (only ticker code) in a list
  return [stock_code.get('href')[-4:] for stock_code in table.find_all('a')]

def get_stock_price(symbol):
  print('In get_stock_list for ', symbol, ' ...')
  # you can change the start date
  df_prices = yf.download(symbol, start="2023-01-01", rounding=True, session=session, progress=True, auto_adjust=True)
  #print('data=', df_prices)
  print("FIRST row of df_stock_quotes df = ", df_prices.head(1))
  print("LAST row of df_stock_quotes df = ", df_prices.tail(1))
  return df_prices

def add_EMA(price, day):
  return price.ewm(span=day).mean()

def add_STOCH(close, low, high, period, k, d=0): 
    STOCH_K = ((close - low.rolling(window=period).min()) / (high.rolling(window=period).max() - low.rolling(window=period).min())) * 100
    STOCH_K = STOCH_K.rolling(window=k).mean()
    if d == 0:
      return STOCH_K
    else:
      STOCH_D = STOCH_K.rolling(window=d).mean()
      return STOCH_D

def check_bounce_EMA(df):
    candle1 = df.iloc[-1]
    candle2 = df.iloc[-2]
    cond1 = candle1['EMA18'] > candle1['EMA50'] > candle1['EMA100']
    cond2 = candle1['STOCH_%K(5,3,3)'] <= 30 or candle1['STOCH_%D(5,3,3)'] <= 30
    cond3 = candle2['Low'] < candle2['EMA50'] and \
            candle2['Close'] > candle2['EMA50'] and \
            candle1['Low'] > candle1 ['EMA50']
    #return cond1 and cond2 and cond3
    return cond1        # temp for testing just to make sure we get results


def main():
  # a list to store the screened results
  screened_list = [] 
  # get the full stock list
  #stock_list = get_stock_list()
  #print('stock_list=', stock_list)
  print("------- 1 ----------")
  
  # temporary, to reduce symbols and data lookups for testing
  #my_temp_filtered_stock_list =  [ symbol for symbol in stock_list if "113" in symbol ]
  my_temp_filtered_stock_list = ['AAPL', 'NFLX', 'META', 'ORCL', 'PFE']
  print('my_temp_filtered_stock_list (for analysis) =', my_temp_filtered_stock_list)
  
  for symbol in my_temp_filtered_stock_list:
  
    #print(symbol) # remove this if you dont want the ticker to be printed
    df_stock_quotes = []
    try: 
      # Step 1: get stock price for each stock
      df_stock_quotes = get_stock_price(symbol)
      print("------- 2 ----------")
  
      # Step 2: add technical indicators (in this case EMA)
      close = df_stock_quotes['Close']
      low = df_stock_quotes['Low']
      open = df_stock_quotes['Open']
      high = df_stock_quotes['High']
      df_stock_quotes['EMA18'] = add_EMA(close,18)
      df_stock_quotes['EMA50'] = add_EMA(close,50)
      df_stock_quotes['EMA100'] = add_EMA(close,100)
      df_stock_quotes['STOCH_%K(5,3,3)'] = add_STOCH(close, low, high, 5, 3)
      df_stock_quotes['STOCH_%D(5,3,3)'] = add_STOCH(close, low, high, 5, 3, 3)
  
      # if all 3 conditions are met, add stock into screened list
      if check_bounce_EMA(df_stock_quotes):
        screened_list.append(symbol)
        print('In analysis loop : Cumulative screened_list currently =', screened_list)
    except Exception as e:
      print(e)

  print('screened_list (post analysis) =', screened_list)



# --- main ---
if __name__ == '__main__':
  # main(sys.argv)
  main()

