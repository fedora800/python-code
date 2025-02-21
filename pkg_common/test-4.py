import ssl
import certifi
import yfinance as yf
import requests

# Set up session without SSL verification
session = requests.Session()
session.verify = False  # Disable SSL verification

# Fetch data with the insecure session
ticker = "META"
data = yf.download(ticker, session=session)
print(data)
