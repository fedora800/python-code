# https://www.allthesnippets.com/notes/finance/calculating_cumulative_returns_of_stocks_with_python_and_pandas.html


Calculating cumulative returns of a stock with python and pandas

    Returns definitions

        One-period return

        Multiperiod return / cumulative return

    Daily returns and cumulative returns of Apple, Microsoft and S&P 500 index

        Download the data from yahoo finance

        Quick data exploration and quality check

        Transform the data

        Compute cumulative returns from prices

        Compute cumulative returns from simple daily returns

        Visualize the returns

Scouring the Internet for a formula to compute the cumulative return of a stock lead us to something like this:

cumprod(1+Rt)−1

😀

Here are few definitions, math formulas and expansions to explain the mystery of the product operation and adding/subtracting the 1.
What Is a Return?

A return, also known as a financial return, in its simplest terms, is the money made or lost on an investment over some period of time.

A return is a percentage defined as the change of price expressed as a fraction of the initial price.

Returns exhibit more attractive statistical properties than asset prices themselves. Therefore it also makes more statistical sense to analyze return data rather than price series.
One-period return

Holding an asset from time t − 1 to t, the value of the asset changes from Pt−1
to Pt

. Assuming that no dividends paid are over the period.

Then the one-period simple return is defined as
Rt=Pt−Pt−1Pt−1(a)

The one period gross return is defined as
PtPt−1=Rt+1

It is the ratio of the new market value at the end of the holding period over the initial market value.
Multiperiod return

(also known as cumulative return)

The holding period for an investment may be more than one time unit. For any integer k>=1

, the returns for over k periods may be defined in a similar manner.

For example, the k-period simple return from time t − k to t is
Rt(k)=Pt−Pt−kPt−k(b)

and the k-period gross return is
PtPt−k=Rt(k)+1

It is easy to see that the multiperiod returns may be expressed in terms of one-period returns as follows:
PtPt−k=PtPt−1∗Pt−1Pt−2∗…∗Pt−k+1Pt−k
Rt(k)=PtPt−k−1=(Rt+1)∗(Rt−1+1)∗…∗(Rt−k+1+1)−1
Rt(k)=(Rt+1)∗(Rt−1+1)∗…∗(Rt−k+1+1)−1(c)
Daily returns and cumulative returns of Apple, Microsoft and S&P 500 index

In this section we will apply the formulas above to compute one-period (day) and multi-period returns (2015-09-21 to 2020-09-18) for Apple and Microsoft stock as well as S&P500 index, aka the market.

Import pandas and plotly libraries in the notebook

import pandas as pd
import plotly.offline as offline
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.express as px
import plotly.graph_objs as go
offline.init_notebook_mode(connected=True)
pd.set_option('display.max_rows', 10)

Download the data from yahoo finance

This data contains the opening and closing price per day, the extreme high and low price movements for each stock for each day. Additionally, we also get two extra columns: Volume and Adj Close.

Adj Close is the column that we will use to compute the cumulative return of the two stocks and the index.

# yahoo url template (5 years of daily data: 2015-09-21 to 2020-09-18)
yahoo_url = 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1=1442707200&period2=1600560000&interval=1d&events=history'
# get data for 3 tickers and concatenate together
tickers = ['AAPL', 'MSFT', '^GSPC']

df = pd.DataFrame()
for ticker in tickers:
    url = yahoo_url.format(ticker)
    df_tmp = pd.read_csv(url)
    df_tmp['Ticker'] = ticker
    df = pd.concat([df, df_tmp])
df

	Date 	Open 	High 	Low 	Close 	Adj Close 	Volume 	Ticker
0 	2015-09-21 	28.417500 	28.842501 	28.415001 	28.802500 	26.616798 	200888000 	AAPL
1 	2015-09-22 	28.344999 	28.545000 	28.129999 	28.350000 	26.198639 	201384800 	AAPL
2 	2015-09-23 	28.407499 	28.680000 	28.325001 	28.580000 	26.411180 	143026800 	AAPL
3 	2015-09-24 	28.312500 	28.875000 	28.092501 	28.750000 	26.568277 	200878000 	AAPL
4 	2015-09-25 	29.110001 	29.172501 	28.504999 	28.677500 	26.501280 	224607600 	AAPL
... 	... 	... 	... 	... 	... 	... 	... 	...
1254 	2020-09-14 	3363.560059 	3402.929932 	3363.560059 	3383.540039 	3383.540039 	3832130000 	^GSPC
1255 	2020-09-15 	3407.729980 	3419.479980 	3389.250000 	3401.199951 	3401.199951 	4051460000 	^GSPC
1256 	2020-09-16 	3411.229980 	3428.919922 	3384.449951 	3385.489990 	3385.489990 	4710030000 	^GSPC
1257 	2020-09-17 	3346.860107 	3375.169922 	3328.820068 	3357.010010 	3357.010010 	4371940000 	^GSPC
1258 	2020-09-18 	3357.379883 	3362.270020 	3292.399902 	3319.469971 	3319.469971 	7068700000 	^GSPC

3777 rows × 8 columns
Quick data exploration and quality check
Check start date, end date, length of each ticker time series grouping the data by each ticker

We can quickly find the groupby syntax for multiple aggregations in the pandas snippets collection:

https://www.allthesnippets.com/search/index.html?query=groupby%20multiple%20aggregations

df.groupby('Ticker')['Date'].agg(['min', 'max', 'count'])

	min 	max 	count
Ticker 			
AAPL 	2015-09-21 	2020-09-18 	1259
MSFT 	2015-09-21 	2020-09-18 	1259
^GSPC 	2015-09-21 	2020-09-18 	1259
Check missing data

Any pandas snippet for this?

https://www.allthesnippets.com/search/index.html?query=missing%20data

df.isnull().sum()

Date         0
Open         0
High         0
Low          0
Close        0
Adj Close    0
Volume       0
Ticker       0
dtype: int64

So far so good. We have the daily time series data of AAPL, MSFT and ^GSPS (S&P 500 index). Each time series has 1259 points and no missing data on column Adj Close that we will use to compute returns.
Transform the data for our calculations

Since we are only interested in specif columns we will keep only the ones we need and give them simpler names. It is always easier to work with lowercase column names and column names that don't contain special characters.

df = df[['Date', 'Ticker', 'Adj Close']]
# make columns names prettier
df.columns = ['date', 'ticker', 'price']
df

	date 	ticker 	price
0 	2015-09-21 	AAPL 	26.616798
1 	2015-09-22 	AAPL 	26.198639
2 	2015-09-23 	AAPL 	26.411180
3 	2015-09-24 	AAPL 	26.568277
4 	2015-09-25 	AAPL 	26.501280
... 	... 	... 	...
1254 	2020-09-14 	^GSPC 	3383.540039
1255 	2020-09-15 	^GSPC 	3401.199951
1256 	2020-09-16 	^GSPC 	3385.489990
1257 	2020-09-17 	^GSPC 	3357.010010
1258 	2020-09-18 	^GSPC 	3319.469971

3777 rows × 3 columns

We pivot the data from long format to wide, moving the ticker values as columns.

A handy snippet that remind us how to pivot rows to columns is available in the pandas snippets collection:

https://www.allthesnippets.com/search/index.html?query=pivot

df1 = df.pivot_table(index=['date'], columns='ticker', values=['price'])
# flatten columns multi-index, `date` will become the dataframe index
df1.columns = [col[1] for col in df1.columns.values]
df1

	AAPL 	MSFT 	^GSPC
date 			
2015-09-21 	26.616798 	40.086960 	1966.969971
2015-09-22 	26.198639 	39.896111 	1942.739990
2015-09-23 	26.411180 	39.868851 	1938.760010
2015-09-24 	26.568277 	39.905201 	1932.239990
2015-09-25 	26.501280 	39.932461 	1931.339966
... 	... 	... 	...
2020-09-14 	115.360001 	205.410004 	3383.540039
2020-09-15 	115.540001 	208.779999 	3401.199951
2020-09-16 	112.129997 	205.050003 	3385.489990
2020-09-17 	110.339996 	202.910004 	3357.010010
2020-09-18 	106.839996 	200.389999 	3319.469971

1259 rows × 3 columns
Compute cumulative returns from prices

Since the stock prices are available to us for the entire period we can calculate the cumulative return on the entire period 2015-09-21 to 2020-09-18 using formula (b)

cum_return = (df1.iloc[-1] - df1.iloc[0]) / df1.iloc[0]
cum_return

AAPL     3.014006
MSFT     3.998882
^GSPC    0.687606
dtype: float64

These are the rates of change for each ticker. We will multiple by 100 to get the numbers as percentage change.

cum_return * 100

AAPL     301.400634
MSFT     399.888240
^GSPC     68.760582
dtype: float64

Looks like Microsoft stock price increased almost 400% during the period while Apple stock price increased 301.4%. Not bad!

During the same period the S&P 500 market increased only by 68.7%.
Compute cumulative returns from simple daily returns

We will use formula (a) and pandas built in function pct_change to compute the simple returns for each day, each stock in our dataset.

# compute daily returns using pandas pct_change()
df_daily_returns = df1.pct_change()
# skip first row with NA 
df_daily_returns = df_daily_returns[1:]
df_daily_returns

	AAPL 	MSFT 	^GSPC
date 			
2015-09-22 	-0.015710 	-0.004761 	-0.012318
2015-09-23 	0.008113 	-0.000683 	-0.002049
2015-09-24 	0.005948 	0.000912 	-0.003363
2015-09-25 	-0.002522 	0.000683 	-0.000466
2015-09-28 	-0.019789 	-0.014793 	-0.025666
... 	... 	... 	...
2020-09-14 	0.030000 	0.006764 	0.012742
2020-09-15 	0.001560 	0.016406 	0.005219
2020-09-16 	-0.029514 	-0.017866 	-0.004619
2020-09-17 	-0.015964 	-0.010436 	-0.008412
2020-09-18 	-0.031720 	-0.012419 	-0.011183

1258 rows × 3 columns

And finally, the formula (c) on the dataframe of daily returns using pandas' cumprod function.

# Calculate the cumulative daily returns
df_cum_daily_returns = (1 + df_daily_returns).cumprod() - 1
df_cum_daily_returns = df_cum_daily_returns.reset_index()
df_cum_daily_returns

	date 	AAPL 	MSFT 	^GSPC
0 	2015-09-22 	-0.015710 	-0.004761 	-0.012318
1 	2015-09-23 	-0.007725 	-0.005441 	-0.014342
2 	2015-09-24 	-0.001823 	-0.004534 	-0.017657
3 	2015-09-25 	-0.004340 	-0.003854 	-0.018114
4 	2015-09-28 	-0.024043 	-0.018590 	-0.043315
... 	... 	... 	... 	...
1253 	2020-09-14 	3.334105 	4.124110 	0.720179
1254 	2020-09-15 	3.340868 	4.208177 	0.729157
1255 	2020-09-16 	3.212753 	4.115130 	0.721170
1256 	2020-09-17 	3.145502 	4.061746 	0.706691
1257 	2020-09-18 	3.014006 	3.998882 	0.687606

1258 rows × 4 columns

Last record of the dataframe multiplied by 100 is giving us the percentage change of the stock prices for our entire period (2015-09-22 to 2020-09-18).

Notice that we've got same results as when we applied formula (b)

cum_return_entire_period = df_cum_daily_returns.iloc[:, 1:].tail(1)
cum_return_entire_period * 100

	AAPL 	MSFT 	^GSPC
1257 	301.400634 	399.88824 	68.760582
Visualize the returns

It is always good to visualize the returns to better understand the stocks performance.

We will use the interactive library plotly.express for this exercise. This library allows us to interact with the graph: zooming in and out, adding/removing a plot line, saving as image and more.

plotly.express works with pandas dataframes in long format and we will use the function melt to transform our dataframes df_daily_returns and df_cum_daily_returns from short format (we have the tickers as columns) to long format (tickers as rows).

A quick pandas snippet for that can be found on AllTheSnippets.com website:

https://www.allthesnippets.com/search/index.html?query=melt

# reset the index, moving `date` as column
df_daily_returns = df_daily_returns.reset_index()
# use `melt`
df1 = df_daily_returns.melt(id_vars=['date'], var_name='ticker', value_name='daily_return')
# add one more column, showing the daily_return as percent
df1['daily_return_pct'] = df1['daily_return'] * 100
df1

	date 	ticker 	daily_return 	daily_return_pct
0 	2015-09-22 	AAPL 	-0.015710 	-1.571034
1 	2015-09-23 	AAPL 	0.008113 	0.811267
2 	2015-09-24 	AAPL 	0.005948 	0.594812
3 	2015-09-25 	AAPL 	-0.002522 	-0.252169
4 	2015-09-28 	AAPL 	-0.019789 	-1.978889
... 	... 	... 	... 	...
3769 	2020-09-14 	^GSPC 	0.012742 	1.274183
3770 	2020-09-15 	^GSPC 	0.005219 	0.521936
3771 	2020-09-16 	^GSPC 	-0.004619 	-0.461895
3772 	2020-09-17 	^GSPC 	-0.008412 	-0.841237
3773 	2020-09-18 	^GSPC 	-0.011183 	-1.118258

3774 rows × 4 columns

fig = px.line(df1, x='date',
              y='daily_return_pct', color='ticker',
              title='Performance - Daily Simple Returns',
              labels={'daily_return_pct':'daily returns (%)'})
fig.show()

Transforming the cumulative returns data for plotting.

df2 = df_cum_daily_returns.melt(id_vars=['date'], var_name='ticker', value_name='cum_return')
df2['cum_return_pct'] = df2['cum_return'] * 100
df2

	date 	ticker 	cum_return 	cum_return_pct
0 	2015-09-22 	AAPL 	-0.015710 	-1.571034
1 	2015-09-23 	AAPL 	-0.007725 	-0.772512
2 	2015-09-24 	AAPL 	-0.001823 	-0.182295
3 	2015-09-25 	AAPL 	-0.004340 	-0.434004
4 	2015-09-28 	AAPL 	-0.024043 	-2.404305
... 	... 	... 	... 	...
3769 	2020-09-14 	^GSPC 	0.720179 	72.017880
3770 	2020-09-15 	^GSPC 	0.729157 	72.915703
3771 	2020-09-16 	^GSPC 	0.721170 	72.117014
3772 	2020-09-17 	^GSPC 	0.706691 	70.669103
3773 	2020-09-18 	^GSPC 	0.687606 	68.760582

3774 rows × 4 columns

fig = px.line(df2, x='date',
              y='cum_return_pct', color='ticker',
              title='Performance - Daily Cumulative Returns',
              labels={'cum_return_pct':'daily cumulative returns (%)', })
fig.show()

Navigation


