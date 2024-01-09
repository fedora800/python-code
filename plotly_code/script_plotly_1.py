
# https://chart-studio.plotly.com/~jackluo/2228/moving-sma-slider-visualization-with-plo/#/

import numpy as np
import pandas as pd
import pandas_datareader.data as web

import plotly.plotly as py
from plotly.graph_objs import *

Select ticker, SMA range, date range and other options

ticker = "GS"
sma_range = 200
log_yaxis = False

# Specify a bit more time because rolling average needs backward data
date_start = "2014-01-01"
date_range_start = "2015-01-01"
date_end = "2016-12-31"

chart_filename = ticker + " " + date_start + " to " + date_end
df = web.get_data_yahoo(ticker, date_start, date_end)

Create Candlestick chart

trace1 = Candlestick(
    x = df.index,
    open = df["Open"],
    high = df["High"],
    low = df["Low"],
    close = df["Close"],
    name = ticker,
)

data = [trace1]

for i in range(5, (sma_range + 1), 5):

    sma = Scatter(
        x = df.index,
        y = df["Close"].rolling(i).mean(), # Pandas SMA
        name = "SMA" + str(i),
        mode = "line",
        line = dict(color = "#3E86AB"),
        opacity = 0.7,
        visible = False,
    )

    data.append(sma)
    

Set up slider and buttons

sliders = dict(

    # GENERAL
    steps = [],
    currentvalue = dict(
        font = dict(size = 16),
        prefix = "SMA: ",
        xanchor = "left",
    ),

    # PLACEMENT
    x = 0.15,
    y = 0,
    len = 0.85,
    pad = dict(t = 0, b = 0),
    yanchor = "bottom",
    xanchor = "left",
)

for i in range((sma_range // 5) + 1):

    step = dict(
        method = "restyle",
        label = str(i * 5),
        value = str(i * 5),
        args = ["visible", [False] * ((sma_range // 5) + 1)], # Sets all to false
    )

    step['args'][1][0] = True # Main trace
    step['args'][1][i] = True # Selected trace through slider
    sliders["steps"].append(step)

updatemenus = dict(

    # GENERAL
    type = "buttons",
    showactive = False,
    x = 0,
    y = 0,
    pad = dict(t = 0, b = 0),
    yanchor = "bottom",
    xanchor = "left",

    # BUTTONS
    buttons=[
        dict(
            method = "restyle",
            label = "Golden Cross",
            args = ["visible", [False] * ((sma_range // 5) + 1)],
        ),
        dict(
            method = "restyle",
            label = "Common SMAs",
            args = ["visible", [False] * ((sma_range // 5) + 1)],
        )
    ],

)

# Set all traces to invisible, then toggle these ones selectively

# Golden cross refers to the 50SMA and 200SMA cross
# and is an indicator of long term market support
updatemenus["buttons"][0]["args"][1][0] = True # Main plot
updatemenus["buttons"][0]["args"][1][10] = True # SMA 50
updatemenus["buttons"][0]["args"][1][40] = True # SMA 200

# Here are other common SMAs used in trading (5, 10, 20, 50 SMA)
updatemenus["buttons"][1]["args"][1][0] = True # Main plot
updatemenus["buttons"][1]["args"][1][1] = True # SMA 5
updatemenus["buttons"][1]["args"][1][2] = True # etc.
updatemenus["buttons"][1]["args"][1][4] = True
updatemenus["buttons"][1]["args"][1][10] = True

Create layout

layout = dict(

    title = chart_filename,

    # GENERAL LAYOUT
    width = 1080,
    height = 720,
    autosize = True,
    font = dict(
        family = "Overpass",
        size = 12,
    ),
    margin = dict(
        t = 80,
        l = 50,
        b = 50,
        r = 50,
        pad = 5,
    ),
    showlegend = False,

    # ANIMATIONS
    sliders = [sliders],
    updatemenus = [updatemenus],

    # COLOR THEME
    plot_bgcolor = "#FFFFFF",
    paper_bgcolor = "#FAFAFA",

    # LINEAR PLOTS
    xaxis = dict(

        # RANGE
        range = [date_range_start, date_end],

        # RANGE SLIDER AND SELECTOR
        rangeslider = dict(
            bordercolor = "#FFFFFF",
            bgcolor = "#FFFFFF",
            thickness = 0.1,
        ),

        # Buttons for date range (1D, 5D, 1M, 3M, 6M, 1Y, 2Y, 5Y, Max, YTD)
        rangeselector = dict(
            activecolor = "#888888",
            bgcolor = "#DDDDDD",
            buttons = [
                dict(count = 1, step = "day", stepmode = "backward", label = "1D"),
                dict(count = 5, step = "day", stepmode = "backward", label = "5D"),
                dict(count = 1, step = "month", stepmode = "backward", label = "1M"),
                dict(count = 3, step = "month", stepmode = "backward", label = "3M"),
                dict(count = 6, step = "month", stepmode = "backward", label = "6M"),
                dict(count = 1, step = "year", stepmode = "backward", label = "1Y"),
                dict(count = 2, step = "year", stepmode = "backward", label = "2Y"),
                dict(count = 5, step = "year", stepmode = "backward", label = "5Y"),
                dict(count = 1, step = "all", stepmode = "backward", label = "MAX"),
                dict(count = 1, step = "year", stepmode = "todate", label = "YTD"),
            ]
        ),

    ),
    yaxis = dict(
        tickprefix = "$",
        type = "linear",
        domain = [0.25, 1],
    ),

)

if log_yaxis: layout["yaxis"]["type"] = "log"

Upload graph

figure = dict(data=data, layout=layout)
py.iplot(figure, filename=chart_filename, fileopt="overwrite")



