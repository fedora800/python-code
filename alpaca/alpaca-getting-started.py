# https://docs.alpaca.markets/docs/getting-started-with-alpaca-market-data
# https://github.com/alpacahq/alpaca-py
# works perfectly fine without needing API keys as its crypto

# pip install alpaca-py

from alpaca.data.historical import CryptoHistoricalDataClient
from datetime import datetime, timezone

# No keys required for crypto data
client = CryptoHistoricalDataClient()

# Next we’ll define the parameters for our request. Import the request class for crypto bars, 
# CryptoBarsRequest and TimeFrame class to access time frame units more easily. 
# This example queries for historical daily bar data of Bitcoin in the first week of September 2022.
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime

# Creating request object
request_params = CryptoBarsRequest(
                        symbol_or_symbols=["BTC/USD"],
                        timeframe=TimeFrame.Day,
#                        start=datetime(2022, 9, 1), T00:00:00Z",
                        start=datetime(2023, 3, 1, 0, 0, 0, tzinfo=timezone.utc),
#                        end=datetime(2022, 9, 7) T00:00:00Z"
                        end=datetime(2024, 3, 4, 0, 0, 0, tzinfo=timezone.utc),
                        )

# Finally, send the request using the client’s built-in method, get_crypto_bars. 
# Additionally, we’ll access the .df property which returns a pandas DataFrame of the response.
# Retrieve daily bars for Bitcoin in a DataFrame and printing it
btc_bars = client.get_crypto_bars(request_params)

# Convert to dataframe
btc_bars.df

print("---btc_bars=")
print(btc_bars)
