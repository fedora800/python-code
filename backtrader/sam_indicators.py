import backtrader as bt

# Create a customer indicator
class MyCustomIndicator_1(bt.Indicator):
    # below is something to do with describing the line on the indicator sub-plot ?
    lines = ('overunder',)

    def __init__(self):
        sma1 = bt.ind.SMA(period=13)
        sma2 = bt.ind.SMA(period=50)
        sma3 = bt.ind.SMA(period=200)

        #self.l.overunder = bt.Cmp(sma1, sma2) + bt.Cmp(sma2, sma3) - 1.5
        # each of these bt.Cmp will be -1 or 1.
        #self.l.overunder = bt.Cmp(sma1, sma2) + bt.Cmp(sma1, sma3)
        self.l.overunder = bt.Cmp(sma1, sma2)


