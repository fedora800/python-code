import pandas as pd
from loguru import logger


def fn_df_get_first_last(df: pd.DataFrame, num_rows: int):
  # take the first n and last n rows of df and return them as a dataframe

  df_first_last = pd.concat([df.head(num_rows), df.tail(num_rows)])
  logger.debug("df with only first and last [{}] rows = \n{}", num_rows, df_first_last)
