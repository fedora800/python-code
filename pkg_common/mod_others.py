import os
import sys
import time
import inspect
import traceback
import requests
import certifi

import pandas as pd
import numpy as np
from loguru import logger




def fn_inspect_caller_functions():

  # print caller of the function of interest to us
  logger.debug('inspect: this function was invoked by -', inspect.stack()[2].function)

  stack = traceback.extract_stack()[:-1]  # exclude the current frame because we are interested in the caller of the caller and higher up
  for frame in stack:
    logger.debug("File: {}, Line: {} Function: {} calls =>", frame.filename, frame.lineno, frame.name)
    #print("   File: {}, Line: {}, Function: {} calls =>".format(os.path.basename(frame.filename), frame.lineno, frame.name,))



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



def fn_df_print_first_last_rows(df: pd.DataFrame, num_rows: int, column_opt: str):
  """ print with logger module the first n and last n rows of df and we can choose which columns to print 

  Args:
      df (pd.DataFrame): df containing the data
      num_rows (int): number of rows to print
      column_opt (str): which columns need to be displayed
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
  logger.debug("df with only first and last [{}] rows = \n[  {}  ]", num_rows, df_first_last)

  df.info
  logger.debug("Number of levels in columns = {}", df.columns.nlevels)
  if df.columns.nlevels == 1:
    logger.debug("Columns are a regular Index:", df.columns.tolist())
  else:
    logger.debug("Columns are a MultiIndex. Levels = {}", df.columns.levels)
    #print("Full structure:")
    #print(df.columns.to_frame(index=False))  # Converts MultiIndex to a DataFrame




def fn_df_get_first_last_dates(df: pd.DataFrame) -> str:
  # Find the dates of the first and last row of df and return them as a comma seperated string

  ret_str = df['pd_time'].head(1).item() .strftime('%Y-%m-%d %H:%M:%S') + ',' + df['pd_time'].tail(1).item() .strftime('%Y-%m-%d %H:%M:%S')
  logger.debug("ret_str = {}", ret_str)



def fn_modify_dataframe_per_our_requirements(sym: str, df: pd.DataFrame):
  '''
  Input df :
                  Open   High    Low  Close  Volume
     Date08-04  49.90  49.90  48.83  49.48   263700
     2022-08-05  49.22  50.01  49.08  49.98  105100
     2022-08-08  50.17  50.90  49.92  49.96   68200
     2022-08-09  49.79  49.96  49.35  49.57  165700
     2022-08-10  50.69  51.25  50.69  51.18  160700

         [  Close    High     Low    Open   Volume
2025-01-03  157.83  158.44  154.49  155.42  5885800
2025-01-06  159.85  165.67  159.33  159.33  9599800
2025-01-07  160.52  163.45  159.25  162.00  7666000
2025-01-15  164.41  165.45  162.09  162.10  9284000
2025-01-16  161.43  165.84  161.28  165.35  7188900
2025-01-17  164.56  165.61  163.10  165.38  8065900  ]

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
  fn_df_print_first_last_rows(df, 3, 'ALL_COLS')


  # we are trying to make this df exactly same in format as the data we have from tbl_price_data_1day when put into a df
  #df.reset_index(inplace=True)  # reset the Date index and make it into a column by itself. will be the 1st column

  #df.drop(columns=['Adj Close'], inplace=True)   #new version of yfinance does not download this column by default
  df.columns = df.columns.str.lower()  # convert all header/column names to lowercase
  df = df.rename(columns={'date': 'pd_time'})
  df['pd_time'] = pd.to_datetime(df['pd_time'], format='%Y-%m-%d', utc=True)
  df['pd_time'] = df['pd_time'].dt.normalize()    # Normalize the time part to midnight
  df.insert(0, "pd_symbol", sym) # add Symbol as 1st column after date
  new_columns = ['ema_5', 'ema_13', 'sma_50', 'sma_200', 'rsi_14', 'macd_sig_hist', 'dm_dp_adx', 'crs_50']      #  define the names of the new columns
  df_return = df.assign(**{col: np.nan for col in new_columns})   #  add the new columns with value NaN for each column across all rows

  logger.debug("converted df_return =")
  fn_df_print_first_last_rows(df_return, 3, 'ALL_COLS')
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
  logger.add(sys.stderr, level=LOGGING_LEVEL, colorize=True)  # sets the logging level
  
  curr_level = logger.level(LOGGING_LEVEL)     # get the current logging level
  logger.info("Current Logging level is : {} ", curr_level)  # Level(name='DEBUG', no=10, color='<blue><bold>', icon='🐞')
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

def fn_disable_session_for_ssl() -> requests.Session:
  unsafe_session = requests.session()
  unsafe_session.verify = False
  logger.warning("Session is disabled for SSL verification")
  return unsafe_session


def fn_enable_session_for_ssl_certifi() -> requests.Session:
  session = requests.session()
  session.verify = certifi.where()    # ensures that requests uses the certifi-managed CA bundle for SSL verification
  logger.warning("Session is now enabled to use SSL certificate from certifi ...")
  return session