# https://algotrading101.com/learn/backtrader-for-backtesting/

from __future__ import (absolute_import, division, print_function, unicode_literals)
from strategies import *

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

import backtrader as bt


# Just a basic Strategy skeleton that only prints price, no logic
class TestStrategy(bt.Strategy):

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


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    #cerebro.addstrategy(TestStrategy)
    cerebro.addstrategy(SimpleStrategy_3DownPeriods)
    #cerebro.addstrategy(MAcrossover)
    # TODO - print the strategy name

    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname='TSLA.csv',
        fromdate=datetime.datetime(2022, 1, 1),
        todate=datetime.datetime(2022, 3, 31)
    )

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
