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
