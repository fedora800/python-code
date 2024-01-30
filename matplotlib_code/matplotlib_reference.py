import matplotlib.pyplot as plt
import pandas as pd


# --------------------------------------------------------------------------------
def fn_01_simple_chart(symbol, df):


  # Set the size pf chart
  #plt.figure(figsize=(12, 6))

  # Define the title name of the figure
  plt.title(f"{symbol} Price Chart", fontsize=16)


  # Define the labels for x-axis and y-axis
  plt.xlabel('Date', fontsize=14)
  plt.ylabel('Closing Price', fontsize=14)

  # Plot the grid lines
  plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)

  # Line plot of closing prices
  plt.plot(df['Close'], label=f'{symbol} Closing Price', linewidth=2)
  #plt.plot(df['Close'])

  # Show the legend
  #A legend is an area describing the elements of the graph. In the Matplotlib library, there’s a function called legend() which is used to place a legend on the axes
  # ie INSIDE the chart image
  # if the plt.plot(..., label="my-label-1") is defined, then the legend will show this label name
  # Function add a legend
  #plt.legend(["symbol_price", "test_legend"], loc="lower right")
  plt.legend()

  plt.show()
  # note - the x axis dates will not show correctly, it will show datapoints like 200, 400, 600 etc



# --------------------------------------------------------------------------------

def fn_02_subplots_with_pandas(df, sym):

  NUM_SUBPLOTS=2
  NUM_COLUMNS=1

  '''
  matplotlib.pyplot.subplots(nrows=1, ncols=1, *, sharex=False, sharey=False, squeeze=True, width_ratios=None,
          height_ratios=None, subplot_kw=None, gridspec_kw=None, **fig_kw)
  subplots() without arguments returns a Figure and a single Axes.
  '''

  '''
  A figure with just one subplot
  fig, ax = plt.subplots()
  ax.plot(x, y)
  ax.set_title('A single plot')
  '''


  fig, axs = plt.subplots(nrows=NUM_SUBPLOTS, ncols=NUM_COLUMNS)
  # fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(6, 6), layout='constrained')

  '''
  ax1.legend(handles=[ml.Line2D([], [], ls='--', label='Gaps in daily data')])
  ax1.xaxis.set_major_locator(DayLocator())
  ax1.xaxis.set_major_formatter(DateFormatter('%a'))
  '''


  # plot 1
  axs[0].set_xlabel('Date', fontsize=12)
  axs[0].set_ylabel('Close Price', fontsize=12)
  axs[0].grid(which="major", color='k', linestyle='-.', linewidth=0.5)
  axs[0].plot(df['Date'], df['Close'], label=f'{sym} Closing Price', linewidth=2)  # by default 1st is x axis, 2nd is y axis
  axs[0].legend(["symbol_price"], loc="lower right")
  axs[0].set_title("--Closing Prices--")


  # Set the size pf chart
  #plt.figure(figsize=(12, 6))

  # Define the title name of the figure
  #plt.title(f"{sym} Price Chart", fontsize=16)


  # plot 2
  axs[1].set_title("--Volume--")
  axs[1].bar(df['Date'], df['Volume'], color='red', label=f'{sym} lbl_Volume', linewidth=2)
  axs[1].tick_params('y', colors='purple')
  axs[1].axhline(100000, color='black', linestyle='dotted')       # draw a horizontal line



  fig.suptitle('Vertically stacked subplots')
  plt.show()


# --------------------------------------------------------------------------------
def fn_03_relative_strength_chart(df_bch, bch_sym, df_sym, sym):

  NUM_SUBPLOTS=5
  NUM_COLUMNS=1

  # IMPORTANT - both dataframes should have data from same start and end dates

  print('Computing daily percentage change on both Symbol and Benchmark ...')
  df_bch['Dly_Pct_Change'] = df_bch['Close'].pct_change()
  # below change seems to mess up the Relative_Performance_* column computation in the relative performance section
  #df_bch['Dly_Pct_Change'] = (df_bch['Dly_Pct_Change'] * 100).round(3)   # Multiply by 100 and reduce the decimal precision so it's human readable
  df_bch = df_bch[['Date','Close','Dly_Pct_Change']]
  print(f"--- {bch_sym} ---")
  print(df_bch.tail(3))

  df_sym['Dly_Pct_Change'] = df_sym['Close'].pct_change()
  #df_sym['Dly_Pct_Change'] = (df_sym['Dly_Pct_Change'] * 100).round(3)
  df_sym = df_sym[['Date','Close','Dly_Pct_Change']]
  print(f"--- {sym} ---")
  print(df_sym.tail(3))

  print("--- MERGED DFs ---")
  df_merged = pd.merge(df_sym[['Date', 'Close', 'Dly_Pct_Change']], df_bch[['Date', 'Close', 'Dly_Pct_Change']], on='Date', suffixes=('_SYMB', '_ETF'))
  print(df_merged.tail(3))

  # Parameters
  length = 50
  
  # Calculate Relative Strength
  # used my Trading Reference gdoc and TradingView RS pinecode from someone and ultimately ChatGPT for getting this right
  df_merged['Relative_Strength'] = (df_merged['Close_SYMB'] / df_merged['Close_SYMB'].shift(length) /
                                    (df_merged['Close_ETF'] / df_merged['Close_ETF'].shift(length)) - 1)

  # Prepare the fig and axs plot objects with subplot information
  #fig, axs = plt.subplots(NUM_SUBPLOTS, NUM_COLUMNS, figsize=(10, 8), sharex=True)
  fig, axs = plt.subplots(NUM_SUBPLOTS, NUM_COLUMNS, figsize=(10, 8))

  # Plot 1 - Symbol Prices
  axs[0].plot(df_merged['Date'], df_merged['Close_SYMB'], label=sym + ' Prices', color='blue')
  axs[0].set_ylabel('1-Symbol Prices', color='blue')
  axs[0].tick_params('y', colors='blue')
  axs[0].legend(loc='upper left')

  # Plot 2 - Benchmark Prices
  axs[1].plot(df_merged['Date'], df_merged['Close_ETF'], label=bch_sym + ' Prices (Benchmark)', color='orange')
  axs[1].set_ylabel('2-Benchmark Prices', color='orange')
  axs[1].tick_params('y', colors='orange')
  axs[1].legend(loc='upper left')


  '''
  # Plot Relative Strength
  ax2.plot(df_merged['Relative_Strength'], label='Relative Strength', color='#1155CC')
  ax2.set_xlabel('Date')
  ax2.set_ylabel('Relative Strength', color='red')
  ax2.tick_params('y', colors='red')
  ax2.set_title('xxxxxxxx Relative Strength')
  ax2.axhline(0, color='black', linestyle='dotted')       # draw a horizontal line
  '''

  # Plot 3 - Relative Strength Indicator
  axs[2].plot(df_merged['Date'], df_merged['Relative_Strength'], label='Relative Strength', color='purple')
  axs[2].set_ylabel('3-Relative Strength (RS)', color='purple')
  axs[2].tick_params('y', colors='purple') 
  axs[2].axhline(0, color='black', linestyle='dotted')       # draw a horizontal line
  # Calculate and plot Moving Average if show_MA is True
  # if show_MA:
  #     df_merged['MA'] = df_merged['Relative_Strength'].rolling(window=length_MA).mean()
  #     plt.plot(df_merged['MA'], label=f'MA ({length_MA})', color='gray')

  # Plot 4 - Show the Symbol and Benchmark prices together on 1 plot
  #df_merged.set_index('Date', inplace=True)    # this will show the dates at the bottom properly, else just numbers
  axs[3].plot(df_merged['Date'], df_merged['Close_SYMB'], label='Close_SYMB', color='green')
  axs[3].plot(df_merged['Date'], df_merged['Close_ETF'], label='Close_ETF', color='orange')
  axs[3].set_ylabel('4-Prices on Same Plot', color='black')
  # plt.title('Performance Comparison: Close_SYMB vs Close_ETF')

  # Plot 5A - Plot the relative performance of symbol and benchmark in % terms starting from 0 at start
  # Calculate relative performance starting from 0
  df_merged['Relative_Performance_SYMB'] = (1 + df_merged['Dly_Pct_Change_SYMB']).cumprod() - 1
  df_merged['Relative_Performance_ETF'] = (1 + df_merged['Dly_Pct_Change_ETF']).cumprod() - 1
  
  # Multiply by 100 and reduce the decimal precision so it's human readable
  df_merged['Relative_Performance_SYMB']  = (df_merged['Relative_Performance_SYMB'] * 100).round(3)
  df_merged['Relative_Performance_ETF']  = (df_merged['Relative_Performance_ETF'] * 100).round(3) 

  print("--- merged dataframe data before plotting ---")
  print(df_merged)
  # Plot relative performance
  axs[4].plot(df_merged['Date'], df_merged['Relative_Performance_SYMB'], label='Relative Performance SYMB', marker='+', color='blue')
  axs[4].plot(df_merged['Date'], df_merged['Relative_Performance_ETF'], label='Relative Performance ETF', marker='+', color='orange')
  axs[4].set_ylabel('5-Performance Plot', color='black')

  # Plot 5B - Plot the same relative performance chart on a new plot
  # NEW SEPERATE CHART
  plt.figure(figsize=(10, 6))
  plt.plot(df_merged['Date'], df_merged['Relative_Performance_SYMB'], label='Relative Performance ' + sym, marker='+', color='blue')
  plt.plot(df_merged['Date'], df_merged['Relative_Performance_ETF'], label='Relative Performance (benchmark) ' + bch_sym, marker='+', color='orange')

  # Display the plot
  plt.legend()
  plt.show()


# --------------------------------------------------------------------------------
def main():

  benchmark_symbol_file = "SPY.csv"
  benchmark_symbol = "SPY"
  symbol_file = "MSFT.csv"
  symbol="MSFT"
  
  df_benchmark_symbol = pd.read_csv(benchmark_symbol_file)
  df_benchmark_symbol['Date'] = pd.to_datetime(df_benchmark_symbol['Date'])     # convert Date to a datetime object
  print(df_benchmark_symbol.tail(3))
  
  df_symbol = pd.read_csv(symbol_file)
  df_symbol['Date'] = pd.to_datetime(df_symbol['Date'])     # convert Date to a datetime object
  print(df_symbol.tail(3))

  #fn_01_simple_chart(df_symbol)
  #fn_02_subplots_with_pandas(df_symbol, symbol)
  fn_03_relative_strength_chart(benchmark_symbol, df_benchmark_symbol, symbol, df_symbol)


# --------------------------------------------------------------------------------
if __name__ == '__main__':
  main()


# https://realpython.com/python-matplotlib-guide/       useful archetecture and objects info
# https://www.influxdata.com/blog/matplotlib-tutorial-visualize-time-series-data-matplotlib-influxdb/



