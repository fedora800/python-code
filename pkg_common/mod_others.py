import sys
from datetime import timezone
import pandas as pd
import numpy as np
from loguru import logger


def fn_df_get_first_last(df: pd.DataFrame, num_rows: int):
  # take the first n and last n rows of df and return them as a dataframe

  df_first_last = pd.concat([df.head(num_rows), df.tail(num_rows)])
  logger.debug("df with only first and last [{}] rows = \n{}", num_rows, df_first_last)


def fn_modify_dataframe_per_our_requirements(sym: str, df: pd.DataFrame):

  print("----- MOD DF ------------START--------------")

  logger.info("modifying df as per our requirements ...")
  logger.debug("before = ")
  print(df.info())
  logger.debug(fn_df_get_first_last(df, 2))

  # we are trying to make this df exactly same in format as the data we have from tbl_price_data_1day when put into a df
  df.reset_index(inplace=True)  # reset the Date index and make it into a column by itself. will be the 1st column
  df.drop(columns=['Adj Close'], inplace=True)
  df.columns = df.columns.str.lower()  # convert header/column names to lowercase
  df = df.rename(columns={'date': 'pd_time'})
  df['pd_time'] = pd.to_datetime(df['pd_time'], format='%Y-%m-%d', utc=True)
  df['pd_time'] = df['pd_time'].dt.normalize()    # Normalize the time part to midnight
  df.insert(0, "pd_symbol", sym) # add Symbol as 1st column after date
  new_columns = ['ema_5', 'ema_13', 'sma_50', 'sma_200', 'rsi_14', 'macd_sig_hist', 'dm_dp_adx', 'crs_50']      #  define the names of the new columns
  df = df.assign(**{col: "None" for col in new_columns})   #  add the new columns with value "None" for each column across all rows
  logger.debug("after =")
  logger.debug(fn_df_get_first_last(df, 2))
  print(df.info())
  print("----- MOD DF ------------END--------------")
  return df

def fn_set_logger(debug_mode: bool):
  """
  Remove the default logger and set the logging level.

  Args:
    DEBUG_MODE (bool): Whether to set the logging level to DEBUG or not.

  Returns:
    None

  """

  logger.remove()  # First remove the default logger

  if debug_mode:
      LOGGING_LEVEL = "TRACE"
      # LOGGING_LEVEL = 'DEBUG'     # this is the loguru default
  else:
      LOGGING_LEVEL = "INFO"  # our default logging level

  logger.add(sys.stderr, level=LOGGING_LEVEL)  # sets the logging level
  logger.info("Logging level set to {} ", LOGGING_LEVEL)

