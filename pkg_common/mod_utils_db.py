import sys
import platform
from datetime import datetime, timedelta
from typing import Optional
import time

import sqlalchemy as sa

import psycopg2 as psy
import pandas as pd
from sqlalchemy import text
from loguru import logger

import mod_yfinance as m_yfn



if platform.system() == "Windows":
  logger.debug("mod_utils_db.py - Running on Windows")
  sys.path.append("H:\\git-projects\\python-code")
  sys.path.append("H:\\git-projects\\python-code\\streamlit_code")
elif platform.system() == "Linux":
  logger.debug("mod_utils_db.py - Running on Linux")
  sys.path.append("~/git-projects/python-code")
  sys.path.append("~/git-projects/python-code/streamlit_code")
  sys.path.append("/home/cloud_user/git-projects/python-code/streamlit_code")
else:
  print("Operating system not recognized")


#from technical_analysis.config import DB_INFO, DEBUG_MODE
from streamlit_code.config import DB_INFO, DEBUG_MODE
#from config import DB_INFO, DEBUG_MODE
logger.debug(sys.path)
#import config
import mod_others as m_oth

def fn_create_database_engine_sqlalchemy(db_uri: str)-> sa.Engine:
  """
  Create a SQLAlchemy Engine for connecting to a database.

  Parameters:
  - db_uri (str): Database URI of the format dialect+driver://username:password@host:port/database.

  Returns:
  - Engine: SQLAlchemy Engine object providing a source of connectivity to a database.

  Example:
  >>> db_uri = "postgresql://user:password@localhost:5432/mydatabase"
  >>> engine = create_database_engine(db_uri)
  >>> # Use the engine for database operations
  """
  # Create a SQLAlchemy engine
  engine = sa.create_engine(db_uri)  # db_uri should be of format -  dialect+driver://username:password@host:port/database

  return engine


# connect to the database
def connect_to_db_using_psycopg2():
    # Set up a connection string
    # sslmode = 'require'  # or 'prefer' if you don't want to use SSL encryption
    # conn_str = f"postgresql://{username}:{password}@{host}:{port}/{database}?sslmode={sslmode}"
    # connect_str = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    connect_str = f"postgresql://{DB_INFO['USERNAME']}:{DB_INFO['PASSWORD']}@{DB_INFO['HOSTNAME']}:{DB_INFO['PORT']}/{DB_INFO['DATABASE']}"
    # print('DB conn_str = ', connect_str)

    print(
        f"Debug mode is enabled. Connection String: {connect_str}"
    ) if DEBUG_MODE else None

    try:
        # Connect to an existing database
        #      connection = psycopg2.connect(user="postgres",
        #                                    password="pynative@#29",
        #                                    host="127.0.0.1",
        #                                    port="5432",
        #                                    database="postgres_db")
        connection = psy.connect(connect_str)

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information -")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        print("Checking PostgreSQL server version using SQL query -")
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print(record, "\n")

    except Exception as e:
        print(f"An error occurred: {e}")

    #    finally:
    #      if (connection):
    #          cursor.close()
    #          connection.close()
    #          print("PostgreSQL connection is closed")

    cursor.close()

    # return handle to an opened db connection
    # print(type(connection), "---", connection)
    return connection


def run_conn_sql_query(dbconn, sql_query):
    """
    input is the db connection and the sql_query. it will run against the database and return output in a pandas df.
    TODO - what about no output ???
    """
    print("Input sql_query = ", sql_query)

    df_output = pd.read_sql_query(sql_query, dbconn)
    m_oth.fn_df_get_first_last(df_output)
 
    return df_output


def fn_get_symbol_price_data_stats_from_database(dbconn, symbol):
  """
  Looks up in the database for details about how much price data information we have on this particular symbol

  Parameters:
  - parameter1 (db connection object): db connection object
  - parameter2 (string): symbol

  Returns:
  type: df [pd_symbol, oldest_rec_pd_time, latest_rec_pd_time, num_records]

  Raises:
  SpecificException: Description of when this exception is raised.
  AnotherException: Description of another possible exception.
  """
  logger.debug("Received arguments : dbconn={} symbol={}", dbconn, symbol)

  sql_query = sa.text("SELECT * FROM viw_price_data_stats_by_symbol WHERE pd_symbol = :prm_symbol").bindparams(prm_symbol=symbol)
  logger.info("Now fetching price data table stats from database for symbol {} using query {}", symbol, sql_query)
  df_result = pd.read_sql_query(sql_query, dbconn)
  logger.debug("Returning results df = \n{}", df_result)

  return df_result


def fn_insert_symbol_price_data_into_db(dbconn, symbol, df, table_name, to_insert_indicator_values: bool):
  """Using the df provided, insert OHLC data into the table for this particular symbol

  Args:
      dbconn (db connection object): SQLAlchemy db connection handle
      symbol (string): symbol for which we need the data inserted
      df (dataframe): dataframe containing olhc data for the symbol
      table_name (string): name of the table into which we need this data inserted
      to_insert_indicator_values (boolean): this will tell the function if the advanced indicator values also need to be computed AND inserted into the respective columns

  df format:
      symbol       date   open   high    low  close  volume
  0   VWRL.L 2024-01-17  92.39  92.48  92.00  92.19   30614
  1   VWRL.L 2024-01-18  92.07  92.71  92.04  92.58   23364
  19  VWRL.L 2024-02-13  97.13  97.36  96.00  96.33   56403
  20  VWRL.L 2024-02-14  96.58  97.27  96.36  97.00   22437
  """

  logger.debug( "Received arguments : dbconn={} symbol={} tbl_name={} df=", dbconn, symbol, table_name)
  logger.debug(m_oth.fn_df_get_first_last(df, 2))

  if symbol != "SPY" and to_insert_indicator_values:
    # first sync the benchmark symbol price data
    # TODO: but that needs to be done before this as otherwise it will cause a recursive loop
    print("---------------------1010--------------")

    # to compute the indicator values, we need a minimum of 50 records of historical data 
    # which is older than the oldest record in the df
    dt_date_of_oldest_df_record = df.iloc[0]["date"]
    dt_50days_prior_date  = dt_date_of_oldest_df_record - timedelta(days=50)
    logger.debug("dt_date_of_oldest_df_record = {}, dt_50days_prior_date = {}", dt_date_of_oldest_df_record, dt_50days_prior_date)
    
    # TODO: here we just get all the data and then cut out, maybe we need to get only the 50 days reqd
    df_prev = fn_get_table_data_for_symbol(dbconn, symbol, dt_50days_prior_date, dt_date_of_oldest_df_record)
    


  # prepare the df for inserting into the table
  column_mapping = {
      "symbol": "pd_symbol",
      "date": "pd_time",
      "open": "open",
      "high": "high",
      "low": "low",
      "Close": "close",
      "volume": "volume",
      "ema_5": None,
      "ema_13": None,
      "sma_50": None,
      "sma_200": None,
      "rsi_14": None,
  }
  if column_mapping:
      df = df.rename(columns=column_mapping)
  
  tm_before_insert = time.time()
  # Insert the DataFrame into the specified table
  # index=False to avoid saving the DataFrame index as a separate column in the table
  df.to_sql(name=table_name, con=dbconn, if_exists="append", index=False)
  tm_after_insert = time.time()
  tm_taken_for_insertion_secs = tm_after_insert - tm_before_insert 
  tm_taken_for_insertion_secs  = "{:.3f}".format(tm_taken_for_insertion_secs)
  logger.info("DB insert completed in {} seconds - {} rows inserted into table {} for symbol {}", tm_taken_for_insertion_secs, df.shape[0], table_name, symbol)
  logger.trace("Exiting function fn_insert_symbol_price_data_into_db() ...")
  m_oth.fn_df_get_first_last(df, 2)
  return df
  

def get_symbol_input_check_against_db_using_psycopg2(dbconn):
    """
    user will input symbol. we will check in instrument table if it exists.
    if yes, we will return that entire row
    if not, we will say that symbol not found
    """

    text_input = "AAPL"
    if text_input:
        print("You entered Symbol : ", text_input)
    sql_query = "select * from tbl_instrument where symbol= '%s'" % text_input
    psy.run_sql_query(dbconn, sql_query)

    sql_query = (
        "select * from viw_price_data_stats_by_symbol where pd_symbol = '%s'"
        % text_input
    )
    psy.run_sql_query(dbconn, sql_query)


def record_exists(dbconn, pd_symbol, pd_time):
    # Check if a record with the given pd_symbol and pd_time already exists
    sql_query = text(
        """
      SELECT 1
      FROM tbl_price_data_1day
      WHERE pd_symbol = :symbol AND pd_time = :time
  """
    )

    result = dbconn.execute(sql_query, symbol=pd_symbol, time=pd_time)
    return result.fetchone() is not None



def fn_get_table_data_for_symbol(dbconn, symbol: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
    """
    Fetches data from tbl_price_data_1day for this symbol into a dataframe
    Assumptions:
      Symbol is a valid symbol on the data venue.
      Symbol record exists in tbl_instrumeent.
      Up to date price data exists in tbl_price_data_1day

    Returns:
      dataframe
    """

    logger.debug("Received arguments : dbconn={} symbol={} start_date={} end_date={}", dbconn, symbol, start_date, end_date)

    # # Base SQL query
    # sql_query = text("""SELECT * FROM tbl_price_data_1day WHERE pd_symbol = :symbol""").bindparams(symbol=symbol)
    # conditions = []

    # # Add conditions for start_date and end_date if provided
    # if start_date:
    #   conditions.append(text("pd_time >= :start_date").bindparams(start_date=start_date))
    # if end_date:
    #   conditions.append(text("pd_time <= :end_date").bindparams(end_date=end_date))

    # if conditions:
    #   sql_query = sa.and_(sql_query, *conditions)

    conditions = []

    if start_date:
        conditions.append(text("pd_time >= :start_date"))
    if end_date:
        conditions.append(text("pd_time <= :end_date"))

    conditions.append(text("pd_symbol = :param"))

    where_clause = " AND ".join([str(condition) for condition in conditions])

    sql_query = text(f"SELECT * FROM tbl_price_data_1day WHERE {where_clause}")
    
    print("----sql_query=", sql_query)
    params = {"start_date": start_date, "end_date": end_date, "param": symbol}


    logger.info("To get the price data for {} - evaluated sql_query = {}", symbol, sql_query)

    # Execute the query and fetch data
    df_ohlcv_symbol = pd.read_sql_query(sql_query, dbconn, params=params)

    logger.debug("Returning df = \n{}", df_ohlcv_symbol.head(2))

    return df_ohlcv_symbol

    
    