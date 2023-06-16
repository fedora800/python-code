
import backtrader as bt



# Just a basic Strategy from backtrader example documentation with my notes and additional logging 
# https://www.backtrader.com/docu/quickstart/quickstart/
class SimpleStrategy_SMACrossOver(bt.Strategy):
    params = (
        ('maperiod', 15),
        ('exitbars', 5),
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    # Upon init being called the strategy already has a list of datas that are present in the platform
    # This is a standard Python list and datas can be accessed in the order they were inserted.
    # The first data in the list self.datas[0] is the default data for trading operations and to keep all strategy elements synchronized (it’s the system clock)
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        # self.dataclose = self.datas[0].close keeps a reference to the close line. Only one level of indirection is later needed to access the close values.
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.maperiod)


    # The strategy next method will be called on each bar of the system clock (self.datas[0]). 
    # This is true until other things come into play like indicators, which need some bars to start producing an output
    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        #self.log('(next) order = %s' % self.order)    # to review how and when this prints
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are already in a position, in which case, we SELL
        if self.position:
            # Basic sell strategy of selling after holding for a fixed (5) defined in params periods
            if len(self) >= (self.bar_executed + self.params.exitbars):
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('(next) SELL CREATE, %.2f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()            
        else:
            # no position, so good to initiate a buy position
            # strategy logic - if close price is above the SMA period defined by params
            # current close less than previous close
            if self.dataclose[0] > self.sma[0]:
                # BUY, BUY, BUY!!! (with all possible default parameters)
                # But note, order creation criteria has been met but it is unknown if it was executed, when and at what price and how many shares
                self.log('(next) BUY CREATE, %.2f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

    def notify_order(self, order):
        self.log('(notify_order) order status = %s' % order.status)
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '(notify_order) BUY EXECUTED, Price: %.2f, Size: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price, order.executed.size,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('(notify_order) SELL EXECUTED, Price: %.2f, Size: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price, order.executed.size,
                          order.executed.value,
                          order.executed.comm))
            self.bar_executed = len(self)
            self.log('(notify_order) Executed at bar : %.2f' % self.bar_executed)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('(notify_order) Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        self.log('(notify_trade) order status = %.2f' % trade.status)    # dont see this after a buy/sell executed, as i would expect, need to see later
        if not trade.isclosed:
            return

        self.log('(notify_trade) OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))


class MAcrossover(bt.Strategy): 
    # Moving average parameters
    params = (('pfast',20),('pslow',50),)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}') # Comment this line when running optimization

    def __init__(self):
        self.dataclose = self.datas[0].close
        
		# Order variable will contain ongoing order details/status
        # We’ve created an order variable which will store ongoing order details and the order status. This way we will know if we are currently in a trade or if an order is pending
        self.order = None

        # Instantiate moving averages
        self.slow_sma = bt.indicators.MovingAverageSimple(self.datas[0], 
                        period=self.params.pslow)
        self.fast_sma = bt.indicators.MovingAverageSimple(self.datas[0], 
                        period=self.params.pfast)
    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])


