from loguru import logger
import pandas as pd

def fn_01_relative_strength_indicator(xxx):

  '''
  # Create RSI
  rsi = RSI(data.close, timeperiod=14)

  # Create MACD
  macd, macdsignal, macdhist = MACD(
      data.close, 
      fastperiod=12, 
      slowperiod=26, 
      signalperiod=9
  )

  macd = pd.DataFrame(
      {
          "MACD": macd,
          "MACD Signal": macdsignal,
          "MACD History": macdhist,
      }
  )
  https://pyquantnews.com/technical-df_macd-python-3-indicators/
  https://tradewithpython.com/generating-buy-sell-signals-using-python
  https://www.exfinsis.com/tutorials/python-programming-language/macd-stock-technical-indicator-with-python/


  # Plotting MACD
  plt.subplot(2, 1, 2)
  plt.plot(data['MACD'], label='MACD Line', color='blue')
  plt.plot(data['MACD_Signal'], label='Signal Line', color='red')
  plt.bar(data.index, data['MACD_Diff'], label='Histogram', color='grey', alpha=0.5)
  plt.legend()
  '''
  logger.debug("Received arguments : dbconn={} symbol={} df={} tbl_name={}", xxx, xxx)


def fn_02_comparative_relative_strength_CRS_indicator(benchmark_symbol: str, df_benchmark_symbol: pd.DataFrame, symbol: str, df_symbol: pd.DataFrame) -> pd.DataFrame:
  """
  Computes the Comparative Relative Strength (CRS) using the data provided in the arguments
  NOTE: This will change the symbol original df by appending an extra column to the df for the CRS
  NOTE: The number of records/amount of data in df should be same (same start and end dates) for both the benchmark and the symbol

  Args:
      benchmark_symbol (str): benchmark symbol ticker
      df_benchmark_symbol (pd.DataFrame): df containing prices for the benchmark symbol
      symbol (str): symbol ticker for whom we need to compute the CRS
      df_benchmark_symbol (pd.DataFrame): df containing prices for the required symbol

  Returns:
      pd.DataFrame: df of the symbol with an extra column containing CRS values

  Example:
  >> fn_02_comparative_relative_strength_CRS_indicator("SPY", df_SPY, "AAPL", df_AAPL)
  """  

  # set the lookback calculation period 
  LENGTH = 50
  
  logger.debug("Received arguments : benchmark_symbol={} symbol={}", benchmark_symbol, symbol)
  logger.debug("Received arguments : df_benchmark_symbol={}", df_benchmark_symbol)
  logger.debug("Received arguments : df_symbol={}", df_symbol)


  print('Computing daily percentage change on both Symbol and Benchmark ...')
  df_benchmark_symbol['dly_pct_change'] = df_benchmark_symbol['close'].pct_change()
  df_benchmark_symbol = df_benchmark_symbol[['pd_time','close','dly_pct_change']]      # remove all unnecessary columns
  print(df_benchmark_symbol.tail(3))
  df_symbol['dly_pct_change'] = df_symbol['close'].pct_change()
  df_symbol = df_symbol[['pd_time','close','dly_pct_change']]
  print(df_symbol.tail(3))

  print("--- MERGED DFs ---")
  # uses pandas merge function to merge these two DataFrames on the common column 'pd_time'.
  # In the merged DataFrame, df_symbol columns will have suffix '_SYMB' df_benchmark_symbol columns will have suffix '_ETF'.
  df_merged = pd.merge(df_symbol[['pd_time', 'close', 'dly_pct_change']], 
                       df_benchmark_symbol[['pd_time', 'close', 'dly_pct_change']], 
                       on='pd_time', suffixes=('_SYMB', '_ETF'))
  print(df_merged.tail(3))

  # Calculate Comparative Relative Strength (CRS)
  # used my Trading Reference gdoc and TradingView RS pinecode from someone and ultimately ChatGPT for getting this right
  logger.debug("Calculating the Comparative Relative Strength (CRS) on {} against {}", symbol, benchmark_symbol)
  df_merged['CRS'] = (df_merged['close_SYMB'] / df_merged['close_SYMB'].shift(LENGTH) /
                                    (df_merged['close_ETF'] / df_merged['close_ETF'].shift(LENGTH)) - 1)
  print("--- UPDATED MERGED DFs ---")
  print(df_merged.tail(3))

  '''
  # Plot - Comparative Relative Strength (CRS) Indicator
  axs[2].plot(df_merged['pd_time'], df_merged['Relative_Strength'], label='Comparative Relative Strength (CRS)', color='purple')
  axs[2].axhline(0, color='black', linestyle='dotted')       # draw a horizontal line
  # Calculate and plot Moving Average if show_MA is True
  # if show_MA:
  #     df_merged['MA'] = df_merged['Relative_Strength'].rolling(window=length_MA).mean()
  #     plt.plot(df_merged['MA'], label=f'MA ({length_MA})', color='gray')
  '''
  
  return(df_merged)


# --------------------------------------------------------------------------------
def main():

  benchmark_symbol_file = "SPY.csv"
  benchmark_symbol = "SPY"
  symbol_file = "MSFT.csv"
  symbol="MSFT"
  
  df_benchmark_symbol = pd.read_csv(benchmark_symbol_file)
  df_benchmark_symbol['Date'] = pd.to_datetime(df_benchmark_symbol['Date'])     # convert Date to a datetime object
  print(f"BENCHMARK = {benchmark_symbol} and df = {df_benchmark_symbol.tail(3)}")
  
  df_symbol = pd.read_csv(symbol_file)
  df_symbol['Date'] = pd.to_datetime(df_symbol['Date'])     # convert Date to a datetime object
  print(f"SYMBOL = {symbol} and df = {df_symbol.tail(3)}")

  fn_03_relative_strength_chart(benchmark_symbol, df_benchmark_symbol, symbol, df_symbol)
  #fn_02_comparative_relative_strength_CRS_indicator(benchmark_symbol: str, df_benchmark_symbol: pd.DataFrame, symbol: str, df_symbol: pd.DataFrame) -> pd.DataFrame:
