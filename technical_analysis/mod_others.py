import pandas as pd
from loguru import logger


def fn_df_fl(df: pd.DataFrame)
  # find the first and last row of df and return them as a dataframe
  df_first_last = pd.concat([df.head(1), df.tail(1)])
  logger.debug("df with only first and last rows = {}", df_first_last)