# chatgpt code to get the top 20 stocks from sp500 which have the most 30-day average volume
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Step 1: Get S&P 500 Stock Symbols
sp500_symbols = ["AAPL", "GOOGL", ...]  # Add all S&P 500 stock symbols

# Step 2: Fetch Historical Data and Calculate 30-Day Volume Average
data = {}
for symbol in sp500_symbols:
    stock_data = yf.download(symbol, start=datetime.now() - timedelta(days=365), end=datetime.now())
    stock_data['30d_avg_volume'] = stock_data['Volume'].rolling(window=30).mean()
    data[symbol] = stock_data

# Step 3: Combine DataFrames into a Single DataFrame
combined_data = pd.concat(data.values(), keys=data.keys())

# Step 4: Sort and Select Top 20
top_20_stocks = combined_data.groupby(level=0).apply(lambda x: x.nlargest(1, '30d_avg_volume')).reset_index(level=1, drop=True)

# Display the top 20 stocks
print(top_20_stocks[['Close', '30d_avg_volume']])

