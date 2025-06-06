import sys
import platform

from loguru import logger
import numpy as np
import pandas as pd
import talib as ta

if platform.system() == "Windows":
  #logger.debug("mod_technical_indicators.py - Running on Windows")
  sys.path.append("H:\\git-projects\\python-code")
  sys.path.append("H:\\git-projects\\python-code\\streamlit_code")
elif platform.system() == "Linux":
  #logger.debug("mod_technical_indicators.py - Running on Linux")
  sys.path.append("/home/cloud_user/git-projects/python-code")
else:
  print("Operating system not recognized")

from pkg_common import mod_others as m_oth

def fn_check_data(df: pd.DataFrame):
  """_summary_

  Args:
      df (pd.DataFrame): contains the data_

  Returns:
      int: number of records in the dataframe
  """

  # logger.debug("Received arguments : df={} and exp_recs={}", df, exp_recs)
  num_records = df.shape[0]
  num_columns = df.shape[1]
  logger.debug("Received arguments : num_records={} and num_columns={}", num_records, num_columns)
  #logger.trace("df info={}", df.info())
  return num_records


def fn_adx_indicator(df: pd.DataFrame, column_name: str):
    """
    Computes the ADX indicator using the data provided in the arguments
    NOTE: This will change the symbol original df by appending an extra column to the df for the ADX values
    Args:
      df (pd.DataFrame): df containing prices for the required symbol
      column_name (str) : name of the new column that will be appended to the df with ADX values
    Returns:
        pd.DataFrame: df of the symbol with an extra column containing ADX values
    Example:
    >> fn_adx_indicator(df, "dm_dp_adx")

    """

    TIME_PERIOD = 14
    IF_DELIMITER = ";"  # intra-field delimeter for the macd column

    logger.debug("Received arguments : df={}", df)
    fn_check_data(df, 300)

    # create a temporary df with same index as the df passed, so that we can later merge/update df with values matching the same index of df_tmp
    df_tmp = pd.DataFrame(index=df.index)

    na_ADX = ta.ADX(df["high"], df["low"], df["close"], TIME_PERIOD)
    na_DMI_MINUS = ta.MINUS_DI(df["high"], df["low"], df["close"], TIME_PERIOD)
    na_DMI_PLUS = ta.PLUS_DI(df["high"], df["low"], df["close"], TIME_PERIOD)

    # store the computed ADX values into individual columns of the temporary df
    df_tmp["dmi_minus"] = na_DMI_MINUS
    df_tmp["dmi_plus"] = na_DMI_PLUS
    df_tmp["adx"] = na_ADX

    # round the values to 2 decimal places of only specific columns
    columns_to_round = ["dmi_minus", "dmi_plus", "adx"]
    df_tmp[columns_to_round] = df_tmp[columns_to_round].round(2)

    df[column_name] = (
        df_tmp["dmi_minus"].astype(str)
        + IF_DELIMITER
        + df_tmp["dmi_plus"].astype(str)
        + IF_DELIMITER
        + df_tmp["adx"].astype(str)
    )
    logger.trace("-------df.info={}---df={}---", df.info(), df)
    logger.debug("--dfhead=\n{}----dftail=\n{}----", df.head(1), df.tail(1))

    return df


def fn_macd_indicator_last_row_only(df: pd.DataFrame, column_name: str):        # might have to remove later ?
    """
    Computes the MACD indicator using the data provided in the arguments
    NOTE: This will change the symbol original df by appending an extra column to the df for the MACD values
    NOTE: All 3 values (macd,signal,histogram) will be delimited and put together into this 1 column
    Args:
      df (pd.DataFrame): df containing prices for the required symbol
      column_name (str) : name of the new column that will be appended to the df with MACD values
    Returns:
        pd.DataFrame: df of the symbol with an extra column containing MACD values

    Example:
    >> fn_macd_indicator(df, "macd-sig-hist")
    """
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    IF_DELIMITER = ";"  # intra-field delimeter for the macd column
    df_tmp = pd.DataFrame()

    logger.debug("Received arguments : df={}", df)
    num_recs = fn_check_data(df, 300)

    if num_recs < 200:
        logger.error("num_records={} less than expected records={}", num_recs, 200)
        # TODO: exit maybe ?

    na_macd, na_macd_signal, na_macd_hist = ta.MACD(
        df["close"].to_numpy(),
        fastperiod=MACD_FAST,
        slowperiod=MACD_SLOW,
        signalperiod=MACD_SIGNAL,
    )

    # store in a temporary df
    df_tmp["macd"] = na_macd
    df_tmp["signal"] = na_macd_signal
    df_tmp["histogram"] = na_macd_hist

    # round the values to 2 decimal places in the last row only due to starting rows having null values
    df_tmp.iloc[-1, df_tmp.columns.get_loc("macd")] = df_tmp.iloc[-1]["macd"].round(2)
    df_tmp.iloc[-1, df_tmp.columns.get_loc("signal")] = df_tmp.iloc[-1]["signal"].round(2)
    df_tmp.iloc[-1, df_tmp.columns.get_loc("histogram")] = df_tmp.iloc[-1]["histogram"].round(2)

    df[column_name] = (
        df_tmp["macd"].astype(str)
        + IF_DELIMITER
        + df_tmp["signal"].astype(str)
        + IF_DELIMITER
        + df_tmp["histogram"].astype(str)
    )

    logger.trace("-------df.info={}------", df.info())
    m_oth.fn_df_print_first_last_rows(df, 3, 'ALL_COLS')
    return df

    # '''
    # # Create RSI
    # rsi = RSI(data.close, timeperiod=14)

    # # Create MACD
    # macd, macdsignal, macdhist = MACD(
    #     data.close,
    #     fastperiod=12,
    #     slowperiod=26,
    #     signalperiod=9
    # )

    # macd = pd.DataFrame(
    #     {
    #         "MACD": macd,
    #         "MACD Signal": macdsignal,
    #         "MACD History": macdhist,
    #     }
    # )
    # https://pyquantnews.com/technical-df_macd-python-3-indicators/
    # https://tradewithpython.com/generating-buy-sell-signals-using-python
    # https://www.exfinsis.com/tutorials/python-programming-language/macd-stock-technical-indicator-with-python/

    # # Plotting MACD
    # plt.subplot(2, 1, 2)
    # plt.plot(data['MACD'], label='MACD Line', color='blue')
    # plt.plot(data['MACD_Signal'], label='Signal Line', color='red')
    # plt.bar(data.index, data['MACD_Diff'], label='Histogram', color='grey', alpha=0.5)
    # plt.legend()
    # '''
    # logger.debug("Received arguments : df={}", df)



def fn_macd_indicator(df: pd.DataFrame, column_name: str):
  """
  Computes the MACD indicator using the data provided in the arguments
  NOTE: This will change the symbol original df by appending an extra column to the df for the MACD values
  NOTE: All 3 values (macd,signal,histogram) will be delimited and put together into this 1 column
  Args:
    df (pd.DataFrame): df containing prices for the required symbol
    column_name (str) : name of the new column that will be appended to the df with MACD values
  Returns:
      pd.DataFrame: df of the symbol with an extra column containing MACD values

  Example:
  >> fn_macd_indicator(df, "macd-sig-hist")
  """

  # NOTE: i think i should be using pandas-ta, very simple - https://www.alpharithms.com/calculate-macd-python-272222/


  MACD_FAST = 12
  MACD_SLOW = 26
  MACD_SIGNAL = 9
  IF_DELIMITER = ";"  # intra-field delimeter for the macd column
  
  logger.debug("Received arguments : df={}", df)
  num_recs = fn_check_data(df, 300)

  if num_recs < 200:
      logger.error("num_records={} less than expected records={}", num_recs, 200)
      # TODO: exit maybe ?

  # create a temporary df with same index as the df passed, so that we can later merge/update df with values matching the same index of df_tmp
  df_tmp = pd.DataFrame(index=df.index)

  na_macd, na_macd_signal, na_macd_hist = ta.MACD(df["close"].to_numpy(), fastperiod=MACD_FAST, slowperiod=MACD_SLOW, signalperiod=MACD_SIGNAL)

  # store the computed macd values into individual columns of the temporary df
  df_tmp["macd"] = na_macd
  df_tmp["signal"] = na_macd_signal
  df_tmp["histogram"] = na_macd_hist

  # round the values to 2 decimal places of only specific columns
  columns_to_round = ["macd", "signal", "histogram"]
  df_tmp[columns_to_round] = df_tmp[columns_to_round].round(2)
  # df_tmp["macd"] = df_tmp["macd"].round(2)
  # df_tmp["signal"] = df_tmp["signal"].round(2)
  # df_tmp["histogram"] = df_tmp["histogram"].round(2)

  logger.debug("---- Debugging Information ----")
  logger.debug("df_tmp shape: {}", df_tmp.shape)
  logger.debug("df_tmp data types: \n{}", df_tmp.dtypes)
  logger.debug("df_tmp head: \n{}", df_tmp.head())

  logger.debug("df shape: {}", df.shape)
  logger.debug("df data types: \n{}", df.dtypes)
  logger.debug("df head: \n{}", df.head())
  logger.debug("---- End of Debugging Information ----")


  df[column_name] = (
      df_tmp["macd"].astype(str)
      + IF_DELIMITER
      + df_tmp["signal"].astype(str)
      + IF_DELIMITER
      + df_tmp["histogram"].astype(str)
  )

  logger.trace("-------df.info={}------", df.info())
  m_oth.fn_df_print_first_last_rows(df, 3, 'ALL_COLS')
  return df



def fn_relative_strength_indicator(df: pd.DataFrame):
  PERIOD = 14

  logger.debug("Received arguments : df={}", df)
  num_recs = fn_check_data(df, 300)

  if num_recs < 200:
      logger.error("num_records={} less than expected records={}", num_recs, 200)
      # TODO: exit maybe ?

  df["rsi_14"] = ta.RSI(df["close"], timeperiod=PERIOD)
  df["rsi_14"] = df["rsi_14"].round(3)
  m_oth.fn_df_print_first_last_rows(df, 3, 'ALL_COLS')

  return df

    # '''
    # # Create RSI
    # rsi = RSI(data.close, timeperiod=14)

    # # Create MACD
    # macd, macdsignal, macdhist = MACD(
    #     data.close,
    #     fastperiod=12,
    #     slowperiod=26,
    #     signalperiod=9
    # )

    # macd = pd.DataFrame(
    #     {
    #         "MACD": macd,
    #         "MACD Signal": macdsignal,
    #         "MACD History": macdhist,
    #     }
    # )
    # https://pyquantnews.com/technical-df_macd-python-3-indicators/
    # https://tradewithpython.com/generating-buy-sell-signals-using-python
    # https://www.exfinsis.com/tutorials/python-programming-language/macd-stock-technical-indicator-with-python/

    # # Plotting MACD
    # plt.subplot(2, 1, 2)
    # plt.plot(data['MACD'], label='MACD Line', color='blue')
    # plt.plot(data['MACD_Signal'], label='Signal Line', color='red')
    # plt.bar(data.index, data['MACD_Diff'], label='Histogram', color='grey', alpha=0.5)
    # plt.legend()
    # '''
    # logger.debug("Received arguments : df={}", df)


def fn_comparative_relative_strength_CRS_indicator(bch_sym: str, df_bch_sym: pd.DataFrame, sym: str, df_sym: pd.DataFrame, column_name: str,
) -> pd.DataFrame:
  """_summary_

  Args:
      bch_sym (str): _description_
      df_bch_sym (pd.DataFrame): _description_
      sym (str): _description_
      df_sym (pd.DataFrame): _description_
      column_name (str): _description_

  Returns:
      pd.DataFrame: _description_

  Example:
  >> fn_macd_indicator(df, "crs_50")
    """
  
  # set the lookback calculation period
  LENGTH = 50

  logger.debug("Received arguments : df_bch_sym=")
  m_oth.fn_df_print_first_last_rows(df_bch_sym, 3, 'ALL_COLS')
  logger.debug("Received arguments : df_sym=")
  m_oth.fn_df_print_first_last_rows(df_sym, 3, 'ALL_COLS')

  # benchmark might have holidays on some days while symbol can have on another day, meaning all records will not match on pd_time
  # we need to handle this by currently only taking the common rows on pd_time
  # Get the set of common pd_time values
  common_pd_time = set(df_bch_sym["pd_time"]).intersection(df_sym["pd_time"])
  print("---common_pd_time=", common_pd_time)
  # Filter df_bch_sym to keep only rows with pd_time in common_pd_time
  df_bch_sym_filtered = df_bch_sym[df_bch_sym["pd_time"].isin(common_pd_time)]
  # Filter df_bch_sym to keep only rows with pd_time in common_pd_time
  df_sym_filtered = df_sym[df_sym["pd_time"].isin(common_pd_time)]

  original_max_rows = pd.get_option('display.max_rows')
  # Set option to display all rows
  pd.set_option('display.max_rows', None)
  print("----- df_bch_sym_filtered ----")
  #m_oth.fn_df_get_first_last_rows(df_bch_sym_filtered, 3)
  print(df_bch_sym_filtered)
  print("----- df_sym_filtered ----")
  #m_oth.fn_df_get_first_last_rows(df_sym_filtered, 3)
  print(df_sym_filtered)
  # Reset the option to its original value
  pd.reset_option('display.max_rows')

  print("--- CRS_50 AAA --------Computing daily percentage change on both Sym and Benchmark ...")
  # Using .loc[:, "dly_pct_change"] ensures that the modifications are made on the original DataFrame and should eliminate the warning.
  df_bch_sym_filtered.loc[:, "dly_pct_change"] = df_bch_sym_filtered["close"].pct_change()
  df_sym_filtered.loc[:, "dly_pct_change"] = df_sym_filtered["close"].pct_change()

  # remove all unnecessary columns
  df_bch_sym_filtered = df_bch_sym_filtered[["pd_time", "close", "dly_pct_change"]]
  df_sym_filtered = df_sym_filtered[["pd_symbol", "pd_time", "close", "dly_pct_change"]]
  print("----- df_bch_sym_filtered ----")
  m_oth.fn_df_print_first_last_rows(df_bch_sym_filtered, 3, 'ALL_COLS')
  print("----- df_sym_filtered ----")
  m_oth.fn_df_print_first_last_rows(df_sym_filtered, 3, 'ALL_COLS')
  # df_sym = df_sym[['pd_time','close','dly_pct_change']]

  print("--- Merging the 2 dfs using pandas merge function ---")
  # uses pandas merge function to merge these two DataFrames on the common column 'pd_time'.
  # In the merged DataFrame, df_sym columns will have suffix '_SYMB' df_bch_sym columns will have suffix '_ETF'.
  df_merged = pd.merge(
      df_sym_filtered[["pd_symbol", "pd_time", "close", "dly_pct_change"]],
      df_bch_sym_filtered[["pd_time", "close", "dly_pct_change"]],
      on="pd_time",
      suffixes=("_SYMB", "_ETF")
  )

  print("--- MERGED DF ---")
  m_oth.fn_df_print_first_last_rows(df_merged, 3, 'ALL_COLS')
  df_merged["close"] = df_sym["close"]      # add the close column back to the merged df
  print("---YYY ---")
  print(df_merged.tail(3))
  
  # Calculate Comparative Relative Strength (CRS)
  # used my Trading Reference gdoc and TradingView RS pinecode from someone and ultimately ChatGPT for getting this right
  logger.debug("Calculating the Comparative Relative Strength (CRS) on {} against {}", sym, bch_sym)
  df_merged[column_name] = (
      df_merged["close_SYMB"]
      / df_merged["close_SYMB"].shift(LENGTH)
      / (df_merged["close_ETF"] / df_merged["close_ETF"].shift(LENGTH))
      - 1
  )

  # Create a boolean mask for the rows that we want update (ie where df_merged[column] is not empty/NaN)
  # ~ operator is a bitwise NOT, and it will invert the boolean values in the mask
  mask = ~df_merged[column_name].isna()
  
  # round the values to 3 decimal places in the last row only due to starting rows having null values
  # df_merged.iloc[-1, df_merged.columns.get_loc(column_name)] = df_merged.iloc[-1][
  #     column_name
  # ].round(3)
  # Update the values in the requiredcolumn for the rows that satisfy the condition
  df_merged.loc[mask, column_name] = df_merged.loc[mask, column_name].round(3)

  print("--- UPDATED MERGED DFs ---")
  pd.set_option('display.max_rows', None)
  print(df_merged)
  pd.reset_option('display.max_rows')


  df_sym[column_name] = df_merged[column_name]

  """
  # Plot - Comparative Relative Strength (CRS) Indicator
  axs[2].plot(df_merged['pd_time'], df_merged['Relative_Strength'], label='Comparative Relative Strength (CRS)', color='purple')
  axs[2].axhline(0, color='black', linestyle='dotted')       # draw a horizontal line
  # Calculate and plot Moving Average if show_MA is True
  # if show_MA:
  #     df_merged['MA'] = df_merged['Relative_Strength'].rolling(window=length_MA).mean()
  #     plt.plot(df_merged['MA'], label=f'MA ({length_MA})', color='gray')
  """

  logger.trace("-------df_sym.info={}------", df_sym.info())
  m_oth.fn_df_print_first_last_rows(df_sym, 3, 'ALL_COLS')
  return df_sym




def fn_compute_all_required_indicators(
    bch_sym: str,
    df_bch_sym: pd.DataFrame,
    sym: str,
    df_sym: pd.DataFrame,
) -> pd.DataFrame:
  """
  Computes all the required indicators for the given sym and benchmark sym.
  Currently these 8 -
  SMA_50
  SMA_200
  EMA_5
  EMA_13
  RSI_14
  MACD
  ADX
  CRS_50

  Args:
    bch_sym (str): the ticker sym of the benchmark stock.
    df_bch_sym (pd.DataFrame): the data frame of the benchmark stock.
    sym (str): the ticker sym of the stock for which the indicators are to be computed.
    df_sym (pd.DataFrame): the data frame of the stock for which the indicators are to be computed.
    column_name (str): the name of the column to be added to the data frame with the computed indicators.

  Returns:
    pd.DataFrame: the data frame with the computed indicators.
    IMPORTANT: it's the ORIGINAL df_sym dataframe itself that will be MODIFIED/appended with all the indicator columns

  """

  logger.log("MYNOTICE", "START: LOG-TAG-002 : Computing all the required indicators using dataframes for symbol={} and benchmark symbol = {}", sym, bch_sym)

  # we need this many records of past data to compute the indicators on the current row
  NUM_RECORDS_EXPECTED = 50
  IF_DELIMITER = ";"  # intra-field delimeter for the macd column

  # these are the names of the new columns that will be added to the dataframe with the computed indicators.
  COL_NAME_MACD = "macd_sig_hist"
  COL_NAME_ADX  = "dm_dp_adx"
  COL_NAME_CRS  = "crs_50"

  # print("-----A11 ----")
  # print(df_bch_sym)
  # print("-----A22 ----")
  # print(df_sym)

  logger.debug("Received arguments : bch_sym={} df_bch_sym=", bch_sym)
  m_oth.fn_df_print_first_last_rows(df_bch_sym, 3, 'ALL_COLS')
  logger.debug("Received arguments :           sym={}           df_sym=", sym)
  m_oth.fn_df_print_first_last_rows(df_sym, 3, 'ALL_COLS')
  num_recs = fn_check_data(df_sym)
  if num_recs < NUM_RECORDS_EXPECTED:
      logger.error("num_records={} less than expected records={}", num_recs, NUM_RECORDS_EXPECTED)
      # TODO: exit maybe ?

  # check if the symbol passed down is itself an index or ETF like SPY, NIFTY etc
  if bch_sym == sym:
    sym_is_benchmark = True
    logger.log("MYNOTICE", "symbol sym={} matches our predefined benchmark bch_sym={}", sym, bch_sym)
  else:  
    sym_is_benchmark = False

  # ----- 1. SMA_50 -----
  logger.debug("---Indicator 1 : SMA_50 ---")

  SMA_50_PERIOD=50
  df_sym["sma_50"] = ta.SMA(df_sym["close"], timeperiod=SMA_50_PERIOD)
  df_sym["sma_50"] = df_sym["sma_50"] .round(2)

  m_oth.fn_df_print_first_last_rows(df_sym, 3, 'ALL_COLS')

  # ------ 2. SMA_200 ---
  logger.debug("---Indicator 1 : SMA_200 ---")

  SMA_200_PERIOD=200
  df_sym["sma_200"] = ta.SMA(df_sym["close"], timeperiod=SMA_200_PERIOD)
  df_sym["sma_200"] = df_sym["sma_200"] .round(2)
  m_oth.fn_df_print_first_last_rows(df_sym, 3, 'ALL_COLS')

  # ------ 3. EMA_5 ------
  # TODO: this one
  logger.debug("--- TODO: EMA_5 ---")

  # ------ 4. EMA_13 ------
  logger.debug("---Indicator 4 : EMA_13 ---")

  EMA_13_PERIOD=13
  df_sym["ema_13"] = ta.EMA(df_sym["close"], timeperiod=EMA_13_PERIOD)
  df_sym["ema_13"] = df_sym["ema_13"].round(2)
  m_oth.fn_df_print_first_last_rows(df_sym, 3, 'ALL_COLS')

  # ------ 5. RSI_14 ------
  logger.debug("---Indicator 5 : RSI ---")

  RSI_PERIOD = 14
  df_sym["rsi_14"] = ta.RSI(df_sym["close"], timeperiod=RSI_PERIOD)
  df_sym["rsi_14"] = df_sym["rsi_14"].round(2)
  m_oth.fn_df_print_first_last_rows(df_sym, 3, 'ALL_COLS')

  # ------ 6. MACD ------
  logger.debug("---Indicator 6 : MACD ---")
  logger.debug("Input dataframe : df_sym={}", df_sym)

  MACD_FAST = 12
  MACD_SLOW = 26
  MACD_SIGNAL = 9
  df_tmp = pd.DataFrame(index=df_sym.index)
  na_macd, na_macd_signal, na_macd_hist = ta.MACD(df_sym["close"].to_numpy(), fastperiod=MACD_FAST, slowperiod=MACD_SLOW, signalperiod=MACD_SIGNAL)
  df_tmp["macd"] = na_macd
  df_tmp["signal"] = na_macd_signal
  df_tmp["histogram"] = na_macd_hist
  columns_to_round = ["macd", "signal", "histogram"]
  df_tmp[columns_to_round] = df_tmp[columns_to_round].round(2)

  df_sym[COL_NAME_MACD] = (df_tmp["macd"].astype(str) + IF_DELIMITER + df_tmp["signal"].astype(str) + IF_DELIMITER + df_tmp["histogram"].astype(str))
  logger.debug("Output dataframe : df_sym={}", df_sym)


  # ------ 7. ADX ------
  logger.debug("---Indicator 7 : ADX ---")
  logger.debug("Input dataframe : df_sym={}", df_sym)

  ADX_PERIOD = 14
  df_tmp = pd.DataFrame(index=df_sym.index)
  na_ADX = ta.ADX(df_sym["high"], df_sym["low"], df_sym["close"], ADX_PERIOD)
  na_DMI_MINUS = ta.MINUS_DI(df_sym["high"], df_sym["low"], df_sym["close"], ADX_PERIOD)
  na_DMI_PLUS = ta.PLUS_DI(df_sym["high"], df_sym["low"], df_sym["close"], ADX_PERIOD)
  df_tmp["dmi_minus"] = na_DMI_MINUS
  df_tmp["dmi_plus"] = na_DMI_PLUS
  df_tmp["adx"] = na_ADX
  columns_to_round = ["dmi_minus", "dmi_plus", "adx"]
  df_tmp[columns_to_round] = df_tmp[columns_to_round].round(2)

  df_sym[COL_NAME_ADX] = (df_tmp["dmi_minus"].astype(str)
      + IF_DELIMITER + df_tmp["dmi_plus"].astype(str)
      + IF_DELIMITER + df_tmp["adx"].astype(str)
  )
  logger.debug("Output dataframe : df_sym={}", df_sym)



  # ------ 8. CRS_50 ------
  logger.debug("---Indicator 8 : CRS_50---")
  
  if sym_is_benchmark:
    logger.debug("Not computing CRS_50 as the symbol {} is the benchmark itself ...", sym)
  else:
    CRS_LENGTH = 50
    # do not manipulate the original dfs as they have all the computed indicator values, so create independant copies
    df_tmp_bch_sym = df_bch_sym.copy()
    df_tmp_sym = df_sym.copy()
    
    df_tmp_bch_sym["dly_pct_change"] = df_tmp_bch_sym["close"].pct_change().round(3)
    df_tmp_sym["dly_pct_change"] = df_tmp_sym["close"].pct_change().round(3)
    # now reduce these 2 dataframes to keep only the required columns
    df_tmp_bch_sym = df_tmp_bch_sym[["pd_time", "close", "dly_pct_change"]]
    df_tmp_sym = df_tmp_sym[["pd_symbol", "pd_time", "close", "dly_pct_change"]]

    logger.debug("------crs_50  dataframe 1 = df_tmp_sym -----")
    logger.debug(df_tmp_sym)
    logger.debug("------crs_50  dataframe 2 = df_tmp_bch_sym -----")
    logger.debug(df_tmp_bch_sym)

    # Convert pd_time column values into pandas timestamp objects first and then convert those to python datetime objects
    df_tmp_sym["pd_time"] = pd.to_datetime(df_tmp_sym["pd_time"], utc=True).tolist()
    df_tmp_bch_sym["pd_time"] = pd.to_datetime(df_tmp_bch_sym["pd_time"], utc=True).tolist()

    # merge the 2 tmp dfs to get df_merged 
    df_merged = pd.merge(
        df_tmp_sym[["pd_symbol", "pd_time", "close", "dly_pct_change"]],
        df_tmp_bch_sym[["pd_time", "close", "dly_pct_change"]],
        on="pd_time",
        suffixes=("_SYMB", "_ETF"),
    )
    logger.debug("------crs_50  MERGED df on pd_time (df_merged = symbol and benchmark sym and benchmark quote data) BEFORE CRS computation -----")
    m_oth.fn_df_print_first_last_rows(df_merged, 5, 'ALL_COLS')

    # compute the CRS value for each row and put them in a new column
    logger.log("MYNOTICE", "Now actually computing CRS over symbol and benchmark dataframes and putting values into a merged df")
    # df_merged["close_SYMB"] / df_merged["close_SYMB"].shift(CRS_LENGTH) calculates the percentage change for the symbol over CRS_LENGTH rows.
    # df_merged["close_ETF"] / df_merged["close_ETF"].shift(CRS_LENGTH) calculates the percentage change for the ETF over the same period.
    # The division of the two changes computes the relative strength ratio, subtracting 1 centers it around zero.
    df_merged[COL_NAME_CRS] = (df_merged["close_SYMB"] / df_merged["close_SYMB"].shift(CRS_LENGTH) / 
                        (df_merged["close_ETF"] / df_merged["close_ETF"].shift(CRS_LENGTH)) - 1
    )
    # Round the CRS values to three decimal places
    df_merged[COL_NAME_CRS] = df_merged[COL_NAME_CRS].round(3)

    logger.debug("------crs_50  MERGED df AFTER CRS computation -----")
    m_oth.fn_df_print_first_last_rows(df_merged, 5, 'ALL_COLS')

    # find out which of the rows have null or not null values
    #mask = ~df_merged[COL_NAME_CRS].isna()
    #logger.trace("mask={}", mask)
    # apply rounding only on those that have non-null values
    #df_merged.loc[mask, COL_NAME_CRS] = df_merged.loc[mask, COL_NAME_CRS].round(3)
    columns_to_keep = ['pd_time', 'crs_50']
    df_merged = df_merged[columns_to_keep]
    logger.debug("------crs_50  Remove unwanted columns df_merged -----")
    m_oth.fn_df_print_first_last_rows(df_merged, 5, 'ALL_COLS')

    logger.debug("------crs_50  df_sym -----")
    m_oth.fn_df_print_first_last_rows(df_sym, 5, 'ALL_COLS')

    # we need to update the original df_sym column for crs_50 with the corresponding value from df_merged, based off pd_time
    # so create a new df based on merging of df_sym and df_merged based on pd_time
    #merged_df = pd.merge(df_sym, df_merged, how='left', on='pd_time')

    # Create a mapping dictionary from df_merged
    crs_50_mapping = df_merged.set_index('pd_time')['crs_50'].to_dict()
    #print("-- Z 33 -- crs_50_mapping = ", crs_50_mapping)

    #m_oth.fn_df_get_first_last_rows(merged_df, 5, 'ALL_COLS')
    # NOW FINALLY update the column in ORIGINAL df_sym with the corresponding values from df_merged
    #df_sym['COL_NAME_CRS'] = merged_df['COL_NAME_CRS']

    # Update values in df_sym based on matching pd_time in both df_sym and df_merged
    #df_sym.loc[df_sym['pd_time'].isin(df_merged['pd_time']), COL_NAME_CRS] = df_merged.loc[df_merged['pd_time'].isin(df_sym['pd_time']), COL_NAME_CRS]

    # Alternatively, update only if values exist in df_merged
    #df_sym['COL_NAME_CRS'] = merged_df['COL_NAME_CRS'].where(merged_df['COL_NAME_CRS'].notna(), df_sym['COL_NAME_CRS'])

    # Update the crs_50 column in df_sym with the mapped values
    df_sym['crs_50'] = df_sym['pd_time'].map(crs_50_mapping)
    logger.debug("Now computed all the indicator values and at the end of the function, resulting df_sym=")
    m_oth.fn_df_print_first_last_rows(df_sym, 3, 'ALL_COLS')

  logger.log("MYNOTICE", "END: LOG-TAG-002 : Completed computing all the required indicators using dataframes for symbol={} and benchmark symbol = {}", sym, bch_sym)
  return df_sym


# --------------------------------------------------------------------------------
def main():
    benchmark_symbol_file = "SPY.csv"
    benchmark_symbol = "SPY"
    symbol_file = "MSFT.csv"
    symbol = "MSFT"

    df_benchmark_symbol = pd.read_csv(benchmark_symbol_file)
    df_benchmark_symbol["Date"] = pd.to_datetime(df_benchmark_symbol["Date"])  # convert Date to a datetime object
    df_benchmark_symbol.rename(columns={'Date': 'pd_time', 'Symbol': 'pd_symbol', 'Close': 'close', 'High': 'high', 'Low': 'low', 'Open':'open'}, inplace=True)

    print(f"BENCHMARK = {benchmark_symbol} and df = {df_benchmark_symbol.tail(3)}")

    df_symbol = pd.read_csv(symbol_file)
    df_symbol["Date"] = pd.to_datetime(df_symbol["Date"])  # convert Date to a datetime object
    df_symbol.rename(columns={'Date': 'pd_time', 'Symbol': 'pd_symbol', 'Close': 'close', 'High': 'high', 'Low': 'low', 'Open':'open'}, inplace=True)
    print(f"SYMBOL = {symbol} and df = {df_symbol.tail(3)}")

    # fn_relative_strength_chart(benchmark_symbol, df_benchmark_symbol, symbol, df_symbol)
    #fn_comparative_relative_strength_CRS_indicator(benchmark_symbol: str, df_benchmark_symbol: pd.DataFrame, symbol: str, df_symbol: pd.DataFrame) -> pd.DataFrame:
    fn_compute_all_required_indicators(benchmark_symbol, df_benchmark_symbol, symbol, df_symbol)


#main()

