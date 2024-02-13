def generate_chart_plot_with_sub_plots(df):
    """
    TODO
    https://stackoverflow.com/questions/64689342/plotly-how-to-add-volume-to-a-candlestick-chart
    https://web3-ethereum-defi.readthedocs.io/tutorials/uniswap-v3-price-df_macd.html
    """

    candlesticks = gobj.Candlestick(
        x=df["pd_time"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        showlegend=False,
    )

    volume_bars = gobj.Bar(
        x=df["pd_time"],
        y=df["volume"],
        showlegend=False,
        marker={
            "color": "rgba(128,128,128,0.5)",
        },
    )

    fig = gobj.Figure(candlesticks)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(candlesticks, secondary_y=True)
    fig.add_trace(volume_bars, secondary_y=False)
    fig.update_layout(
        title="ETH/USDC pool price data at the very beginning of Uniswap v3",
        height=800,
        # Hide Plotly scrolling minimap below the price chart
        xaxis={"rangeslider": {"visible": False}},
    )
    fig.update_yaxes(title="Price $", secondary_y=True, showgrid=True)
    fig.update_yaxes(title="Volume $", secondary_y=False, showgrid=False)

    #  fig.show()

    # Render plot using plotly_chart
    st.plotly_chart(
        fig, width=1100, height=600
    )  # make sure to increase this appropriately with the other objects
    logger.info("plotly on streamlit main chart rendered")








def generate_chart_plot(df):
    # this works
    #  fig = gobj.Figure(data=[gobj.Candlestick(x=df['pd_time'],
    #                                       open=df['open'],
    #                                       high=df['high'],
    #                                       low=df['low'],
    #                                       close=df['close']
    #                                      ),
    #                        gobj.Scatter(x=df['pd_time'], y=df['sma_50'], line=dict(color='red', width=2))  # plots the moving average on top as a scatter plot
    #                       ]
    #                 )

    # Create a gobj.Candlestick object, assign these fields and then assign it to a variable named chart_data
    chart_data = gobj.Candlestick(
        x=df["pd_time"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        decreasing_line_color= 'pink',
    )

    #  layout = go.Layout(
    #      autosize=False,
    #      width=1000,
    #      height=1000,
    #      xaxis=go.layout.XAxis(linecolor="black", linewidth=1, mirror=True),
    #      yaxis=go.layout.YAxis(linecolor="black", linewidth=1, mirror=True),
    #      margin=go.layout.Margin(l=50, r=50, b=100, t=100, pad=4),
    #  )
    #
    #  fig = go.Figure(data=data, layout=layout)

    # Now create a gobj.Figure called fig to display the data. Create this object passing in chart_data and assigning it to a variable named fig:
    fig = gobj.Figure(data=[chart_data])

    # To plot the moving average on top of this chart/figure, create a gobj.Scatter object, setting x with the same df time and y with the movavg df.
    # we can also specify other settings like mode, colour, width etc
    # name value is what we will see as the the label/legend on the side of the chart, the sma line can have its own properties defined by a dict below
    # marker=dict(size=25, color=color_4, symbol=marker_list_2, line=dict(width=0.5))
    dct_textfont = dict(color="black", size=18, family="Times New Roman")
    trace_ema_13 = gobj.Scatter(
        x=df["pd_time"],
        y=df["ema_13"],
        mode="lines",
        name="13-EMA",
        textfont=dct_textfont,
        line=dict(color="purple", width=2),
    )
    trace_sma_50 = gobj.Scatter(
        x=df["pd_time"],
        y=df["sma_50"],
        mode="lines",
        name="50-SMA",
        textfont=dct_textfont,
        line=dict(color="blue", width=2),
    )
    trace_sma_200 = gobj.Scatter(
        x=df["pd_time"],
        y=df["sma_200"],
        mode="lines",
        name="200-SMA",
        textfont=dct_textfont,
        line=dict(color="red", width=2),
    )

    # To add the new scatter plot, call fig.add_trace and pass in the various trace objects
    fig.add_trace(trace_ema_13)
    fig.add_trace(trace_sma_50)
    fig.add_trace(trace_sma_200)

    # Do not show OHLC's rangeslider sub plot
    fig.update_layout(xaxis_rangeslider_visible=False)

    dct_y_axis = dict(
        title_text="Y-axis Title for the Symbol Chart",  # this text will appear 180 turned on the left of the y axis
        titlefont=dict(size=30),  # font size for title_text
        #  tickvals=[100, 200, 300, 400],                     # these will be fixed horizontal lines on the chart at the defined values
        #  ticktext=["pricelevel 100", "pricelevel 200", "pricelevel 300 (getting expensive)", "pricelevel 400"],   # for the tickvals, these texts will appear on the left
        #  tickmode="array",
    )
    # dct_margin = dict(l=20, r=20, t=20, b=20)
    fig.update_layout(
        width=1100,
        height=600,
        yaxis=dct_y_axis,
        #    margin=dct_margin,
        #    paper_bgcolor="LightSteelBlue"
    )
    # fig.update_layout(width=1100, height=900)            # default size of chart is small, increase it
    # fig.show()

    # Render plot using plotly_chart
    st.plotly_chart(
        fig, width=1100, height=600
    )  # make sure to increase this appropriately with the other objects


# plot the candlesticks


#  ----
#                 # Add the moving average
#                 gobj.Scatter(x=stock_data['moving3'].index,
#                            y=stock_data['moving3']),
#                 gobj.Scatter(x=stock_data['moving8'].index,
#                            y=stock_data['moving8'])
#                 ])
#
# # Mask a default range slider
# fig.update_layout(xaxis_rangeslider_visible=False)
#
#
# # Set layout size
# fig.update_layout(
#     autosize=False,
#     width=600,
#     height=500,
#     legend=dict(
#         x=0.82,  # Adjust the legend's x position
#         y=0.98,  # Adjust the legend's y position
#         font=dict(size=12)  # Customize font size
#     )
# )
#  ---


    # Remove the default horizontal lines at RSI levels 30, 40, 60, and 70
    fig.update_yaxes(
        rangemode="tozero",  # This ensures that the y-axis starts from 0
        range=[0, 100],  # Customize the y-axis range if needed
        #range=[df["low"].min(), df["high"].max()]    # for the low/high prices to scale the full y-axis instead of squished
        row=3,
        col=1,  # Specify the subplot
        # showgrid=False,  # Hide grid lines
        # zeroline=False,  # Hide the zero line
        # showline=False,  # Hide the axis line
        ticks="",  # Hide tick marks
    )

    #     # Update the layout for X-axis so that weekends and holidays (shows gaps on chart) are omitted from plotting
    #     fig.update_xaxes(
    #         rangebreaks = [
    #             # NOTE: Below values are bound (not single values), ie. hide x to y
    #             dict(bounds=["sat", "mon"]),                 # hide weekends, eg. hide sat to before mon
    #             dict(bounds=[16, 9.5], pattern="hour"),      # hide hours outside of 9.30am-4pm
    #             # dict(values=["2023-12-25", "2024-01-01"])  # hide holidays (Christmas and New Year's, etc)
    #         ]
    #     )