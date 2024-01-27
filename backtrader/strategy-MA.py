import backtrader as bt
import backtrader.analyzers as btanalyzers
import datetime


class EMACrossStrategy(bt.Strategy):
    params = (("fast_length", 13), ("slow_length", 50))

    def __init__(self):
        self.crossovers = []
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add the 2 EMA indicators
        self.ema_fast = bt.indicators.ExponentialMovingAverage(
            self.datas[0], period=self.params.fast_length
        )
        self.ema_slow = bt.indicators.ExponentialMovingAverage(
            self.datas[0], period=self.params.slow_length
        )

        # for d in self.datas:
        #     ma_fast = bt.ind.EMA(d, period = self.params.fast_length)
        #     ma_slow = bt.ind.EMA(d, period = self.params.slow_length)

        #     self.crossovers.append(bt.ind.CrossOver(ma_fast, ma_slow))

        # Indicators for the plotting show
        # bt.indicators.MovingAverageSimple(self.datas[0], period=200)
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25, subplot=True)
        bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
        bt.indicators.ATR(self.datas[0], plot=False)

    def log(self, txt, dt=None):
        """Logging function for this strategy"""
        dt = dt or self.datas[0].datetime.date(0)
        print("%s, %s" % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    "BUY EXECUTED, Size: %.2f, Price: %.2f, Cost: %.2f, Comm %.2f"
                    % (
                        order.executed.size,
                        order.executed.price,
                        order.executed.value,
                        order.executed.comm,
                    )
                )

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log(
                    "SELL EXECUTED, Size: %.2f, Price: %.2f, Cost: %.2f, Comm %.2f"
                    % (
                        order.executed.size,
                        order.executed.price,
                        order.executed.value,
                        order.executed.comm,
                    )
                )

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log("OPERATION PROFIT, GROSS %.2f, NET %.2f" % (trade.pnl, trade.pnlcomm))
        self.log(
            "-------------------------------------------------------------------------------"
        )

    def next(self):
        # for i, d in enumerate(self.datas):
        #     if not self.getposition(d).size:
        #         if self.crossovers[i] > 0:
        #             self.buy(data = d)
        #             # BUY
        #             self.log('Buy condition met - raising new open order for next bar, %.2f' % self.dataclose[0])
        #     elif self.crossovers[i] < 0:
        #         self.close(data = d)
        #         # CLOSE OUT POSITION
        #         self.log('Exit condition met - raising close position order for next bar, %.2f' % self.dataclose[0])
        # # Simply log the closing price of the series from the reference
        # #self.log('Close, %.2f' % self.dataclose[0])

        # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # Not yet ... we MIGHT BUY if ...
            if self.ema_fast[0] >= self.ema_slow[0]:
                # BUY
                self.log(
                    "Buy condition met - raising new open order for next bar, %.2f"
                    % self.dataclose[0]
                )
                self.log(
                    "ema_fast=%.2f, ema_slow=%.2f"
                    % (self.ema_fast[0], self.ema_slow[0])
                )  # for debug

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:
            if self.ema_fast[0] < self.ema_slow[0]:
                # CLOSE OUT POSITION
                self.log(
                    "Exit condition met - raising close position order for next bar, %.2f"
                    % self.dataclose[0]
                )
                self.log(
                    "ema_fast=%.2f, ema_slow=%.2f"
                    % (self.ema_fast[0], self.ema_slow[0])
                )  # for debug

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()

    # stop method will be called when the data has been exhausted and resultstesting is over.
    # It’s used to print the final net value of the portfolio in the broker (it was done in Cerebro previously)
    def stop(self):
        # self.log('(EMA Period fast %2d ans slow %2d ) Ending Value %.2f' %
        #          (self.params.fast_length, self.params.slow_length, self.broker.getvalue()), doprint=True)
        self.log(
            "(EMA Period fast %2d and slow %2d ) Ending Value %.2f"
            % (self.params.fast_length, self.params.slow_length, self.broker.getvalue())
        )


cerebro = bt.Cerebro()

# Load data from the CSV file
data = bt.feeds.GenericCSVData(
    dataname="AAPL.csv",  # Replace with the filename of your CSV file
    fromdate=datetime.datetime(2020, 1, 1),  # Replace with the desired start date
    todate=datetime.datetime(2023, 5, 20),  # Replace with the desired end date
    nullvalue=0.0,
    dtformat="%Y-%m-%d",  # Replace with the appropriate date format in your CSV file
    datetime=0,  # Column index of the datetime column in your CSV file
    open=1,  # Column index of the open price column in your CSV file
    high=2,  # Column index of the high price column in your CSV file
    low=3,  # Column index of the low price column in your CSV file
    close=4,  # Column index of the close price column in your CSV file
    volume=5,  # Column index of the volume column in your CSV file
    openinterest=-1,  # Column index of the open interest column in your CSV file (or -1 if not present)
)
# csv file format -
# Date,Open,High,Low,Close,Volume
# 2020-01-01,100.0,105.0,98.0,102.0,100000
# 2020-01-02,102.5,106.0,100.0,105.0,120000


cerebro.adddata(data)
cerebro.addstrategy(EMACrossStrategy)

# Set our desired cash start
cerebro.broker.setcash(100000.0)


# Add a FixedSize sizer according to the stake
cerebro.addsizer(bt.sizers.FixedSize, stake=100)

# Set the commission - 0.1% ... divide by 100 to remove the %
cerebro.broker.setcommission(commission=0.001)

# Print out the starting conditions
print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())


cerebro.addanalyzer(btanalyzers.SharpeRatio, _name="sharpe")
cerebro.addanalyzer(btanalyzers.Returns, _name="returns")
cerebro.addanalyzer(btanalyzers.Transactions, _name="trans")

results = cerebro.run()
cerebro.plot()

cerebro.broker.getvalue()
results[0].analyzers.returns.get_analysis()["rnorm100"]
results[0].analyzers.sharpe.get_analysis()
results[0].analyzers.trans.get_analysis()

# Print out the final result
print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
# print('Sharpe Ratio: ', results[0].analyzers.sharperatio.get_analysis()['sharperatio'])
print("Sharpe Ratio: ", results[0].analyzers.sharpe.get_analysis())

