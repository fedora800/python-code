from datetime import datetime
import numpy as np
import pandas as pd
import yfinance as yf
import vectorbt as vbt

#price = vbt.YFData.download('BTC-USD').get('Close')

SYMBOL_FILE='BTC-USD.csv'
SMA_1 = 10
SMA_2 = 20

# Prepare data
start = datetime(2019, 1, 1)
end = datetime(2020, 1, 1)
#price = yf.Ticker("BTC-USD").history(start=start, end=end)['Close']
price = pd.read_csv(SYMBOL_FILE)
price.vbt.ohlcv.plot()

#print(price)
slow_ma = vbt.MA.run(price, SMA_1, short_name='slow')
fast_ma = vbt.MA.run(price, SMA_2, short_name='fast')

entries = fast_ma.ma_above(slow_ma, crossed=True)
exits = fast_ma.ma_below(slow_ma, crossed=True)
#print(entries)


#pf = vbt.Portfolio.from_holding(price, init_cash=100)
#pf.total_profit()
portfolio = vbt.Portfolio.from_signals(price, entries, exits)
print(portfolio.total_profit())
print(portfolio.total_return())



#================================================================


# >>> portfolio = vbt.Portfolio.from_signals(btc_price, entries, exits)
# >>> portfolio.total_return()
# 0.6633185970977526
# ```

# One strategy instance of DMAC produced one column in signals and one performance value.

# Adding one more strategy instance is as simple as adding a new column. Here we are passing an array of
# window sizes instead of a single value. For each window size in this array, it will compute a moving
# average over the entire price series and store it as a distinct column.

# ```python-repl
# >>> # Multiple strategy instances: (10, 30) and (20, 30)
# >>> fast_ma = vbt.MA.run(btc_price, [10, 20], short_name='fast')
# >>> slow_ma = vbt.MA.run(btc_price, [30, 30], short_name='slow')

# >>> entries = fast_ma.ma_above(slow_ma, crossed=True)
# >>> entries
# fast_window     10     20
# slow_window     30     30
# Date
# 2018-12-31   False  False
# 2019-01-01   False  False
# 2019-01-02   False  False
# ...            ...    ...
# 2019-12-29   False  False
# 2019-12-30    True  False
# 2019-12-31   False  False

# [366 rows x 2 columns]

# >>> exits = fast_ma.ma_below(slow_ma, crossed=True)
# >>> exits
# fast_window     10     20
# slow_window     30     30
# Date
# 2018-12-31   False  False
# 2019-01-01   False  False
# 2019-01-02   False  False
# ...            ...    ...
# 2019-12-29   False  False
# 2019-12-30   False  False
# 2019-12-31   False  False

# [366 rows x 2 columns]

# >>> portfolio = vbt.Portfolio.from_signals(btc_price, entries, exits)
# >>> portfolio.total_return()
# fast_window  slow_window
# 10           30             0.865956
# 20           30             0.547047
# dtype: float64
# ```

