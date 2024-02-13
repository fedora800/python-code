import sys
import pandas as pd
from loguru import logger


def fn_df_get_first_last(df: pd.DataFrame, num_rows: int):
  # take the first n and last n rows of df and return them as a dataframe

  df_first_last = pd.concat([df.head(num_rows), df.tail(num_rows)])
  logger.debug("df with only first and last [{}] rows = \n{}", num_rows, df_first_last)


def fn_modify_dataframe_per_our_requirements(sym: str, df: pd.DataFrame):

  df.reset_index(inplace=True)  # reset the Date index and make it into a column by itself. will be the 1st column
  df.insert(0, "Symbol", sym) # add Symbol as 2nd column after date
  #df_prices['Symbol'] = sym   # but this will add as the last column of df
  df.drop(columns=['Adj Close'], inplace=True)
  #print("modified df so as to be able to insert into postgres table : \n", df_prices.head(1))


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

