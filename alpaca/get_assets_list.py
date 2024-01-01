import config
from alpaca.data.historical import CryptoHistoricalDataClient, StockHistoricalDataClient
#from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.requests import StockBarsRequest
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime


'''
crypto_client = CryptoHistoricalDataClient(config.ALPACA_API_KEY, config.ALPACA_API_SECRET)
request_params = CryptoBarsRequest(
                        symbol_or_symbols=["BTC/USD", "ETH/USD"],
                        timeframe=TimeFrame.Day,
                        start="2022-07-01"
                 )

bars = crypto_client.get_crypto_bars(request_params)
'''

stock_client = StockHistoricalDataClient(config.ALPACA_API_KEY, config.ALPACA_API_SECRET)
# multi symbol request - single symbol is similar
multisymbol_request_params = StockLatestQuoteRequest(symbol_or_symbols=["SPY", "GLD", "TLT"])
latest_multisymbol_quotes = stock_client.get_stock_latest_quote(multisymbol_request_params)
#print("latest_multisymbol_quotes = ", latest_multisymbol_quotes)

print(latest_multisymbol_quotes)
gld_latest_ask_price = latest_multisymbol_quotes["GLD"].ask_price
print("GLD latest ask price = ", gld_latest_ask_price)

request_params = StockBarsRequest(
                        symbol_or_symbols=["AAPL", "NFLX"],
                        start=datetime(2023, 12, 1),
                        end=datetime(2023, 12, 7),
                        timeframe=TimeFrame.Day
                 )
bars = stock_client.get_stock_bars(request_params)

print(bars["AAPL"])

