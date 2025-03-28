# https://levelup.gitconnected.com/automate-your-stock-screening-using-python-9107dda724c3

import requests
from bs4 import BeautifulSoup
import yfinance as yf

def get_stock_list():
  # this is the website we're going to scrape from
  url = "https://www.malaysiastock.biz/Stock-Screener.aspx"
  response = requests.get(url, headers={'User-Agent':'test'})
  soup = BeautifulSoup(response.content, "html.parser")
  table = soup.find(id = "MainContent2_tbAllStock")
  # return the result (only ticker code) in a list
  return [stock_code.get('href')[-4:] for stock_code in table.find_all('a')]

def get_stock_price(code):
  # you can change the start date
  data = yf.download(code, start="2022-01-01", rounding=True, progress=True, auto_adjust=True)
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
    return cond1 and cond2 and cond3


# a list to store the screened results
screened_list = [] 
# get the full stock list
stock_list = get_stock_list()
for stock_code in stock_list:

  print(stock_code) # remove this if you dont want the ticker to be printed
  try: 
    # Step 1: get stock price for each stock
    price_chart_df = get_stock_price(stock_code + ".KL")

    # Step 2: add technical indicators (in this case EMA)
    close = price_chart_df['Close']
    low = price_chart_df['Low']
    open = price_chart_df['Open']
    high = price_chart_df['High']
    price_chart_df['EMA18'] = add_EMA(close,18)
    price_chart_df['EMA50'] = add_EMA(close,50)
    price_chart_df['EMA100'] = add_EMA(close,100)
    price_chart_df['STOCH_%K(5,3,3)'] = add_STOCH(close, low, high, 5, 3)
    price_chart_df['STOCH_%D(5,3,3)'] = add_STOCH(close, low, high, 5, 3, 3)

    # if all 3 conditions are met, add stock into screened list
    if check_bounce_EMA(price_chart_df):
      screened_list.append(stock_code)
      print(screened_list)
  except Exception as e:
    print(e)

