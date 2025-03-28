
import os
import certifi
os.environ["CURL_CA_BUNDLE"] = "C:\\mytmp\\downloads\\corp-root.crt"  # or .der if you kept it that way

import yfinance as yf

#os.environ["SSL_CERT_FILE"] = certifi.where()  # Use trusted CA bundle

print(os.environ.get("CURL_CA_BUNDLE"))

df_prices = yf.download("XOM", start="2025-05-01", end="2025-05-31", rounding=True, progress=True, auto_adjust=True)

print(df_prices)
