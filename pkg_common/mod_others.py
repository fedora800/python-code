import sys
import time
import inspect
import traceback

import pandas as pd
import numpy as np
from loguru import logger




def fn_inspect_caller_functions():

  # print caller of the function of interest to us
  logger.debug('inspect: this function was invoked by -', inspect.stack()[2].function)

  stack = traceback.extract_stack()[:-1]  # exclude the current frame because we are interested in the caller of the caller and higher up
  for frame in stack:
    logger.debug("File: {}, Line: {} Function: {} calls =>", frame.filename, frame.lineno, frame.name)


def fn_sleep_for_seconds(seconds: int) -> None:
  """_summary_

  Args:
      seconds (int): number of seconds for the program to sleep
  """

  try:
    # Sleep for n seconds
    logger.debug("Sleeping for {} seconds", seconds)
    time.sleep(seconds)

  except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C)
    logger.debug("Sleep interrupted by user")



def fn_df_get_first_last_rows(df: pd.DataFrame, num_rows: int, column_opt: str):
  """ print with logger module the first n and last n rows of df and we can choose which columns to print 

  Args:
      df (pd.DataFrame): _description_
      num_rows (int): _description_
      column_opt (str): for which columns need to be displayed
          valid options are : ALL_COLS, IND_COLS
  """
 
  lst_column_names = []
  if column_opt == 'ALL_COLS':
    # print all columns
    lst_column_names = df.columns.tolist()
  elif column_opt == 'IND_COLS':
    # print only the main indicators
#    lst_column_names = [ "pd_symbol", "pd_time", "close", "volume", "ema_5", "ema_13", "sma_50", "sma_200", "rsi_14", "macd_sig_hist", "dm_dp_adx", "crs_50" ]
    lst_column_names = [ "pd_symbol", "pd_time", "close", "volume", "rsi_14", "macd_sig_hist", "dm_dp_adx", "crs_50" ]
  else:
    logger.error("Wrong parameter value passed : column_opt = {}", column_opt)

  # Get only the selected columns into a df
  df_print = df[lst_column_names]

  df_first_last = pd.concat([df_print.head(num_rows), df_print.tail(num_rows)])
  logger.debug("df with only first and last [{}] rows = \n{}", num_rows, df_first_last)


def fn_df_get_first_last_dates(df: pd.DataFrame) -> str:
  # Find the dates of the first and last row of df and return them as a comma seperated string

  ret_str = df['pd_time'].head(1).item() .strftime('%Y-%m-%d %H:%M:%S') + ',' + df['pd_time'].tail(1).item() .strftime('%Y-%m-%d %H:%M:%S')
  logger.debug("ret_str = {}", ret_str)



def fn_modify_dataframe_per_our_requirements(sym: str, df: pd.DataFrame):
  '''
  Input df :
                  Open   High    Low  Close  Adj Close  Volume
     Date
     2022-08-04  49.90  49.90  48.83  49.48      49.31  263700
     2022-08-05  49.22  50.01  49.08  49.98      49.80  105100
     2022-08-08  50.17  50.90  49.92  49.96      49.78   68200
     2022-08-09  49.79  49.96  49.35  49.57      49.40  165700
     2022-08-10  50.69  51.25  50.69  51.18      51.00  160700

  Output df :
         pd_symbol                   pd_time   open   high    low  close  volume  ema_5  ema_13  sma_50  sma_200  rsi_14  macd_sig_hist  dm_dp_adx  crs_50
     0        HACK 2022-08-04 00:00:00+00:00  49.90  49.90  48.83  49.48  263700    NaN     NaN     NaN      NaN     NaN            NaN        NaN     NaN
     1        HACK 2022-08-05 00:00:00+00:00  49.22  50.01  49.08  49.98  105100    NaN     NaN     NaN      NaN     NaN            NaN        NaN     NaN
     2        HACK 2022-08-08 00:00:00+00:00  50.17  50.90  49.92  49.96   68200    NaN     NaN     NaN      NaN     NaN            NaN        NaN     NaN
     3        HACK 2022-08-09 00:00:00+00:00  49.79  49.96  49.35  49.57  165700    NaN     NaN     NaN      NaN     NaN            NaN        NaN     NaN
     4        HACK 2022-08-10 00:00:00+00:00  50.69  51.25  50.69  51.18  160700    NaN     NaN     NaN      NaN     NaN            NaN        NaN     NaN

  '''

  logger.debug("------------------ fn_modify_dataframe_per_our_requirements ----  {}  --- START -----", sym)
  logger.debug("input df = ")
  fn_df_get_first_last_rows(df, 3, 'ALL_COLS')

  # we are trying to make this df exactly same in format as the data we have from tbl_price_data_1day when put into a df
  df.reset_index(inplace=True)  # reset the Date index and make it into a column by itself. will be the 1st column
  df.drop(columns=['Adj Close'], inplace=True)
  df.columns = df.columns.str.lower()  # convert header/column names to lowercase
  df = df.rename(columns={'date': 'pd_time'})
  df['pd_time'] = pd.to_datetime(df['pd_time'], format='%Y-%m-%d', utc=True)
  df['pd_time'] = df['pd_time'].dt.normalize()    # Normalize the time part to midnight
  df.insert(0, "pd_symbol", sym) # add Symbol as 1st column after date
  new_columns = ['ema_5', 'ema_13', 'sma_50', 'sma_200', 'rsi_14', 'macd_sig_hist', 'dm_dp_adx', 'crs_50']      #  define the names of the new columns
  df_return = df.assign(**{col: np.NaN for col in new_columns})   #  add the new columns with value NaN for each column across all rows

  logger.debug("converted df_return =")
  fn_df_get_first_last_rows(df_return, 3, 'ALL_COLS')
  logger.debug("------------------ fn_modify_dataframe_per_our_requirements ----  {}  --- END -----", sym)
  return df_return


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
  logger.add(sys.stderr, level=LOGGING_LEVEL)  # sets the logging level
  
  curr_level = logger.level(LOGGING_LEVEL)     # get the current logging level
  logger.info("Logging level set to {} ", curr_level)  # Level(name='DEBUG', no=10, color='<blue><bold>', icon='🐞')
  logger.debug("Setting for loguru logger level {} : level.name={} level.no={}  level.color={} level.icon={}", LOGGING_LEVEL, curr_level.name, curr_level.no, curr_level.color, curr_level.icon)
  
  # Check if the "MYNOTICE" level already exists
  try:
    str_level_name="MYNOTICE"
    my_level = logger.level(str_level_name)
    logger.debug("MYNOTICE level already exists - ", my_level)
    logger.debug("My existing logger level {} : level.name={} level.no={}  level.color={} level.icon={}", str_level_name, my_level.name, my_level.no, my_level.color, my_level.icon)
  except ValueError:  # Level not found
    # set customized logging level
    MYNOTICE=21
    #logger.level("MYNOTICE", no=MYNOTICE, color="<LIGHT-YELLOW>", icon="@")
    #logger.level("MYNOTICE", no=MYNOTICE, color="<black><LIGHT-YELLOW>", icon="@")
    logger.level("MYNOTICE", no=MYNOTICE, color="<magenta>", icon="@")
    this_level = logger.level("MYNOTICE")
    logger.log("MYNOTICE", "New logging level set with values {}", this_level)
    logger.debug("Setting for loguru logger level MYNOTICE : level.name={} level.no={}  level.color={} level.icon={}", this_level.name, this_level.no, this_level.color, this_level.icon)


