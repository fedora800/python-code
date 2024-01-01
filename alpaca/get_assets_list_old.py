import config
import alpaca_trade_api

api = alpaca_trade_api.REST(config.ALPACA_API_KEY, config.ALPACA_API_SECRET, base_url=config.ALPACA_API_URL)

assets = api.list_assets()

for asset in assets:
    print(f"asset = {asset.symbol}                 {asset.name}")


