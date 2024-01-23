# https://medium.com/@tsubedy/ev-stock-daily-cumulative-returns-using-python-pandas-e918362ebadc


I was interested to perform an analysis of performances of the top 10 EVs makers by market cap during the past 12 months using Python Pandas. I have used Plotly express as a visualization tool to show the performances of the daily cumulative returns and their percentages.

A return in financial is defined as the money made or lost on an investment over the range of time period. It is calculated in terms of percentage that is defined as change of price expressed as a fraction of the initial price.

Holding an asset from time t−1 to t, the value of the asset changes from Pt−1 to Pt assuming no dividends are paid over the time period.

Then the one-period simple return is defined as

Rt = (Pt − Pt−1) / Pt−1

The one period gross return is defined as

Pt / Pt−1 = 1 + Rt

It is the ratio of the new market value at the end of the holding period over the initial market value.

Similarly,

for k period gross return is given by Pt / Pt-k = 1 + Rt(k)
Getting live data from Yahoo Finance

Using Pandas Data Reader, we will be getting the live data from yahoo finance by specifying time period with datetime module.

The time period I have chosen for this analysis is from 2021–2–11 to 2022–2–11 (last twelve months).

The tickers for each EV makers from stock market are chosen on the basis of their market cap (top 10) as of 2022–2–11.
Data exploration and Processing

The dataset is obtained with stock prices as high, low, open, close, adjusted close and volume for each ticker. The following code snippet is used to check the starting and ending dates and number of records.

Any null values in the dataset is then checked as following codes. There are no NULL values in the dataset.
Data Transformation and Calculations

For the purpose of this analysis I have chosen only three variables including Date, Ticker, and Adjusted Closed Price.

Dataset is converted into a Pivot table format where each tickers will be used as individual variables and the prices are considered as values to make the analysis more meaningful.
Computing Cumulative Returns

Cumulative return for the entire period of past 12 months

While looking at the results, it can be seen that only TESLA has positive returns of about 6% in the last 12 months. All other EV makers have shown negative returns ranging from -12% up to -87%.
Daily Return Percentages

Using Pandas built in function pct_change(), the return for each days is calculated as in the following table.

Pandas cumprod() function is used to calculate cumulative daily returns.

The last row of the above dataset shows the fractions of the change in price for the entire period. In order to obtain the percentage of change in the price for the entire period, it is then multiplied by 100.
Visualizing the returns

Visualization gives a better understanding of the performances. For the visualization I have used Plotly express library which allows us to interact with the graph such as zooming in and zooming out, adding/removing a categories, saving the graph as image, scaling, reseting axes.

Since Plotly.express works with pandas data frames in non-pivot format and will be using a function ‘melt()’ to transform the data frames ‘daily_returns’ and ‘cum_daily_returns’ from pivot format (tickers as columns) to non-pivot format (tickers as rows).

From this analysis of top 10 market cap EV stock returns, it can be seen that there were fluctuations in the beginning and and the end of the year 2021 with the EV makers including TESLA, LUCID, FISKER, XPEV and LI Auto. All other EV makers seems to be following a downward trend for the whole year.

