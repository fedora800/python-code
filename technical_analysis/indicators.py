





    '''
    # Create RSI
    rsi = RSI(data.close, timeperiod=14)

    # Create MACD
    macd, macdsignal, macdhist = MACD(
        data.close, 
        fastperiod=12, 
        slowperiod=26, 
        signalperiod=9
    )

    macd = pd.DataFrame(
        {
            "MACD": macd,
            "MACD Signal": macdsignal,
            "MACD History": macdhist,
        }
    )
    https://pyquantnews.com/technical-df_macd-python-3-indicators/
    https://tradewithpython.com/generating-buy-sell-signals-using-python
    https://www.exfinsis.com/tutorials/python-programming-language/macd-stock-technical-indicator-with-python/


    # Plotting MACD
    plt.subplot(2, 1, 2)
    plt.plot(data['MACD'], label='MACD Line', color='blue')
    plt.plot(data['MACD_Signal'], label='Signal Line', color='red')
    plt.bar(data.index, data['MACD_Diff'], label='Histogram', color='grey', alpha=0.5)
    plt.legend()
    '''
