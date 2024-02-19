import sys

import pandas as pd
import numpy as np
from loguru import logger


def fn_df_get_first_last_rows(df: pd.DataFrame, num_rows: int, column_opt: str):

  
    # take the first n and last n rows of df and print with logger

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


def fn_set_logger(enable_debug_mode: bool):
  """
  Remove the default logger and set the logging level.

  Args:
    enable_debug_mode (bool): Whether to set the logging level to DEBUG or not.
    if false, it will take our default of INFO.

  Returns:
    None

  """

  if enable_debug_mode:
    #LOGGING_LEVEL = "TRACE"
    LOGGING_LEVEL = 'DEBUG'     # this is the loguru default
  else:
    LOGGING_LEVEL = "INFO"  # our default logging level

  logger.remove()  # All configured handlers are removed
  
  LOGGING_LEVEL = 'DEBUG'  # this is the loguru default
  #LOGGING_LEVEL = "INFO"  # our default logging level
  
  logger.add(sys.stderr, level=LOGGING_LEVEL)  # sets the logging level
  
  curr_level = logger.level(LOGGING_LEVEL)     # get the current logging level
  logger.info("Logging level set to {} ", curr_level)  # Level(name='DEBUG', no=10, color='<blue><bold>', icon='🐞')
  logger.debug("Setting for loguru logger level {} : level.name={} level.no={}  level.color={} level.icon={}", LOGGING_LEVEL, curr_level.name, curr_level.no, curr_level.color, curr_level.icon)
  
  # Check if the "MYNOTICE" level already exists
  try:
    str_level_name="MYNOTICE"
    my_level = logger.level(str_level_name)
    print("MYNOTICE level already exists - ", my_level)
    logger.debug("My existing logger level {} : level.name={} level.no={}  level.color={} level.icon={}", str_level_name, my_level.name, my_level.no, my_level.color, my_level.icon)
  except ValueError:  # Level not found
    # set customized logging level
    MYNOTICE=21
    #logger.level("MYNOTICE", no=MYNOTICE, color="<LIGHT-YELLOW>", icon="@")
    logger.level("MYNOTICE", no=MYNOTICE, color="<black><LIGHT-YELLOW>", icon="@")
    this_level = logger.level("MYNOTICE")
    logger.log("MYNOTICE", "New logging level set with values {}", this_level)
    logger.debug("Setting for loguru logger level MYNOTICE : level.name={} level.no={}  level.color={} level.icon={}", this_level.name, this_level.no, this_level.color, this_level.icon)


