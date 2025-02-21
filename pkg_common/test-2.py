import yfinance as yf
import pandas as pd
import requests
import certifi

# Configure requests to use certifi's CA bundle
session = requests.Session()
session.verify = certifi.where()    # ensures that requests uses the certifi-managed CA bundle for SSL verification

# Define stock symbol
symbol = "AAPL"

# Fetch historical data using the session
print(f"Downloading data for {symbol} using a secure session...")
df = yf.download(symbol, start="2023-01-01", end="2024-01-01", rounding=True, session=session, progress=True, auto_adjust=True)    # use the secure session

# Display basic info
print(f"Downloaded {len(df)} rows for {symbol}")
print(df.head())  # Print the first few rows

# Print summary statistics
print("\nSummary statistics:")
print(df.describe())

