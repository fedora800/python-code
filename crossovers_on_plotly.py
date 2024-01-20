import datetime
import talib as ta
import numpy as np
import pandas as pd
import plotly as pl 
import plotly.graph_objects as go
from plotly import subplots


symbol='AMZN'
Y_AXIS_SIZE = 12

# date parser lambda/function
dt_parser = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d')
#df = pd.read_csv('AMZN.csv', parse_dates=['Date'], date_parser=dt_parser)
df = pd.read_csv('AMZN-2yrs.csv', parse_dates=['Date'], date_parser=dt_parser)
#df.info()
#print(df.head())


# computing the indicators can be done in different ways, like using TA-Lib like below, or just using pandas using its rolling().mean() functions or something else
df['SMA_5'] = ta.SMA(df['Close'], timeperiod=5)
df['SMA_13'] = ta.SMA(df['Close'], timeperiod=13)
df['RSI_14'] = ta.RSI(df['Close'])
#df['ATR_14'] = ta.ATR(df['High'], df['Low'], df['Close'], timeperiod=14)
df['MACD'], df['MACD_SIGNAL'], df['MACD_HIST']  = ta.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
df['DMI_MINUS'] = ta.MINUS_DM(df['High'] , df['Low'] , timeperiod=14)
df['DMI_PLUS'] = ta.PLUS_DM(df['High'] , df['Low'] , timeperiod=14)
df['ADX_14'] = ta.ADX(df['High'] , df['Low'] , df['Close'], timeperiod=14)

# add a column that holds 1 or -1 on an SMA values diff
df['SMA_CROSS'] = 0
df['SMA_CROSS'] = np.where(df['SMA_5'] > df['SMA_13'], 1, -1)
print(df['SMA_CROSS'])

## TODO: need to sma_cross for -1 when it crosses below, or is it needed ?

# add a column that holds 1 or -1 on a MACD values diff
df['MACD_CROSS'] = 0
df['MACD_CROSS'] = np.where(df['MACD'] > df['MACD_SIGNAL'], 1, -1)
print(df['MACD_CROSS'])

# add a column that holds 1 or -1 on a DMI values diff
df['DMI_CROSS'] = 0
df['DMI_CROSS'] = np.where(df['DMI_PLUS'] > df['DMI_MINUS'], 1, -1)
print(df['DMI_CROSS'])

# add a column that sums up all 3 of above differences
df['3_IN_1'] = 0
df['3_IN_1'] = df['SMA_CROSS'] + df['MACD_CROSS'] + df['DMI_CROSS']
print(df['3_IN_1'])




df.dropna(inplace=True)
#just keep those fields that are needed
#df = df[['Date', 'Adj Close', 'SMA_5', 'SMA_13', 'RSI_14']]

print(df)
BuySMA = SellSMA = []
for i in range(len(df)):
    # previous day sma was below the other, but today it's above (so crossover above)
    if df.SMA_5.iloc[i] > df.SMA_13.iloc[i] and df.SMA_5.iloc[i-1] < df.SMA_13.iloc[i-1]:
        BuySMA.append(i)
    # previous day sma was above the other, but today it's below (so crossover below)
    elif df.SMA_5.iloc[i] < df.SMA_13.iloc[i] and df.SMA_5.iloc[i-1] > df.SMA_13.iloc[i-1]:
        SellSMA.append(i)

BuyMACD = SellMACD = []
for i in range(len(df)):
    # previous day macd was below the signal line, but today it's above (so crossover above)
    if df.MACD.iloc[i] < df.MACD_SIGNAL.iloc[i] and df.MACD.iloc[i-1] > df.MACD_SIGNAL.iloc[i-1]:
        BuyMACD.append(i)
    # previous day macd was above the signal line, but today it's below (so crossover below)
    elif df.MACD.iloc[i] > df.MACD_SIGNAL.iloc[i] and df.MACD.iloc[i-1] < df.MACD_SIGNAL.iloc[i-1]:
        SellMACD.append(i)

fig = go.Figure()
#NUM_OF_SUBPLOTS = 7
NUM_OF_SUBPLOTS = 2
# fig = subplots.make_subplots(rows=NUM_OF_SUBPLOTS, cols=1, subplot_titles=('subplot-title-1-PRICE', 'subplot-title-2-RSI', 'subplot-title-3-MACD' ),
#                     shared_xaxes=False)
fig = subplots.make_subplots(rows=NUM_OF_SUBPLOTS, cols=1, shared_xaxes=False)

# Create and style the traces                    
# configure to show the price chart first (1st row), this will be 3 ie PRICE, SMA_5 and SMA_13
SUBPLOT_ROW_POSITION = 1
SUBPLOT_COL_POSITION = 1
trace_11 = go.Scatter(x=df['Date'], y=df['Close'], name="PRICE_legend", line=dict(color='black', width=3) )
fig.append_trace(trace_11, row=SUBPLOT_ROW_POSITION, col=SUBPLOT_COL_POSITION)
trace_12 = go.Scatter(x=df['Date'], y=df['SMA_5'], name="SMA_5_legend", line=dict(color='blue', width=2))
fig.append_trace(trace_12, row=SUBPLOT_ROW_POSITION, col=SUBPLOT_COL_POSITION)
trace_13 = go.Scatter(x=df['Date'], y=df['SMA_13'], name="SMA_13_legend", line=dict(color='red', width=2))
fig.append_trace(trace_13, row=SUBPLOT_ROW_POSITION, col=SUBPLOT_COL_POSITION)

#trace_14 = go.Scatter(x=df['Date'], y=df['SMA_CROSS'], name="SMA_CROSS_legend", line=dict(color='purple', width=2))
#trace_14 = go.Scatter(x=df['Date'], y=df[df['SMA_CROSS'] ==1].index, name="SMA_CROSS_legend", line=dict(color='purple', width=2))
#fig.append_trace(trace_14, row=SUBPLOT_ROW_POSITION, col=SUBPLOT_COL_POSITION)

# configure to show the RSI next (2nd row)
SUBPLOT_ROW_POSITION = 2
SUBPLOT_COL_POSITION = 1
#trace_21 = go.Scatter(x=df['Date'], y=df['RSI_14'])
#fig.append_trace(trace_21, row=SUBPLOT_ROW_POSITION, col=SUBPLOT_COL_POSITION)
# # configure to show the MACD next (3rd row), this comprises of 3 seperate indicators on 1 sub-plot
SUBPLOT_ROW_POSITION = 3
SUBPLOT_COL_POSITION = 1
#trace_31 = go.Scatter(x=df['Date'], y=df['MACD'], name="MY_MACD_name_legend", line=dict(color='blue', width=2))
#fig.append_trace(trace_31, row=SUBPLOT_ROW_POSITION, col=SUBPLOT_COL_POSITION)
#trace_32 = go.Scatter(x=df['Date'], y=df['MACD_SIGNAL'], name="MACD_SIGNAL_legend", line=dict(color='red', width=2))
#fig.append_trace(trace_32, row=SUBPLOT_ROW_POSITION, col=SUBPLOT_COL_POSITION)
#trace_33 = go.Bar(x=df['Date'], y=df['MACD_HIST'], name="MACD_HIST_legend")
#fig.append_trace(trace_33, row=SUBPLOT_ROW_POSITION, col=SUBPLOT_COL_POSITION)

# configure to show the SMA cross indicator
SUBPLOT_ROW_POSITION = 4
SUBPLOT_COL_POSITION = 1
#trace_41 = go.Scatter(x=df['Date'], y=df['SMA_CROSS'], name="SMA_CROSS_legend",line=dict(color='darkgreen', width=2))
#fig.append_trace(trace_41, row=SUBPLOT_ROW_POSITION, col=SUBPLOT_COL_POSITION)

# configure to show the MACD cross indicator
SUBPLOT_ROW_POSITION = 5
SUBPLOT_COL_POSITION = 1
#trace_51 = go.Scatter(x=df['Date'], y=df['MACD_CROSS'], name="MACD_CROSS_legend",line=dict(color='rosybrown', width=2))
#fig.append_trace(trace_51, row=SUBPLOT_ROW_POSITION, col=SUBPLOT_COL_POSITION)

# configure to show the DMI cross indicator
SUBPLOT_ROW_POSITION = 6
SUBPLOT_COL_POSITION = 1
#trace_61 = go.Scatter(x=df['Date'], y=df['DMI_CROSS'], name="DMI_CROSS_legend",line=dict(color='indianred', width=2))
#fig.append_trace(trace_61, row=SUBPLOT_ROW_POSITION, col=SUBPLOT_COL_POSITION)


# configure to show the 3_IN_1 indicator
#SUBPLOT_ROW_POSITION = 7
SUBPLOT_ROW_POSITION = 2
SUBPLOT_COL_POSITION = 1
trace_71 = go.Scatter(x=df['Date'], y=df['3_IN_1'], name="3_IN_1_legend",line=dict(color='orange', width=4))
fig.append_trace(trace_71, row=SUBPLOT_ROW_POSITION, col=SUBPLOT_COL_POSITION)


fig.show()


"""
fig = go.Figure()
data = [gobj.Candlestick(x = df['Date'], 
                                               open = df['Open'], 
                                               high = df['High'], 
                                               low = df['Low'], 
                                               close = df['Close'])
                                  ]
                        )

fig.update_layout(xaxis_rangeslider_visible = False, title = 'AMAZON SHARE PRICE (2020-2021)')
fig.update_xaxes(title_text = 'Date')
fig.update_yaxes(title_text = 'AMZN Close Price', tickprefix = '$')
fig.show()
"""

"""
fig = go.Figure()
#Add two Scatter traces to a figure
# this will create all the plots as seperate subplots on 1 page, spaces in between each subplot
# fig.add_traces([go.Scatter(x=[1,2,3], y=[5,7,9]),
#                 go.Scatter(x=[1,2,3], y=[2,4,6])]) 

#Add two Scatter traces to vertically stacked subplots
fig = subplots.make_subplots(rows=2)
fig.add_traces([go.Scatter(x=[1,2,3], y=[2,1,2]),
                go.Scatter(x=[1,2,3], y=[2,1,2])],
                rows=[1, 2], cols=[1, 1]) 
fig.show()
"""


""" 
## this will create all the plots in 1 chart, with no spaces in between the subplots 
np.random.seed(1)
N = 100
random_x = np.linspace(0, 1, N)
random_y0 = np.random.randn(N) + 5
random_y1 = np.random.randn(N)
random_y2 = np.random.randn(N) - 5

# Create traces
fig = go.Figure()
fig.add_trace(go.Scatter(x=random_x, y=random_y0,
                    mode='lines',
                    name='lines'))
fig.add_trace(go.Scatter(x=random_x, y=random_y1,
                    mode='lines+markers',
                    name='lines+markers'))
fig.add_trace(go.Scatter(x=random_x, y=random_y2,
                    mode='markers', name='markers')) 
                    

# -- this code will fill the rsi subplot with a different color from 30 to 70 horizontal lines                    
#set the high and low lines (as columns)
df['low'] = 30
df['high'] = 70
df.head(20)                    
fig.add_trace(go.Scatter(x=df['Date'], y=df['high'],
                         fill=None,
                         mode='lines',
                         line=dict(width=0.5, color='rgb(222, 196, 255)', dash='dash')))
fig.add_trace(go.Scatter(x=df['Date'],y=df['low'],
                         fill='tonexty', # fill area between trace0 and trace1
                         mode='lines',
                         line=dict(width=0.5, color='rgb(222, 196, 255)', dash='dash')))                    
# --                    
                    
# background color changes via layout - but below is R code
https://jtr13.github.io/cc19/technical-analysis-for-stocks-using-plotly.html
plot3 <- plot2 %>% layout(paper_bgcolor='rgba(37,37,37,1)',
                          plot_bgcolor='rgba(37,37,37,1)',
                          margin = list(l=60, r=20, t=30, b=5))


                    """

# for plotly
# https://plotly.com/python/line-charts/
# https://people.cam.cornell.edu/md825/ORIE6125/week12/data_visualization.html
# https://blog.devgenius.io/overlaying-the-relative-strength-index-rsi-on-multiple-stocks-crypto-in-python-64a46f9837a1
# https://chart-studio.plotly.com/~xdxxq/41/simple-moving-averages/#code




