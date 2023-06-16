
import backtrader as bt



# Just a basic Strategy skeleton that only prints price, no logic
class SimpleStrategy_3DownPeriods(bt.Strategy):

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

    # The strategy next method will be called on each bar of the system clock (self.datas[0]). 
    # This is true until other things come into play like indicators, which need some bars to start producing an output
    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # strategy logic - If the price has been falling 3 sessions in a row, then buy
        # current close less than previous close
        if self.dataclose[0] < self.dataclose[-1]:
            # previous close less than it's previous close (ie 2 periods ago)
            if self.dataclose[-1] < self.dataclose[-2]:
                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.buy()


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


