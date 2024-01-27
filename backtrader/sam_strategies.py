import backtrader as bt
from sam_indicators import MyCustomIndicator_1

# Backtrader provided Test Stratey
class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)

        # Indicators for the plotting show
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
                                            subplot=True)
        bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
        bt.indicators.ATR(self.datas[0], plot=False)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                print('--order quantity bought=', format(order.size))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                print('--order quantity sold=', format(order.size))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))
        

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.dataclose[0] < self.sma[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()



class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1 = bt.ind.SMA(period=5)
        sma2 = bt.ind.SMA(period=13)
        #price = self.data
        crossover = bt.ind.CrossOver(sma1, sma2)
        # https://www.backtrader.com/docu/signal_strategy/signal_strategy/
        # https://community.backtrader.com/topic/462/strategy-with-signals
        self.signal_add(bt.SIGNAL_LONG, crossover)
        # Plot the custom indicator
        #MyCustomIndicator_1()





class MyCustomStrategy_1(bt.SignalStrategy):
    def __init__(self):
        sma1 = bt.ind.SMA(period=13)
        sma2 = bt.ind.SMA(period=50)
        sma3 = bt.ind.SMA(period=200)
        my_ind = MyCustomIndicator_1()
        self.signal_add(bt.SIGNAL_LONG, my_ind)



# My strategy based off Backtrader provided Test Stratey
# https://www.backtrader.com/docu/strategy/ -- need to read this thoroughly
class SamStrategy_MainTemplate(bt.Strategy):

    params = (
        ('sma_period1', 20),
        ('ema_period1', 5),
        ('ema_period2', 13),
 #       ('wma_period1', 25),
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        # if we had multiple data feeds, 2nd would have been self.datas[1] etc 
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        # As Backtrader iterates through historical data, this variable will get updated with the latest price from dataclose[0]
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        #self.sma1 = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.sma_period1)
        self.ema1 = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema_period1)
        self.ema2 = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema_period2)


        self.macd = bt.indicators.MACD(self.datas[0],
                                       period_me1=self.p.macd1,
                                       period_me2=self.p.macd2,
                                       period_signal=self.p.macdsig)

        # Cross of macd.macd and macd.signal
        self.macdcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)


        # Indicators for the plotting display
        # Any declared indicators will get automatically plotted (if cerebro.plot is called)
        #bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema_period1)
        #bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema_period2)
        #bt.indicators.WeightedMovingAverage(self.datas[0], period=self.params.wma_period1,subplot=True)
        #bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        bt.indicators.DirectionalMovementIndex(self.datas[0])

        # Control market trend
        #self.sma = bt.indicators.SMA(self.data[0], period=self.p.sma_period1)
        #self.smadir = self.sma - self.sma(-self.p.dirperiod)

        #rsi = bt.indicators.RSI(self.datas[0])
        #bt.indicators.SmoothedMovingAverage(rsi, period=10)    # computes and plots this over the RSI
        #bt.indicators.ATR(self.datas[0], plot=False)       # calculate but dont show on plot
        #self.emacross_ind = bt.indicators.CrossOver(self.ema1, self.ema2)      # will plot this emacross_ind as a seperate indicator subplot on the chart
        
        # It should be obvious that the “declarative” approach during __init__ keeps the bloating of next (where the actual strategy work happens) to a minimum.
        # (Don’t forget there is also a speed up factor)
        # D01
        #close_over_sma = self.data.close > sma1
        #close_over_ema = self.data.close > ema1
        #sma_ema_diff = sma1 - ema1
        #buy_sig = bt.And(close_over_sma, close_over_ema, sma_ema_diff > 0)


        # Explain about this strategy
        # TODO : maybe this needs to be a function ?
        print('-'*80)
        #print('Strategy Name : ', SamStrategy_1.__name__) 
        print('Strategy Name : ????') 
        print(f'Buys and Sells on EMA1 ({self.params.ema_period1}) crossover EMA2 ({self.params.ema_period2})')
        print('-'*80)

    def notify_order(self, order):
        #print('notify_order() : order.status=', order.status)

        # from the module -> 
        #  Status = ['Created', 'Submitted', 'Accepted', 'Partial', 'Completed', 'Canceled', 'Expired', 'Margin', 'Rejected',]
        #                   0            1            2         3            4
        # ExecTypes = ['Market', 'Close', 'Limit', 'Stop', 'StopLimit', 'StopTrail', 'StopTrailLimit', 'Historical']
        # OrdTypes = ['Buy', 'Sell']
        #     params = (
        # ('owner', None), ('data', None),
        # ('size', None), ('price', None), ('pricelimit', None),
        # ('exectype', None), ('valid', None), ('tradeid', 0), ('oco', None),
        # ('trailamount', None), ('trailpercent', None),
        # ('parent', None), ('transmit', True),
        # ('simulated', False),
        # # To support historical order evaluation
        # ('histnotify', False),
   
        if order.status in [order.Submitted, order.Accepted]:
            #print('submitted or accepted - nothing to do', order.status)
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # if not order.alive():
        #     self.order = None  # indicate no order is pending

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        # this is set to completed only ifthe open order that was routed to the broker has now been filled by them
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'ORDER NOTIFICATION : BUY EXECUTED - order.ref: %d, order.size: %.2f, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.ref, order.size, order.executed.price, order.executed.value, order.executed.comm))
                #print('--order quantity bought=', format(order.size))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('ORDER NOTIFICATION : SELL EXECUTED - order.ref: %d, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.ref, order.executed.price, order.executed.value, order.executed.comm))
                #print('--order quantity sold=', format(order.size))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('ORDER NOTIFICATION : Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        #print('notify_trade() : trade.status=', trade.status)

        # toprint = (
        #     'ref', 'data', 'tradeid',
        #     'size', 'price', 'value', 'commission', 'pnl', 'pnlcomm',
        #     'justopened', 'isopen', 'isclosed',
        #     'baropen', 'dtopen', 'barclose', 'dtclose', 'barlen',
        #     'historyon', 'history',
        #     'status')
        # status_names = ['Created', 'Open', 'Closed']
        #                        0       1         2

        if not trade.isclosed:
            return

        self.log('TRADE NOTIFICATION - POSITION CLOSED : OPERATION PROFIT, TRADE_REF %d, GROSS %.2f, NET %.2f' % (trade.ref, trade.pnl, trade.pnlcomm))
        #print('notify_trade() 333 : self.order : ', self.order.ref,  self.order.size, self.order.price, trade.pnl, trade.pnlcomm)
        #print('444: ', trade)



    def next(self):
        #This is the most important part of the strategy class as most of our code will get executed here. 
        # This part gets called every time Backtrader iterates over the next new data point.
        #print('Debug-In next() : dt=', self.datas[0].datetime.date(0), ' Close=', self.dataclose[0], 'self.order=', self.order, 'ema1 and ema2 = ', self.ema1[0], self.ema2[0])

        # Simply log the closing price of the series from the reference
        #self.log('Close, %.2f' % self.dataclose[0])
        #print('--1---',len(self))           # len(self) is the bar we are currently on
        #print(self.order)
        #print(self.position)

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            self.log('Order generated is in PENDING state, , not generating another one, Close=%.2f' % self.dataclose[0])
            return

        # Refer to D01
        #if buy_sig:
        #    self.buy()    

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            #if self.dataclose[0] > self.sma1[0]:
            if self.ema1[0] > self.ema2[0]:
                # BUY, BUY, BUY!!! (with all possible default parameters)
                #self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
                #print('next() 111 : self.order=', self.order)          -- gives useful/all the fields of the order
                #print('next() 111 : self.order : ', self.order.ref,  self.order.size, self.order.price, self.order.broker)
                #self.buy(size=0.5)

        else:

            #if self.dataclose[0] < self.sma1[0]:
            if self.ema1[0] < self.ema2[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                #self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
                #print('next() 222 : self.order=', self.order)
                #print('next() 222 : self.order : ', self.order.ref,  self.order.size, self.order.price, self.order.broker)



# https://github.com/amberdata/jupyter-notebook/blob/master/market/Backtest%20BTC_LO_MCD_SMA_STF_Perct_TS.py
class MyMACDCrossStrategy_NOT_WORKING(bt.Strategy):
    params = (
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        ('trailpercent', 0.40),
        ('smaperiod', 30),
        ('dirperiod', 10),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))


    def __init__(self):
        self.dataclose = self.datas[0].close

        self.macd = bt.indicators.MACD(self.datas[0],
                                       period_me1=self.p.macd1,
                                       period_me2=self.p.macd2,
                                       period_signal=self.p.macdsig)

        # Cross of macd.macd and macd.signal
        self.mcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

    def notify_order(self, order):
            if order.status in [order.Submitted, order.Accepted]:
                # Buy/Sell order submitted/accepted to/by broker - Nothing to do
                return

            # Check if an order has been completed
            # Attention: broker could reject order if not enough cash
            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log(
                        'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                        (order.executed.price,
                        order.executed.value,
                        order.executed.comm))
                    print('--order quantity bought=', format(order.size))

                    self.buyprice = order.executed.price
                    self.buycomm = order.executed.comm
                else:  # Sell
                    self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                            (order.executed.price,
                            order.executed.value,
                            order.executed.comm))
                    print('--order quantity sold=', format(order.size))

                self.bar_executed = len(self)

            elif order.status in [order.Canceled, order.Margin, order.Rejected]:
                self.log('Order Canceled/Margin/Rejected')

            # Write down: no pending order
            self.order = None


    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))


    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.mcross[0] > 0.0:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.mcross[0] < 0.0:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


# https://www.backtrader.com/blog/posts/2016-07-30-macd-settings/macd-settings/
class OthersStrategy_01(bt.Strategy):
    '''
    This strategy is loosely based on some of the examples from the Van
    K. Tharp book: *Trade Your Way To Financial Freedom*. The logic:

      - Enter the market if:
        - The MACD.macd line crosses the MACD.signal line to the upside
        - The Simple Moving Average has a negative direction in the last x
          periods (actual value below value x periods ago)

     - Set a stop price x times the ATR value away from the close

     - If in the market:

       - Check if the current close has gone below the stop price. If yes,
         exit.
       - If not, update the stop price if the new stop price would be higher
         than the current
    '''

    params = (
        # Standard MACD Parameters
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        ('atrperiod', 14),  # ATR Period (standard)
        ('atrdist', 3.0),   # ATR distance for stop price
        ('smaperiod', 30),  # SMA Period (pretty standard)
        ('dirperiod', 10),  # Lookback period to consider SMA trend direction
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status == order.Completed:
            pass

        if not order.alive():
            self.order = None  # indicate no order is pending

    def __init__(self):
        self.macd = bt.indicators.MACD(self.data,
                                       period_me1=self.p.macd1,
                                       period_me2=self.p.macd2,
                                       period_signal=self.p.macdsig)

        # Cross of macd.macd and macd.signal
        self.mcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

        # To set the stop price
        self.atr = bt.indicators.ATR(self.data, period=self.p.atrperiod)

        # Control market trend
        self.sma = bt.indicators.SMA(self.data, period=self.p.smaperiod)
        self.smadir = self.sma - self.sma(-self.p.dirperiod)

    def start(self):
        self.order = None  # sentinel to avoid operrations on pending order

    def next(self):
        if self.order:
            return  # pending order execution

        if not self.position:  # not in the market
            if self.mcross[0] > 0.0 and self.smadir < 0.0:
                self.order = self.buy()
                pdist = self.atr[0] * self.p.atrdist
                self.pstop = self.data.close[0] - pdist
                self.log('BUY CREATE, %.2f' % self.data.close[0])
                self.log('INITIAL STOP= %.2f' % self.pstop)


        else:  # in the market
            pclose = self.data.close[0]
            pstop = self.pstop

            if pclose < pstop:
                self.close()  # stop met - get out
                self.log('STOP MET. SELL CREATE, %.2f' % self.data.close[0])


            else:
                pdist = self.atr[0] * self.p.atrdist
                # Update only if greater than
                self.pstop = max(pstop, pclose - pdist)
                print('Stop price now = ', self.pstop)




class MACDStrategyTest2(bt.Strategy):
    params = (
        # Standard MACD Parameters
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status == order.Completed:
            pass

        if not order.alive():
            self.order = None  # indicate no order is pending

    def __init__(self):
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.macd = bt.indicators.MACD(self.datas[0],
                                       period_me1=self.p.macd1,
                                       period_me2=self.p.macd2,
                                       period_signal=self.p.macdsig)

        # Cross of macd.macd and macd.signal
        self.macdcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

    def next(self):
        if self.order:
            return  # pending order execution

        if not self.position:  # not in the market
            if self.macdcross[0] > 0.0:
                self.order = self.buy()
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

        else:  # in the market
            if self.macdcross[0] < 0.0:
                self.order = self.sell()
                self.log('SELL CREATE, %.2f' % self.dataclose[0])



# DMI crossover strategy
class SamStrategy_DMICrossover(bt.Strategy):

    # params not required as for me, the standard ones are fine

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        """     
        # tried a few things myself with adx and dmi but could not get it to work, got stuck with errors
        #self.dmi = bt.indicators.DirectionalMovementIndex(self.datas[0], period=self.p.period, movav=self.p.movav)
        #self.dmi = bt.indicators.DirectionalMovementIndex(self.datas[0])
        #elf.adx = bt.indicators.AverageDirectionalMovementIndex(self.datas[0])
        #print('dt=', self.datas[0].datetime.date(0), ' dmi plus=', self.adx.DIplus, ' dmi minus=', self.adx.DIminus)
        #print(self.dmi.__dict__)
        #print('dt=', self.datas[0].datetime.date(0), ' dmi plus=', self.dmi.DIplus, ' dmi minus=', self.dmi.DIminus)
        #self.dmicross = bt.indicators.CrossOver(self.dmi.DIplus, self.dmi.DIplus)
        #self.dmicross = bt.indicators.CrossOver(self.adx.DIplus, self.adx.DIminus)
        """

        """ 
        # not tried yet as uses TA-lib
        self.adx = bt.talib.ADX(self.datas[0].high, self.datas[0].low, self.datas[0].close)
        self.adx_fast = bt.talib.SMA(self.adx, timeperiod=self.p.pfast)
        self.adx_slow = bt.talib.SMA(self.adx, timeperiod=self.p.pslow)
        self.adx_crossover = bt.ind.CrossOver(
        self.adx_fast, self.adx_slow, plot=True, subplot=True) """

        # below will display ADX, DMI, +DI, -DI as expected into 1 sub-plot
        self.dmi = bt.ind.DMI()
        # below for the crossover computation in the next() function
        self.dmicross = bt.ind.CrossOver(bt.ind.PlusDI(self.datas[0], plot=False), bt.ind.MinusDI(self.datas[0], plot=False))
#       

        # from https://github.com/ChakshuGupta13/technical-indicators-backtesting/blob/master/ADX.py
        #self.adx = bt.ind.ADX()         # alias for AverageDirectionalMovementIndex ?
        #self.dmiplus, self.dmimin = bt.ind.PlusDI(), bt.ind.MinusDI()       # aliases for PlusDirectionalIndicator and MinusDirectionalIndicator ?
        #self.dmicross = bt.ind.CrossOver(self.dmimin, self.dmiplus)   
        #bt.indicators.PlusDI(self.datas[0], plot=False)       # calculate but dont show on plot
        #bt.indicators.MinusDI(self.datas[0], plot=False)       # calculate but dont show on plot
        #print('xxxx=', self.adx, ' dmiplus=', self.dmiplus, ' dmimin=', self.dmimin)

        #self.adx = bt.ind.ADX()
        #self.dmiplus, self.dmimin = bt.ind.PlusDI(), bt.ind.MinusDI()
        #self.dmi = bt.ind.DirectionalMovementIndex()
        #self.crossoverdmi = bt.ind.CrossOver(self.dmimin, self.dmiplus)
        self.rsi = bt.ind.RelativeStrengthIndex()
        

    def notify_order(self, order):
        if order.status == order.Completed:
            pass

        if not order.alive():
            self.order = None  # indicate no order is pending

    def next(self):
        print('Debug-In next() : dt=', self.datas[0].datetime.date(0), ' Close=', self.dataclose[0])
        #print('dmiplus=', self.dmiplus[0], ' dmiminus=', self.dmiminus[0], ' dmicross=', self.dmicross[0])

        if self.order:
            return  # pending order execution

        if not self.position:  # not in the market
            if self.dmicross[0] > 0.0:
                self.order = self.buy()
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

        else:  # in the market
            if self.dmicross[0] < 0.0:
                self.order = self.sell()
                self.log('SELL CREATE, %.2f' % self.dataclose[0])




class SamStrategy_3in1_v1(bt.Strategy):

    # class enumerations 
    NO_CROSS = 0
    CROSSED_UP = 1
    CROSSED_DOWN = -1

    three_ind_cross_last_3bars = 0

    params = (
        # My EMA periods parameters
        ('ema_period1', 5),
        ('ema_period2', 13),
        # Standard MACD Parameters
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        # DMI params not required as standard ones are fine for me
     )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        # if we had multiple data feeds, 2nd would have been self.datas[1] etc 
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        # As Backtrader iterates through historical data, this variable will get updated with the latest price from dataclose[0]
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        

        # Add EMA indicators
        self.ema1 = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema_period1)
        self.ema2 = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema_period2)

        # Add MACD indicators
        self.macd = bt.indicators.MACD(self.datas[0],
                                       period_me1=self.p.macd1,
                                       period_me2=self.p.macd2,
                                       period_signal=self.p.macdsig)

        # Add DMI indicators
        self.dmi = bt.ind.DMI()


        # Indicators for the plotting display
        # Any declared indicators will get automatically plotted (if cerebro.plot is called)
        #bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema_period1)
        #bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema_period2)
        #bt.indicators.WeightedMovingAverage(self.datas[0], period=self.params.wma_period1,subplot=True)
        #bt.indicators.StochasticSlow(self.datas[0])
        #bt.indicators.MACDHisto(self.datas[0])
        #bt.indicators.DirectionalMovementIndex(self.datas[0])
        #ema_crossover = bt.ind.CrossOver(self.params.ema_period1, self.params.ema_period2)

        self.emacross_ind = bt.indicators.CrossOver(self.ema1, self.ema2)      # will plot this emacross_ind as a seperate indicator subplot on the chart
        self.macdcross_ind = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)   # plot this macdcross_ind as a seperate indicator subplot on the chart
        #self.dmicross_ind = bt.ind.CrossOver(bt.ind.PlusDI(self.datas[0], plot=False), bt.ind.MinusDI(self.datas[0], plot=False))
        self.dmicross_ind = bt.ind.CrossOver(bt.ind.PlusDI(self.datas[0]), bt.ind.MinusDI(self.datas[0]))
        #self.dmicross_ind = bt.ind.CrossOver(self.dmi.plusDI, self.DMI.MinusDI)
            #bt.ind.PlusDI(self.datas[0], plot=False), bt.ind.MinusDI(self.datas[0], plot=False))
        self.three_in_one_ind = self.three_ind_cross_last_3bars
        

        # Control market trend
        #self.sma = bt.indicators.SMA(self.data[0], period=self.p.sma_period1)
        #self.smadir = self.sma - self.sma(-self.p.dirperiod)

        #rsi = bt.indicators.RSI(self.datas[0])
        #bt.indicators.SmoothedMovingAverage(rsi, period=10)    # computes and plots this over the RSI
        #bt.indicators.ATR(self.datas[0], plot=False)       # calculate but dont show on plot
        
        # It should be obvious that the “declarative” approach during __init__ keeps the bloating of next (where the actual strategy work happens) to a minimum.
        # (Don’t forget there is also a speed up factor)
        # D01
        #close_over_sma = self.data.close > sma1
        #close_over_ema = self.data.close > ema1
        #sma_ema_diff = sma1 - ema1
        #buy_sig = bt.And(close_over_sma, close_over_ema, sma_ema_diff > 0)


        # Explain about this strategy
        # TODO : maybe this needs to be a function ?
        print('-'*80)
        #print('Strategy Name : ', SamStrategy_1.__name__) 
        print('Strategy Name : ????') 
        print(f'Buys and Sells on EMA1 ({self.params.ema_period1}) crossover EMA2 ({self.params.ema_period2})')
        print('-'*80)

    def notify_order(self, order):
        #print('notify_order() : order.status=', order.status)
   
        if order.status in [order.Submitted, order.Accepted]:
            #print('submitted or accepted - nothing to do', order.status)
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # if not order.alive():
        #     self.order = None  # indicate no order is pending

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'ORDER NOTIFICATION : BUY EXECUTED - order.ref: %d, order.size: %.2f, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.ref, order.size, order.executed.price, order.executed.value, order.executed.comm))
                #print('--order quantity bought=', format(order.size))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('ORDER NOTIFICATION : SELL EXECUTED - order.ref: %d, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.ref, order.executed.price, order.executed.value, order.executed.comm))
                #print('--order quantity sold=', format(order.size))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('ORDER NOTIFICATION : Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        #print('notify_trade() : trade.status=', trade.status)

        # toprint = (
        #     'ref', 'data', 'tradeid',
        #     'size', 'price', 'value', 'commission', 'pnl', 'pnlcomm',
        #     'justopened', 'isopen', 'isclosed',
        #     'baropen', 'dtopen', 'barclose', 'dtclose', 'barlen',
        #     'historyon', 'history',
        #     'status')
        # status_names = ['Created', 'Open', 'Closed']
        #                        0       1         2

        if not trade.isclosed:
            return

        self.log('TRADE NOTIFICATION - POSITION CLOSED : OPERATION PROFIT, TRADE_REF %d, GROSS %.2f, NET %.2f' % (trade.ref, trade.pnl, trade.pnlcomm))
        #print('notify_trade() 333 : self.order : ', self.order.ref,  self.order.size, self.order.price, trade.pnl, trade.pnlcomm)
        #print('444: ', trade)


    def check_ema_cross_last_3bars(self):
        if (self.emacross_ind[0] == 1 or self.emacross_ind[-1] == 1 or self.emacross_ind[-2] == 1):
            #print('--1---emacross UP in last 3 BARS--- curbar=',self.emacross_ind[0], ' 1barago=',self.emacross_ind[-1], ' 2barago=',self.emacross_ind[-2]) 
            return self.CROSSED_UP
        elif (self.emacross_ind[0] == -1 or self.emacross_ind[-1] == -1 or self.emacross_ind[-2] == -1):
            #print('--1---emacross DOWN in last 3 BARS--- curbar=',self.emacross_ind[0], ' 1barago=',self.emacross_ind[-1], ' 2barago=',self.emacross_ind[-2]) 
            return self.CROSSED_DOWN
        else:
            return self.NO_CROSS


    def check_macd_cross_last_3bars(self):
            if (self.macdcross_ind[0] == 1 or self.macdcross_ind[-1] == 1 or self.macdcross_ind[-2] == 1):
                #print('--1---macdcross UP in last 3 BARS--- curbar=',self.macdcross_ind[0], ' 1barago=',self.macdcross_ind[-1], ' 2barago=',self.macdcross_ind[-2])
                return self.CROSSED_UP
            elif (self.macdcross_ind[0] == -1 or self.macdcross_ind[-1] == -1 or self.macdcross_ind[-2] == -1):
                #print('--1---macdcross DOWN in last 3 BARS--- curbar=',self.macdcross_ind[0], ' 1barago=',self.macdcross_ind[-1], ' 2barago=',self.macdcross_ind[-2]) 
                return self.CROSSED_DOWN
            else:
                return self.NO_CROSS

    def check_dmi_cross_last_3bars(self):
            if (self.dmicross_ind[0] == 1 or self.dmicross_ind[-1] == 1 or self.dmicross_ind[-2] == 1):
                #print('--1---macdcross UP in last 3 BARS--- curbar=',self.dmicross_ind[0], ' 1barago=',self.dmicross_ind[-1], ' 2barago=',self.dmicross_ind[-2])
                return self.CROSSED_UP
            elif (self.dmicross_ind[0] == -1 or self.dmicross_ind[-1] == -1 or self.dmicross_ind[-2] == -1):
                #print('--1---macdcross DOWN in last 3 BARS--- curbar=',self.dmicross_ind[0], ' 1barago=',self.dmicross_ind[-1], ' 2barago=',self.dmicross_ind[-2]) 
                return self.CROSSED_DOWN
            else:
                return self.NO_CROSS


    def next(self):
        #This is the most important part of the strategy class as most of our code will get executed here. 
        # This part gets called every time Backtrader iterates over the next new data point.
        print('Debug-In next() : dt=', self.datas[0].datetime.date(0), ' Close=', self.dataclose[0], 'self.order=', self.order, 'ema1 and ema2 = ', self.ema1[0], self.ema2[0])

        # Simply log the closing price of the series from the reference
        #self.log('Close, %.2f' % self.dataclose[0])
        #print('--1---',len(self))           # len(self) is the bar we are currently on
        #print(self.order)
        #print(self.position)
        # print('---1--EMA CROSSOVER FOUND IN LAST 3 BARS--', self.check_ema_cross_last_3bars()) if self.check_ema_cross_last_3bars() != 'NO' else None
        # print('---2--MACD CROSSOVER FOUND IN LAST 3 BARS--', self.check_macd_cross_last_3bars()) if self.check_macd_cross_last_3bars() != 'NO' else None
        # print('---3--DMI CROSSOVER FOUND IN LAST 3 BARS--', self.check_dmi_cross_last_3bars()) if self.check_dmi_cross_last_3bars() != 'NO' else None

        self.three_ind_cross_last_3bars = self.check_ema_cross_last_3bars() + self.check_macd_cross_last_3bars() + self.check_dmi_cross_last_3bars()
        print('--XXX--', self.three_ind_cross_last_3bars) if self.three_ind_cross_last_3bars in [-3, 3] else None

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            self.log('Order generated is in PENDING state, , not generating another one, Close=%.2f' % self.dataclose[0])
            return

        # Refer to D01
        #if buy_sig:
        #    self.buy()    

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            #if self.dataclose[0] > self.sma1[0]:
#            if self.ema1[0] > self.ema2[0]:
            if self.three_ind_cross_last_3bars == 3:
                print('BUY STRATEGY USED = 3 indicators')
                # BUY, BUY, BUY!!! (with all possible default parameters)
                #self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
                #print('next() 111 : self.order=', self.order)          -- gives useful/all the fields of the order
                #print('next() 111 : self.order : ', self.order.ref,  self.order.size, self.order.price, self.order.broker)
                #self.buy(size=0.5)

        else:

            #if self.dataclose[0] < self.sma1[0]:
            if self.ema1[0] < self.ema2[0]:
                print('SELL STRATEGY USED = ema crossover')
            #if self.three_ind_cross_last_3bars == -3:    
                # SELL, SELL, SELL!!! (with all possible default parameters)
                #self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
                #print('next() 222 : self.order=', self.order)
                #print('next() 222 : self.order : ', self.order.ref,  self.order.size, self.order.price, self.order.broker)
