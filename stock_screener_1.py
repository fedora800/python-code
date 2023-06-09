# https://levelup.gitconnected.com/automate-your-stock-screening-using-python-9107dda724c3

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

def get_stock_price(code):
  print('In get_stock_list for ', code, ' ...')
  # you can change the start date
  data = yf.download(code, start="2022-01-01")
  #print('data=', data)
  return data

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

# a list to store the screened results
screened_list = [] 
# get the full stock list
stock_list = get_stock_list()
print('stock_list=', stock_list)

# temporary, to reduce symbols and data lookups for testing
my_temp_filtered_stock_list =  [ symbol for symbol in stock_list if "113" in symbol ]
print('my_temp_filtered_stock_list=', my_temp_filtered_stock_list)

for stock_code in my_temp_filtered_stock_list:

  #print(stock_code) # remove this if you dont want the ticker to be printed
  try: 
    # Step 1: get stock price for each stock
    df_stock_quotes = get_stock_price(stock_code + ".KL")

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
      screened_list.append(stock_code)
      print(screened_list)
  except Exception as e:
    print(e)

print('screened_list=', screened_list)
