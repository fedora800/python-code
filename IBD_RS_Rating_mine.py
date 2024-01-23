#https://github.com/shashankvemuri/Finance/blob/master/find_stocks/IBD_RS_Rating.py

# Imports
import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr
import datetime
import time
import sys
import os
parent_dir = os.path.dirname(os.getcwd())
sys.path.append(parent_dir)

# Override yfinance API for pandas datareader
yf.pdr_override()

# Retrieve S&P 500 tickers and format for Yahoo Finance
#sp500_tickers = ['AAPL', 'MSFT']
sp500_tickers = ['AAPL']

# Set S&P 500 index ticker
sp500_index = '^GSPC'

# Define date range for stock data
start_date = datetime.datetime.now() - datetime.timedelta(days=365)
end_date = datetime.date.today()

# Initialize list for storing relative stock returns
relative_returns = []

# Fetch and process S&P 500 historical data
print('---SP500 index info---')
df_sp500_index = pdr.get_data_yahoo(sp500_index, start_date, end_date)
df_sp500_index['Dly_Pct_Change'] = df_sp500_index['Adj Close'].pct_change()
df_sp500_index = df_sp500_index[['Adj Close','Dly_Pct_Change']]
#print(df_sp500_index.tail())
print(df_sp500_index)
sp500_cumulative_return = df_sp500_index['Dly_Pct_Change'].cumprod().iloc[-1]
print(sp500_cumulative_return)

# Compute relative returns for each S&P 500 stock
for ticker in sp500_tickers:
    try:
        print(f"---{ticker} info---")
        # Download stock data
        df_symbol = pdr.get_data_yahoo(ticker, start_date, end_date)
        df_symbol['Dly_Pct_Change'] = df_symbol['Adj Close'].pct_change()
        df_symbol = df_symbol[['Adj Close','Dly_Pct_Change']]
        print(df_symbol.tail())

        # Calculate cumulative return with added emphasis on recent quarter
#        stock_cumulative_return = (df_symbol['Dly_Pct_Change'].cumprod().iloc[-1] * 2 + df_symbol['Dly_Pct_Change'].cumprod().iloc[-63]) / 3

        # Calculate relative return compared to S&P 500
        relative_return = round(stock_cumulative_return / sp500_cumulative_return, 2)
        relative_returns.append(relative_return)

        print(f'Ticker: {ticker}; Relative Return against S&P 500: {relative_return}')
        time.sleep(1)  # Pause to prevent overloading server
    except Exception as e:
        print(f'Error processing {ticker}: {e}')

# Create dataframe with relative returns and RS ratings
rs_df = pd.DataFrame({'Ticker': sp500_tickers, 'Relative Return': relative_returns})
rs_df['RS_Rating'] = rs_df['Relative Return'].rank(pct=True) * 100
print(rs_df)

