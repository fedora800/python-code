import datetime
import talib as ta
import pandas as pd
import matplotlib.pyplot as plt

symbol='AMZN'
Y_AXIS_SIZE = 12

# date parser lambda/function
dt_parser = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d')
df = pd.read_csv('AMZN.csv', parse_dates=['Date'], date_parser=dt_parser)
df.info()
print(df.head())


# computing the indicators can be done in different ways, like using TA-Lib like below, or just using pandas using its rolling().mean() functions or something else
df['SMA_13'] = ta.SMA(df['Close'], timeperiod=13)
df['SMA_50'] = ta.SMA(df['Close'], timeperiod=50)
df['RSI_14'] = ta.RSI(df['Close'])
#df['ATR_14'] = ta.ATR(df['High'], df['Low'], df['Close'], timeperiod=14)
df['MACD'], df['MACD_SIGNAL'], df['MACD_HIST']  = ta.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
df['DMI_MINUS'] = ta.MINUS_DM(df['High'] , df['Low'] , timeperiod=14)
df['DMI_PLUS'] = ta.PLUS_DM(df['High'] , df['Low'] , timeperiod=14)
df['ADX_14'] = ta.ADX(df['High'] , df['Low'] , df['Close'], timeperiod=14)

df.dropna(inplace=True)
#just keep those fields that are needed
#df = df[['Date', 'Adj Close', 'SMA_13', 'SMA_50', 'RSI_14']]

print(df)
BuySMA = SellSMA = []
for i in range(len(df)):
    # previous day sma was below the other, but today it's above (so crossover above)
    if df.SMA_13.iloc[i] > df.SMA_50.iloc[i] and df.SMA_13.iloc[i-1] < df.SMA_50.iloc[i-1]:
        BuySMA.append(i)
    # previous day sma was above the other, but today it's below (so crossover below)
    elif df.SMA_13.iloc[i] < df.SMA_50.iloc[i] and df.SMA_13.iloc[i-1] > df.SMA_50.iloc[i-1]:
        SellSMA.append(i)



BuyMACD = SellMACD = []
for i in range(len(df)):
    # previous day macd was below the signal line, but today it's above (so crossover above)
    if df.MACD.iloc[i] < df.MACD_SIGNAL.iloc[i] and df.MACD.iloc[i-1] > df.MACD_SIGNAL.iloc[i-1]:
        BuyMACD.append(i)
    # previous day macd was above the signal line, but today it's below (so crossover below)
    elif df.MACD.iloc[i] > df.MACD_SIGNAL.iloc[i] and df.MACD.iloc[i-1] < df.MACD_SIGNAL.iloc[i-1]:
        SellMACD.append(i)



#fig=plt.figure(figsize=(12,8))
#https://www.w3schools.com/python/matplotlib_subplots.asp
# Prepare plot
#fig, (sp1, sp2, sp3) = plt.subplots(3, 1, sharex=True)      # 3 sub-plots all sharing the same X axis values
fig, (sp1, sp2, sp3) = plt.subplots(3)
#sp1.set_ylabel(symbol, size=20)

#size plot
fig.set_size_inches(15,30)

""" # Plot candles
from matplotlib.finance import candlestick_ohlc as candlestick
candlestick(ax1, sec_id_ochl, width=0.5, colorup='g', colordown='r', alpha=1)
 """

# set up the sub_plot 1
#sp1 = plt.subplot(211)
#sp1 = fig.add_subplot(2,1,1)
sp1.plot(df['Adj Close'], label='Stock Price', c='darkgreen', alpha=0.5)     # plots the price
sp1.plot(df['SMA_13'], label='SMA_13', c='blue', alpha=0.9)              # plots this indicator
sp1.plot(df['SMA_50'], label='SMA_50', c='red', alpha=0.9)              # plots this indicator
sp1.scatter(df.iloc[BuySMA].index, df.iloc[BuySMA]['Adj Close'], marker='^', color='g', s=100)
sp1.scatter(df.iloc[SellSMA].index, df.iloc[SellSMA]['Adj Close'], marker='v', color='r', s=100)
sp1.set_title("Stock Price 021-01-01 to 2021-12-31for %s" % symbol, color='yellow', fontsize=8)
sp1.set_xlabel('--Date--', color='pink')
sp1.set_ylabel('--Price--', color='pink')
sp1.set_title('--Title of this subplot--', color='pink')
sp1.grid(True, color='#555555')
#sp1.set_axisbelow(True)
#sp1.set_facecolor('maroon')
#sp1.figure.set_facecolor(#121212')
sp1.tick_params(axis='x', colors='white')
sp1.tick_params(axis='y', colors='white')
sp1.legend(loc = 'lower right')



#sp2.plot(df['ADX'], label='ADX', c='yellow', alpha=0.5)     # plots the price
sp2.plot(df['DMI_MINUS'], label='DMI_MINUS', c='red', alpha=0.9)              # plots this indicator
sp2.plot(df['DMI_PLUS'], label='DMI_PLUS', c='blue', alpha=0.9)              # plots this indicator
#sp2.scatter(df.iloc[BuySMA].index, df.iloc[BuySMA]['Adj Close'], marker='^', color='g', s=100)
#sp12scatter(df.iloc[SellSMA].index, df.iloc[SellSMA]['Adj Close'], marker='v', color='r', s=100)
sp2.set_title("ADX for %s" % symbol, color='yellow', fontsize=8)
sp2.set_xlabel('--Date--', color='pink')
sp2.set_ylabel('--Price--', color='pink')
sp2.axhline(20, linestyle='--', alpha=0.5, color='lightgray')
sp2.set_title('--Title of this subplot--', color='pink')
sp2.grid(True, color='#555555')



"""
# set up the sub_plot 
#sp2 = plt.subplot(212, sharex=sp1)          # shares the same X axis as sub-plot 1
sp2 = fig.add_subplot(212, sharex=sp1)
sp2.set_ylabel('RSI', size=Y_AXIS_SIZE)
plt.plot(df['RSI_14'], label='RSI_14', c='purple', alpha=0.9)              # plots this indicator
sp2.axhline(0, linestyle='--', alpha=0.5, color='#ffaa00')
sp2.axhline(30, linestyle='--', alpha=0.5, color='lightgray')
sp2.axhline(70, linestyle='--', alpha=0.5, color='lightgray')
sp2.set_title("RSI VALUE 2021-01-01 to 2021-12-31 for %s" % symbol, color='blue', fontsize=16)
sp2.grid(True, color='#555555')
sp2.set_axisbelow(True)
sp2.set_facecolor('black')
sp2.figure.set_facecolor('#121212')
sp2.tick_params(axis='x', colors='white')
sp2.tick_params(axis='y', colors='white')
sp2.legend(loc = 'lower right')
"""

""" # set up the sub_plot 
#sp2 = plt.subplot(212, sharex=sp1)          # shares the same X axis as sub-plot 1
#sp2 = fig.add_subplot(212, sharex=sp1)
sp2.set_ylabel('RSI', size=Y_AXIS_SIZE)
sp2.plot(df['RSI_14'], label='RSI_14', c='purple', alpha=0.9)              # plots this indicator
sp2.axhline(0, linestyle='--', alpha=0.5, color='#ffaa00')
sp2.axhline(30, linestyle='--', alpha=0.5, color='lightgray')
sp2.axhline(70, linestyle='--', alpha=0.5, color='lightgray')
sp2.set_title("RSI VALUE 2021-01-01 to 2021-12-31 for %s" % symbol, color='yellow', fontsize=8)
sp2.grid(True, color='#555555')
sp2.set_axisbelow(True)
#sp2.set_facecolor('brown')
sp2.figure.set_facecolor('#121212')
sp2.tick_params(axis='x', colors='white')
sp2.tick_params(axis='y', colors='white')
sp2.legend(loc = 'lower right')
 """
# analysis.rsi.plot(ax = ax2, c='g', label = 'Period: ' + str(RSI_PERIOD))
# analysis.sma_r.plot(ax = ax2, c='r', label = 'MA: ' + str(RSI_AVG_PERIOD))
# sp2.axhline(y=30, c='b')
# sp2.axhline(y=50, c='black')
# sp2.axhline(y=70, c='b')
# sp2.set_ylim([0,100])
# handles, labels = sp2.get_legend_handles_labels()
# sp2.legend(handles, labels)


#RSI
# analysis.rsi.plot(ax = ax2, c='g', label = 'Period: ' + str(RSI_PERIOD))
# analysis.sma_r.plot(ax = ax2, c='r', label = 'MA: ' + str(RSI_AVG_PERIOD))
# ax2.axhline(y=30, c='b')
# ax2.axhline(y=50, c='black')
# ax2.axhline(y=70, c='b')
# ax2.set_ylim([0,100])
#handles, labels = ax2.get_legend_handles_labels()
#ax2.legend(handles, labels)



# set up the sub_plot 3
#sp3 = plt.subplot(213, sharex=sp1)          # shares the same X axis as sub-plot 1
#sp3 = fig.add_subplot(212, sharex=sp1)
sp3.plot(df['MACD'], label='MACD', c='cyan', alpha=0.5)     # plots the price
sp3.plot(df['MACD_SIGNAL'], label='MACD_SIGNAL', c='red', alpha=0.9)              # plots this indicator
sp3.plot(df['MACD_HIST'], label='MACD_HIST', c='darkgray', alpha=0.9)              # plots this indicator
sp3.scatter(df.iloc[BuyMACD].index, df.iloc[BuyMACD]['MACD'], marker='^', color='g', s=100)
sp3.scatter(df.iloc[SellMACD].index, df.iloc[SellMACD]['MACD'], marker='v', color='r', s=100)
sp3.axhline(0, linestyle='--', alpha=0.5, color='#ffaa00')
sp3.set_title("MACD VALUE 2021-01-01 to 2021-12-31 for %s" % symbol, color='yellow', fontsize=8)
sp3.grid(True, color='#555555')
sp3.set_axisbelow(True)
sp3.set_facecolor('black')
sp3.figure.set_facecolor('#121212')
sp3.tick_params(axis='x', colors='white')
sp3.tick_params(axis='y', colors='white')


#plt.legend(loc = 'lower right')
plt.show()

# # Draw MACD computed with Talib
# ax3.set_ylabel('MACD: '+ str(MACD_FAST) + ', ' + str(MACD_SLOW) + ', ' + str(MACD_SIGNAL), size=Y_AXIS_SIZE)
# analysis.macd.plot(ax=ax3, color='b', label='Macd')
# analysis.macdSignal.plot(ax=ax3, color='g', label='Signal')
# analysis.macdHist.plot(ax=ax3, color='r', label='Hist')
# ax3.axhline(0, lw=2, color='0')
# handles, labels = ax3.get_legend_handles_labels()
# ax3.legend(handles, labels)


# # set up the sub_plot 4 --- for future
# # Stochastic plot
# ax4.set_ylabel('Stoch (k,d)', size=Y_AXIS_SIZE)
# analysis.stoch_k.plot(ax=ax4, label='stoch_k:'+ str(STOCH_K), color='r')
# analysis.stoch_d.plot(ax=ax4, label='stoch_d:'+ str(STOCH_D), color='g')
# handles, labels = ax4.get_legend_handles_labels()
# ax4.legend(handles, labels)
# ax4.axhline(y=20, c='b')
# ax4.axhline(y=50, c='black')
# ax4.axhline(y=80, c='b')



# https://medium.com/codex/algorithmic-trading-with-macd-in-python-1c2769a6ad1b 
def plot_macd(prices, macd, signal, hist):
    ax1 = plt.subplot2grid((8,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((8,1), (5,0), rowspan = 3, colspan = 1)

    ax1.plot(prices)
    ax2.plot(macd, color = 'grey', linewidth = 1.5, label = 'MACD')
    ax2.plot(signal, color = 'skyblue', linewidth = 1.5, label = 'SIGNAL')

    for i in range(len(prices)):
        if str(hist[i])[0] == '-':
            ax2.bar(prices.index[i], hist[i], color = '#ef5350')
        else:
            ax2.bar(prices.index[i], hist[i], color = '#26a69a')

    plt.legend(loc = 'lower right')


def abc1():
    ax1 = plt.subplot2grid((8,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((8,1), (5,0), rowspan = 3, colspan = 1)

    ax1.plot(googl['close'], color = 'skyblue', linewidth = 2, label = 'GOOGL')
    ax1.plot(googl.index, buy_price, marker = '^', color = 'green', markersize = 10, label = 'BUY SIGNAL', linewidth = 0)
    ax1.plot(googl.index, SellSMA_price, marker = 'v', color = 'r', markersize = 10, label = 'SellSMA SIGNAL', linewidth = 0)
    ax1.legend()    
    ax1.set_title('GOOGL MACD SIGNALS')
    ax2.plot(googl_macd['macd'], color = 'grey', linewidth = 1.5, label = 'MACD')
    ax2.plot(googl_macd['signal'], color = 'skyblue', linewidth = 1.5, label = 'SIGNAL')

    for i in range(len(googl_macd)):
        if str(googl_macd['hist'][i])[0] == '-':
            ax2.bar(googl_macd.index[i], googl_macd['hist'][i], color = '#ef5350')
        else:
            ax2.bar(googl_macd.index[i], googl_macd['hist'][i], color = '#26a69a')
            
    plt.legend(loc = 'lower right')
    plt.show()


#https://medium.com/codex/increasing-stock-returns-by-combining-williams-r-and-macd-in-python-5af999c90259
#https://matplotlib.org/1.5.3/examples/pylab_examples/finance_work2.html
#https://github.com/mellertson/talib-macd-example/blob/master/talib-macd-matplotlib-example.py          ### VERY GOOD ###


def use_pandas_ta():
    import pandas_ta as ta
    # Request historic pricing data via finance.yahoo.com API
    # Calculate MACD values using the pandas_ta library
    df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
    #                      low  MACD_12_26_9  MACDh_12_26_9  MACDs_12_26_9  
    # also plotly is used - https://www.alpharithms.com/calculate-macd-python-272222/












