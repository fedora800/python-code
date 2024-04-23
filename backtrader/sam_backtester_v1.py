from __future__ import (absolute_import, division, print_function, unicode_literals)
import datetime
import argparse
import pandas as pd
import backtrader as bt
import matplotlib.pyplot as plt
import sam_strategies as sam_st

 #import OthersStrategy_01, SamStrategy_DMICrossover, MACDStrategyTest2, SamStrategy_MainTemplate, SmaCross

PORTFOLIO_STARTING_AMOUNT = 100000.0
#SYMBOLFILE='BTC-USD.csv'
SYMBOLFILE='TSLA.csv'
#STRATEGY_NAME='SamStrategy_1'
STRATEGY_NAME='SamStrategy_DMICrossover'
TRAILING_STOP_PCT = 0.40
BTVERSION = tuple(int(x) for x in bt.__version__.split('.'))

DATASETS = {
    'dsAMZN': 'AMZN.csv',
    'dsPEP' : 'PEP.csv',
    'dsXOM' : 'XOM.csv',
}

class FixedPerc(bt.Sizer):
    '''This sizer simply returns a fixed size for any operation

    Params:
      - ``perc`` (default: ``0.20``) Perc of cash to allocate for operation
    '''

    params = (
        ('perc', 0.20),  # perc of cash to use for operation
    )

    def _getsizing(self, comminfo, cash, data, isbuy):
        cashtouse = self.p.perc * cash
        if BTVERSION > (1, 7, 1, 93):
            size = comminfo.getsize(data.close[0], cashtouse)
        else:
            size = cashtouse // data.close[0]
        return size


def printTradeAnalysis_A(analyzer):
    '''
    Function to print the Technical Analysis results in a nice format.
    '''
    #Get the results we are interested in
    total_open = analyzer.total.open
    total_closed = analyzer.total.closed
    total_won = analyzer.won.total
    total_lost = analyzer.lost.total
    win_streak = analyzer.streak.won.longest
    lose_streak = analyzer.streak.lost.longest
    pnl_net = round(analyzer.pnl.net.total,2)
    strike_rate = (total_won / total_closed) * 100
    #Designate the rows
    h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
    h2 = ['Strike Rate','Win Streak', 'Losing Streak', 'PnL Net']
    r1 = [total_open, total_closed,total_won,total_lost]
    r2 = [strike_rate, win_streak, lose_streak, pnl_net]
    #Check which set of headers is the longest.
    if len(h1) > len(h2):
        header_length = len(h1)
    else:
        header_length = len(h2)
    #Print the rows
    print_list = [h1,r1,h2,r2]
    row_format ="{:<15}" * (header_length + 1)
    print("Trade Analysis Results:")
    for row in print_list:
        print(row_format.format('',*row))


def printSQN_A(analyzer):
    sqn = round(analyzer.sqn,2)
    print('SQN: {}'.format(sqn))


def pretty_print(format, *args):
    print(format.format(*args))

def exists(object, *properties):
    for property in properties:
        if not property in object: return False
        object = object.get(property)
    return True

def printTradeAnalysis_B(cerebro, analyzers):
    format = "  {:<24} : {:<24}"
    NA     = '-'

    print('printTradeAnalysis_B() : Backtesting Results')
    if hasattr(analyzers, 'ta'):
        ta = analyzers.ta.get_analysis()

        openTotal         = ta.total.open          if exists(ta, 'total', 'open'  ) else None
        closedTotal       = ta.total.closed        if exists(ta, 'total', 'closed') else None
        wonTotal          = ta.won.total           if exists(ta, 'won',   'total' ) else None
        lostTotal         = ta.lost.total          if exists(ta, 'lost',  'total' ) else None

        streakWonLongest  = ta.streak.won.longest  if exists(ta, 'streak', 'won',  'longest') else None
        streakLostLongest = ta.streak.lost.longest if exists(ta, 'streak', 'lost', 'longest') else None

        pnlNetTotal       = ta.pnl.net.total       if exists(ta, 'pnl', 'net', 'total'  ) else None
        pnlNetAverage     = ta.pnl.net.average     if exists(ta, 'pnl', 'net', 'average') else None

        pretty_print(format, 'Open Positions', openTotal   or NA)
        pretty_print(format, 'Closed Trades',  closedTotal or NA)
        pretty_print(format, 'Winning Trades', wonTotal    or NA)
        pretty_print(format, 'Loosing Trades', lostTotal   or NA)
        print('\n')

        pretty_print(format, 'Longest Winning Streak',   streakWonLongest  or NA)
        pretty_print(format, 'Longest Loosing Streak',   streakLostLongest or NA)
        pretty_print(format, 'Strike Rate (Win/closed)', (wonTotal / closedTotal) * 100 if wonTotal and closedTotal else NA)
        print('\n')

        pretty_print(format, 'Inital Portfolio Value', '${}'.format(PORTFOLIO_STARTING_AMOUNT))
        pretty_print(format, 'Final Portfolio Value',  '${}'.format(cerebro.broker.getvalue()))
        pretty_print(format, 'Net P/L',                '${}'.format(round(pnlNetTotal,   2)) if pnlNetTotal   else NA)
        pretty_print(format, 'P/L Average per trade',  '${}'.format(round(pnlNetAverage, 2)) if pnlNetAverage else NA)
        print('\n')

    if hasattr(analyzers, 'drawdown'):
        pretty_print(format, 'Drawdown', '${}'.format(analyzers.drawdown.get_analysis()['drawdown']))
#    if hasattr(analyzers, 'sharpe'):
#        pretty_print(format, 'Sharpe Ratio:', analyzers.sharpe.get_analysis()['sharperatio'])
    if hasattr(analyzers, 'vwr'):
        pretty_print(format, 'VRW', analyzers.vwr.get_analysis()['vwr'])
    if hasattr(analyzers, 'sqn'):
        pretty_print(format, 'SQN', analyzers.sqn.get_analysis()['sqn'])
    print('\n')

    print('Transactions')
    format = "  {:<24} {:<24} {:<16} {:<8} {:<8} {:<16}"
    pretty_print(format, 'Date', 'Amount', 'Price', 'SID', 'Symbol', 'Value')
    for key, value in analyzers.txn.get_analysis().items():
        pretty_print(format, key.strftime("%Y/%m/%d %H:%M:%S"), value[0][0], value[0][1], value[0][2], value[0][3], value[0][4])



def parse_args(pargs=None):

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Sample for Tharp example with MACD')

    # group1 = parser.add_mutually_exclusive_group(required=True)
    # group1.add_argument('--data', required=False, default=None,
    #                     help='Specific data to be read in')

    # group1.add_argument('--dataset', required=False, action='store',
    #                     default=None, choices=DATASETS.keys(),
    #                     help='Choose one of the predefined data sets')

    parser.add_argument('--fromdate', required=False,
                        default='2005-01-01',
                        help='Starting date in YYYY-MM-DD format')

    parser.add_argument('--todate', required=False,
                        default=None,
                        help='Ending date in YYYY-MM-DD format')

    parser.add_argument('--cash', required=False, action='store',
                        type=float, default=50000,
                        help=('Cash to start with'))

    parser.add_argument('--cashalloc', required=False, action='store',
                        type=float, default=0.20,
                        help=('Perc (abs) of cash to allocate for ops'))

    parser.add_argument('--commperc', required=False, action='store',
                        type=float, default=0.0033,
                        help=('Perc (abs) commision in each operation. '
                              '0.001 -> 0.1%%, 0.01 -> 1%%'))

    parser.add_argument('--macd1', required=False, action='store',
                        type=int, default=12,
                        help=('MACD Period 1 value'))

    parser.add_argument('--macd2', required=False, action='store',
                        type=int, default=26,
                        help=('MACD Period 2 value'))

    parser.add_argument('--macdsig', required=False, action='store',
                        type=int, default=9,
                        help=('MACD Signal Period value'))

    parser.add_argument('--atrperiod', required=False, action='store',
                        type=int, default=14,
                        help=('ATR Period To Consider'))

    parser.add_argument('--atrdist', required=False, action='store',
                        type=float, default=3.0,
                        help=('ATR Factor for stop price calculation'))

    parser.add_argument('--smaperiod', required=False, action='store',
                        type=int, default=30,
                        help=('Period for the moving average'))

    parser.add_argument('--dirperiod', required=False, action='store',
                        type=int, default=10,
                        help=('Period for SMA direction calculation'))

    parser.add_argument('--riskfreerate', required=False, action='store',
                        type=float, default=0.01,
                        help=('Risk free rate in Perc (abs) of the asset for '
                              'the Sharpe Ratio'))
    # Plot options
    parser.add_argument('--plot', '-p', nargs='?', required=False,
                        metavar='kwargs', const=True,
                        help=('Plot the read data applying any kwargs passed\n'
                              '\n'
                              'For example:\n'
                              '\n'
                              '  --plot style="candle" (to plot candles)\n'))

    if pargs is not None:
        return parser.parse_args(pargs)

    return parser.parse_args()


def run_strategy(args=None):
    args = parse_args(args)

    cerebro = bt.Cerebro()

    # cerebro.broker.set_cash(args.cash)

    # Set the commission
    # cerebro.broker.setcommission(commission=0.0)
    # comminfo = bt.commissions.CommInfo_Stocks_Perc(commission=args.commperc, percabs=True)
    # cerebro.broker.addcommissioninfo(comminfo)

    """ dkwargs = dict()
    if args.fromdate is not None:
        fromdate = datetime.datetime.strptime(args.fromdate, '%Y-%m-%d')
        dkwargs['fromdate'] = fromdate

    if args.todate is not None:
        todate = datetime.datetime.strptime(args.todate, '%Y-%m-%d')
        dkwargs['todate'] = todate

    # if dataset is None, args.data has been  
    dataname = DATASETS.get(args.dataset, args.data)
    data0 = bt.feeds.YahooFinanceCSVData(dataname=dataname, **dkwargs)
    """

    # Add the strategy
    #cerebro.addstrategy(TestStrategy)
    #cerebro.addstrategy(strategy=SmaCross)
    #cerebro.addstrategy(MyCustomStrategy_1)
    #cerebro.addstrategy(STRATEGY_NAME)    ## this is not working, below is, i suppose it needs a class name
    #cerebro.addstrategy(strategy=SamStrategy_MainTemplate)
    #cerebro.addstrategy(strategy=MACDStrategyTest2)
    # cerebro.addstrategy(OthersStrategy_01,
    #                     macd1=args.macd1, macd2=args.macd2, macdsig=args.macdsig,
    #                     atrperiod=args.atrperiod, atrdist=args.atrdist,
    #                     smaperiod=args.smaperiod, dirperiod=args.dirperiod)
    #cerebro.addstrategy(strategy=sam_st.SamStrategy_DMICrossover)
    cerebro.addstrategy(strategy=sam_st.SamStrategy_3in1_v1)

    # Add a FixedSize sizer according to the stake
    #cerebro.addsizer(bt.sizers.FixedSize, stake=1)      # no of shares bot/sold = 1
    cerebro.addsizer(bt.sizers.PercentSizer, percents=95)
    #cerebro.addsizer(FixedPerc, perc=args.cashalloc)

    # Add the analyzers we are interested in
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='ta')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe', riskfreerate=0.0, annualize=True, timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(bt.analyzers.VWR, _name='vwr')
    cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')
    cerebro.addanalyzer(bt.analyzers.Transactions, _name='txn')
    #cerebro.addanalyzer(bt.analyzers.PyFolio)       # https://www.backtrader.com/docu/analyzers/pyfolio/

    """     # Add TimeReturn Analyzers for self and the benchmark data
    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='alltime_roi',
                        timeframe=bt.TimeFrame.NoTimeFrame)

    cerebro.addanalyzer(bt.analyzers.TimeReturn, data=data0, _name='benchmark',
                        timeframe=bt.TimeFrame.NoTimeFrame)

    # Add TimeReturn Analyzers fot the annuyl returns
    cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Years)
    # Add a SharpeRatio
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, timeframe=bt.TimeFrame.Years,
                        riskfreerate=args.riskfreerate)
    """


    # visualize the drawdown evol
    #cerebro.addobserver(bt.observers.DrawDown)  

    
    # Create a Data Feed using csv file and pandas
    #ohlc_df = pd.read_csv(SYMBOLFILE, index_col='Date', parse_dates=True)
    #data = bt.feeds.PandasData(dataname=ohlc_df)

    # Create a Data Feed
    # Used this particular function as it for parsing ALREADY DOWNLOADED Yahoo CSV Data Feeds
    datafeed = bt.feeds.YahooFinanceCSVData(dataname=SYMBOLFILE, fromdate=datetime.datetime(2021, 1, 1), todate=datetime.datetime(2022, 1, 31), reverse=False)
    print(datafeed.__dict__)
   

    # Add the Data Feed to Cerebro
    cerebro.adddata(datafeed)

    # Set our desired cash start
    cerebro.broker.setcash(PORTFOLIO_STARTING_AMOUNT)

   

    # Print out the starting conditions
    # TODO : needs to be in a function i think
    portfolio_starting_value = cerebro.broker.getvalue()
    print('Starting Portfolio Value: ', portfolio_starting_value)
    print('Strategy Name Used : ',STRATEGY_NAME)  # need to make it pick up dynamically 
    print('Symbol File Used : ', SYMBOLFILE)
    print('data.fromdate and data.todate needs printing ...')
    print('datafeed object type= ', type(datafeed))

    
    # Run our backtest over everything
    strategies_stats = cerebro.run()
    first_strategy_results = strategies_stats[0]
    #cerebro.run()

    # print the analyzers
    print("----- Print the first strategy results -----")
    #printTradeAnalysis_A(first_strategy_results.analyzers.ta.get_analysis())
    #printSQN_A(first_strategy_results.analyzers.sqn.get_analysis())
    printTradeAnalysis_B(cerebro, first_strategy_results.analyzers)

    # Print out the final result
    print("----- Print the final portfolio value -----")
    portfolio_final_value = cerebro.broker.getvalue()
    print('Final Portfolio Value: ${}'.format(portfolio_final_value))

    # Print out all the stats of the strategy execution
    #stats.print()
    # print(cerebro.__dict__)  # this is not it, this only shows params passed/used by the object
    # print(stats)
    # TODO: how to get all the stats of the strategy execution


    # Plot the result
    # throwing warnings error - fixed by doing this - https://community.backtrader.com/topic/981/importerror-cannot-import-name-min_per_hour-when-trying-to-plot/8
    #cerebro.plot()
    #cerebro.plot(style='candlestick', volume=False)
    cerebro.plot(style='candle')

"""     for alyzer in st0.analyzers:
        alyzer.print()

    if args.plot:
        pkwargs = dict(style='bar')
        if args.plot is not True:  # evals to True but is not True
            npkwargs = eval('dict(' + args.plot + ')')  # args were passed
            pkwargs.update(npkwargs)

        cerebro.plot(**pkwargs)
 """

if __name__ == '__main__':
    run_strategy()



