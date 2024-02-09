from loguru import logger
import pandas as pd
import talib as ta


def check_data(df: pd.DataFrame, exp_recs: int):
    """_summary_

    Args:
        df (pd.DataFrame): contains the data_
        exp_recs (int): a number mentioning minimum number of records we expect in the df

    Returns:
        int: number of records in the dataframe
    """

    # logger.debug("Received arguments : df={} and exp_recs={}", df, exp_recs)

    num_records = df.shape[0]
    num_columns = df.shape[1]
    logger.debug(
        "Received arguments : num_records={} and num_columns={}",
        num_records,
        num_columns,
    )
    logger.trace("df info={}", df.info())

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
    df_tmp = pd.DataFrame()

    logger.debug("Received arguments : df={}", df)
    check_data(df, 300)

    na_ADX = ta.ADX(df["high"], df["low"], df["close"], TIME_PERIOD)
    na_DMI_MINUS = ta.MINUS_DI(df["high"], df["low"], df["close"], TIME_PERIOD)
    na_DMI_PLUS = ta.PLUS_DI(df["high"], df["low"], df["close"], TIME_PERIOD)

    # store in a temporary df
    df_tmp["dmi_minus"] = na_DMI_MINUS
    df_tmp["dmi_plus"] = na_DMI_PLUS
    df_tmp["adx"] = na_ADX

    # round the values to 2 decimal places in the last row only due to starting rows having null values
    df_tmp.iloc[-1, df_tmp.columns.get_loc("dmi_minus")] = df_tmp.iloc[-1][
        "dmi_minus"
    ].round(2)
    df_tmp.iloc[-1, df_tmp.columns.get_loc("dmi_plus")] = df_tmp.iloc[-1][
        "dmi_plus"
    ].round(2)
    df_tmp.iloc[-1, df_tmp.columns.get_loc("adx")] = df_tmp.iloc[-1]["adx"].round(2)

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
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    IF_DELIMITER = ";"  # intra-field delimeter for the macd column
    df_tmp = pd.DataFrame()

    logger.debug("Received arguments : df={}", df)
    num_recs = check_data(df, 300)

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
    df_tmp.iloc[-1, df_tmp.columns.get_loc("signal")] = df_tmp.iloc[-1]["signal"].round(
        2
    )
    df_tmp.iloc[-1, df_tmp.columns.get_loc("histogram")] = df_tmp.iloc[-1][
        "histogram"
    ].round(2)

    df[column_name] = (
        df_tmp["macd"].astype(str)
        + IF_DELIMITER
        + df_tmp["signal"].astype(str)
        + IF_DELIMITER
        + df_tmp["histogram"].astype(str)
    )

    logger.trace("-------df.info={}---df={}---", df.info(), df)
    logger.debug("--dfhead=\n{}----dftail=\n{}----", df.head(1), df.tail(1))

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


def fn_relative_strength_indicator(df: pd.DataFrame):
    PERIOD = 14

    logger.debug("Received arguments : df={}", df)
    num_recs = check_data(df, 300)

    if num_recs < 200:
        logger.error("num_records={} less than expected records={}", num_recs, 200)
        # TODO: exit maybe ?

    df["rsi_14"] = ta.RSI(df["close"], timeperiod=PERIOD)
    logger.debug("--dfhead={}----dftail={}----", df.head(1), df.tail(1))

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


def fn_comparative_relative_strength_CRS_indicator(
    benchmark_symbol: str,
    df_benchmark_symbol: pd.DataFrame,
    symbol: str,
    df_symbol: pd.DataFrame,
    column_name: str,
) -> pd.DataFrame:
    # set the lookback calculation period
    LENGTH = 50

    logger.debug(
        "Received arguments : benchmark_symbol={} symbol={}", benchmark_symbol, symbol
    )
    logger.debug("Received arguments : df_benchmark_symbol={}", df_benchmark_symbol)
    logger.debug("Received arguments : df_symbol={}", df_symbol)

    print("Computing daily percentage change on both Symbol and Benchmark ...")
    df_benchmark_symbol["dly_pct_change"] = df_benchmark_symbol["close"].pct_change()
    df_benchmark_symbol = df_benchmark_symbol[
        ["pd_time", "close", "dly_pct_change"]
    ]  # remove all unnecessary columns
    print(df_benchmark_symbol.tail(3))
    df_symbol["dly_pct_change"] = df_symbol["close"].pct_change()
    # df_symbol = df_symbol[['pd_time','close','dly_pct_change']]
    df_symbol = df_symbol[["pd_symbol", "pd_time", "close", "dly_pct_change"]]
    print(df_symbol.tail(3))

    print("--- MERGED DFs ---")
    # uses pandas merge function to merge these two DataFrames on the common column 'pd_time'.
    # In the merged DataFrame, df_symbol columns will have suffix '_SYMB' df_benchmark_symbol columns will have suffix '_ETF'.
    df_merged = pd.merge(
        df_symbol[["pd_symbol", "pd_time", "close", "dly_pct_change"]],
        df_benchmark_symbol[["pd_time", "close", "dly_pct_change"]],
        on="pd_time",
        suffixes=("_SYMB", "_ETF"),
    )

    print("---XXX ---")
    print(df_merged.tail(3))
    df_merged["close"] = df_symbol[
        "close"
    ]  # add the close column back to the merged df
    print(df_merged.tail(3))
    print("---YYY ---")

    # Calculate Comparative Relative Strength (CRS)
    # used my Trading Reference gdoc and TradingView RS pinecode from someone and ultimately ChatGPT for getting this right
    logger.debug(
        "Calculating the Comparative Relative Strength (CRS) on {} against {}",
        symbol,
        benchmark_symbol,
    )
    df_merged["crs"] = (
        df_merged["close_SYMB"]
        / df_merged["close_SYMB"].shift(LENGTH)
        / (df_merged["close_ETF"] / df_merged["close_ETF"].shift(LENGTH))
        - 1
    )
    # round the values to 3 decimal places in the last row only due to starting rows having null values
    df_merged.iloc[-1, df_merged.columns.get_loc(column_name)] = df_merged.iloc[-1][
        column_name
    ].round(3)

    print("--- UPDATED MERGED DFs ---")
    print(df_merged.tail(3))

    """
  # Plot - Comparative Relative Strength (CRS) Indicator
  axs[2].plot(df_merged['pd_time'], df_merged['Relative_Strength'], label='Comparative Relative Strength (CRS)', color='purple')
  axs[2].axhline(0, color='black', linestyle='dotted')       # draw a horizontal line
  # Calculate and plot Moving Average if show_MA is True
  # if show_MA:
  #     df_merged['MA'] = df_merged['Relative_Strength'].rolling(window=length_MA).mean()
  #     plt.plot(df_merged['MA'], label=f'MA ({length_MA})', color='gray')
  """

    return df_merged


def fn_compute_all_required_indicators(
    benchmark_symbol: str,
    df_benchmark_symbol: pd.DataFrame,
    symbol: str,
    df_symbol: pd.DataFrame
) -> pd.DataFrame:
  """
  Computes all the required indicators for the given symbol and benchmark symbol.
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
    benchmark_symbol (str): the ticker symbol of the benchmark stock.
    df_benchmark_symbol (pd.DataFrame): the data frame of the benchmark stock.
    symbol (str): the ticker symbol of the stock for which the indicators are to be computed.
    df_symbol (pd.DataFrame): the data frame of the stock for which the indicators are to be computed.
    column_name (str): the name of the column to be added to the data frame with the computed indicators.

  Returns:
    pd.DataFrame: the data frame with the computed indicators.

  """

  NUM_RECORDS_EXPECTED = 300
  IF_DELIMITER = ";"  # intra-field delimeter for the macd column
  RSI_PERIOD = 14
  MACD_FAST = 12
  MACD_SLOW = 26
  MACD_SIGNAL = 9
  ADX_PERIOD = 14
  CRS_LENGTH = 50
  # these are the names of the new columns that will be added to the dataframe with the computed indicators.
  COL_NAME_MACD = "macd_sig_hist"
  COL_NAME_ADX  = "dm_dp_adx"
  COL_NAME_CRS  = "crs_50"

  logger.debug(
      "Received arguments : benchmark_symbol={} symbol={}", benchmark_symbol, symbol
  )
  logger.debug("Received arguments : df_benchmark_symbol={}", df_benchmark_symbol)
  logger.debug("Received arguments : df_symbol={}", df_symbol)

  num_recs = check_data(df_symbol, NUM_RECORDS_EXPECTED)
  if num_recs < 200:
      logger.error(
          "num_records={} less than expected records={}",
          num_recs,
          NUM_RECORDS_EXPECTED,
      )
      # TODO: exit maybe ?

  # ----- 1. SMA_50 -----
  print("--- SMA_50 ---")

  # ------ 2. SMA_200 ---
  print("--- SMA_200 ---")

  # ------ 3. EMA_5 ------
  print("--- EMA_5 ---")

  # ------ 4. EMA_13 ------
  print("--- EMA_13 ---")

  # ------ 5. RSI_14 ------
  df_symbol["rsi_14"] = ta.RSI(df_symbol["close"], timeperiod=RSI_PERIOD)

  # ------ 6. MACD ------
  df_tmp = pd.DataFrame()
  na_macd, na_macd_signal, na_macd_hist = ta.MACD(
      df_symbol["close"].to_numpy(),
      fastperiod=MACD_FAST,
      slowperiod=MACD_SLOW,
      signalperiod=MACD_SIGNAL,
  )
  df_tmp["macd"] = na_macd
  df_tmp["signal"] = na_macd_signal
  df_tmp["histogram"] = na_macd_hist

  df_tmp.iloc[-1, df_tmp.columns.get_loc("macd")] = df_tmp.iloc[-1]["macd"].round(2)
  df_tmp.iloc[-1, df_tmp.columns.get_loc("signal")] = df_tmp.iloc[-1]["signal"].round(2)
  df_tmp.iloc[-1, df_tmp.columns.get_loc("histogram")] = df_tmp.iloc[-1]["histogram"].round(2)

  df_symbol[COL_NAME_MACD] = (
      df_tmp["macd"].astype(str)
      + IF_DELIMITER + df_tmp["signal"].astype(str)
      + IF_DELIMITER + df_tmp["histogram"].astype(str)
  )

  # ------ 7. ADX ------
  df_tmp = pd.DataFrame()
  na_ADX = ta.ADX(df_symbol["high"], df_symbol["low"], df_symbol["close"], ADX_PERIOD)
  na_DMI_MINUS = ta.MINUS_DI(df_symbol["high"], df_symbol["low"], df_symbol["close"], ADX_PERIOD)
  na_DMI_PLUS = ta.PLUS_DI(df_symbol["high"], df_symbol["low"], df_symbol["close"], ADX_PERIOD)
  df_tmp["dmi_minus"] = na_DMI_MINUS
  df_tmp["dmi_plus"] = na_DMI_PLUS
  df_tmp["adx"] = na_ADX

  df_tmp.iloc[-1, df_tmp.columns.get_loc("dmi_minus")] = df_tmp.iloc[-1]["dmi_minus"].round(2)
  df_tmp.iloc[-1, df_tmp.columns.get_loc("dmi_plus")] = df_tmp.iloc[-1]["dmi_plus"].round(2)
  df_tmp.iloc[-1, df_tmp.columns.get_loc("adx")] = df_tmp.iloc[-1]["adx"].round(2)

  df_symbol[COL_NAME_ADX] = (df_tmp["dmi_minus"].astype(str)
      + IF_DELIMITER + df_tmp["dmi_plus"].astype(str)
      + IF_DELIMITER + df_tmp["adx"].astype(str)
  )

  # ------ 8. CRS_50 ------
  df_benchmark_symbol["dly_pct_change"] = df_benchmark_symbol["close"].pct_change()
  df_benchmark_symbol = df_benchmark_symbol[["pd_time", "close", "dly_pct_change"]]
  df_symbol["dly_pct_change"] = df_symbol["close"].pct_change()
  df_symbol = df_symbol[["pd_symbol", "pd_time", "close", "dly_pct_change"]]

  df_merged = pd.merge(
      df_symbol[["pd_symbol", "pd_time", "close", "dly_pct_change"]],
      df_benchmark_symbol[["pd_time", "close", "dly_pct_change"]],
      on="pd_time",
      suffixes=("_SYMB", "_ETF"),
  )
  df_merged["close"] = df_symbol["close"]

  df_merged[COL_NAME_CRS] = (df_merged["close_SYMB"] / df_merged["close_SYMB"].shift(CRS_LENGTH) / 
                      (df_merged["close_ETF"] / df_merged["close_ETF"].shift(CRS_LENGTH)) - 1
  )
  df_merged.iloc[-1, df_merged.columns.get_loc(COL_NAME_CRS)] = df_merged.iloc[-1][COL_NAME_CRS].round(3)
  df_symbol[COL_NAME_CRS] = df_merged[COL_NAME_CRS]

  logger.debug("--dfhead={}----dftail={}----", df_symbol.head(1), df_symbol.tail(1))

  return df_symbol


# --------------------------------------------------------------------------------
def main():
    benchmark_symbol_file = "SPY.csv"
    benchmark_symbol = "SPY"
    symbol_file = "MSFT.csv"
    symbol = "MSFT"

    df_benchmark_symbol = pd.read_csv(benchmark_symbol_file)
    df_benchmark_symbol["Date"] = pd.to_datetime(
        df_benchmark_symbol["Date"]
    )  # convert Date to a datetime object
    print(f"BENCHMARK = {benchmark_symbol} and df = {df_benchmark_symbol.tail(3)}")

    df_symbol = pd.read_csv(symbol_file)
    df_symbol["Date"] = pd.to_datetime(
        df_symbol["Date"]
    )  # convert Date to a datetime object
    print(f"SYMBOL = {symbol} and df = {df_symbol.tail(3)}")

    # fn_relative_strength_chart(benchmark_symbol, df_benchmark_symbol, symbol, df_symbol)
    # fn_comparative_relative_strength_CRS_indicator(benchmark_symbol: str, df_benchmark_symbol: pd.DataFrame, symbol: str, df_symbol: pd.DataFrame) -> pd.DataFrame:
