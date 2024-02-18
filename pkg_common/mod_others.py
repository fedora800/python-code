import sys

import pandas as pd
import numpy as np
from loguru import logger


def fn_df_get_first_last_rows(df: pd.DataFrame, num_rows: int):
  # take the first n and last n rows of df and return them as a dataframe

  df_first_last = pd.concat([df.head(num_rows), df.tail(num_rows)])
  logger.debug("df with only first and last [{}] rows = \n{}", num_rows, df_first_last)


def fn_df_get_first_last_dates(df: pd.DataFrame) -> str:
  # Find the dates of the first and last row of df and return them as a comma seperated string

  ret_str = df.iloc[0]["pd_time"] + ',' + df.iloc[-1]["pd_time"]
  logger.debug("ret_str = {}", ret_str)



def fn_modify_dataframe_per_our_requirements(sym: str, df: pd.DataFrame):

  print("----- MOD DF ------------START--------------")

  logger.info("modifying df as per our requirements ...")
  logger.debug("before = ")
  logger.trace(df.info())
  logger.debug(fn_df_get_first_last_rows(df, 2))

  # we are trying to make this df exactly same in format as the data we have from tbl_price_data_1day when put into a df
  df.reset_index(inplace=True)  # reset the Date index and make it into a column by itself. will be the 1st column
  df.drop(columns=['Adj Close'], inplace=True)
  df.columns = df.columns.str.lower()  # convert header/column names to lowercase
  df = df.rename(columns={'date': 'pd_time'})
  df['pd_time'] = pd.to_datetime(df['pd_time'], format='%Y-%m-%d', utc=True)
  df['pd_time'] = df['pd_time'].dt.normalize()    # Normalize the time part to midnight
  df.insert(0, "pd_symbol", sym) # add Symbol as 1st column after date
  new_columns = ['ema_5', 'ema_13', 'sma_50', 'sma_200', 'rsi_14', 'macd_sig_hist', 'dm_dp_adx', 'crs_50']      #  define the names of the new columns
  df = df.assign(**{col: np.NaN for col in new_columns})   #  add the new columns with value NaN for each column across all rows
  logger.debug("after =")
  logger.debug(fn_df_get_first_last_rows(df, 2))
  print(df.info())
  print("----- MOD DF ------------END--------------")
  return df


def fn_set_logger(debug_mode: bool):
  """
  Remove the default logger and set the logging level.

  Args:
    debug_mode (bool): Whether to set the logging level to DEBUG or not.
    if false, it will take our default of INFO.

  Returns:
    None

  """

  logger.remove()  # All configured handlers are removed

  if debug_mode:
    #LOGGING_LEVEL = "TRACE"
    LOGGING_LEVEL = 'DEBUG'     # this is the loguru default
  else:
    LOGGING_LEVEL = "INFO"  # our default logging level

  logger.add(sys.stderr, level=LOGGING_LEVEL)  # sets the logging level

  current_logging_level = logger.level   # get the current logging level
  logger.info("Logging level set to {} ", current_logging_level)

  # compares the current logger level "name" with "DEBUG"
  # The result will be True if it matches and False otherwise.
  is_debug_enabled = logger.level == "DEBUG"
  logger.warning("Is DEBUG level enabled? {}", is_debug_enabled)

  # set our customized logging level named NOTICE
  #logger.level("NOTICE", no=15, color="<light-magenta>", icon="@")
  #notice_level = logger.level("NOTICE")
  #logger.log("NOTICE", "New logging level set with values {}", notice_level)

  # set our customized logging level named KEYACTION
  logger.level("KEYACTION", no=16, color="<light-magenta>", icon="@")
  keyaction_level = logger.level("KEYACTION")
  logger.log("KEYACTION", "New logging level set with values {}", keyaction_level)


'''
  # to show what setting we have for that particular logger level
  level = logger.level("ERROR")   # returns A |namedtuple| containing information about the level.
  print(level)    # => Level(name='ERROR', no=40, color='<red><bold>', icon='❌')

  2024-02-18 09:08:03.983 | INFO     | mod_others:fn_set_logger:64 - Logging level set to <bound method Logger.level of <loguru.logger handlers=[(id=1, level=20, sink=<stderr>)]>> 
2024-02-18 09:08:03.984 | WARNING  | mod_others:fn_set_logger:69 - Is DEBUG level enabled? False
'''
