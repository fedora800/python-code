import yfinance as yf
import requests

session = requests.Session()
session.verify = False  # Disable SSL verification

df_prices = yf.download("XOM", start="2025-01-01", end="2025-01-31", rounding=True, session=session)

print(df_prices)