import os
import sys
import platform
from datetime import datetime, timedelta
import time
from typing import Optional

import sqlalchemy as sa
import psycopg2 as psy
import pandas as pd
import numpy as np
import sqlalchemy as sa
from loguru import logger

import mod_others as m_oth

if platform.system() == "Windows":
  #logger.debug("mod_utils_db.py - Running on Windows")
  sys.path.append("H:\\git-projects\\python-code")
  sys.path.append("H:\\git-projects\\python-code\\streamlit_code")
elif platform.system() == "Linux":
  #logger.debug("mod_utils_db.py - Running on Linux")
  home_dir = os.environ.get("HOME")
  if home_dir:
    sys.path.append(os.path.join(home_dir, "git-projects/python-code"))
    sys.path.append(os.path.join(home_dir, "git-projects/python-code/pkg_common"))
#  sys.path.append("/home/cloud_user/git-projects/python-code/streamlit_code")
else:
  print("Operating system not recognized")


#from technical_analysis.config import DB_INFO, DEBUG_MODE
#from streamlit_code.config import DB_INFO, DEBUG_MODE
#from config import DB_INFO, DEBUG_MODE
from technical_analysis import mod_technical_indicators as m_tin
#logger.debug(sys.path)
#import config

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


def fn_run_conn_sql_query(dbconn, sql_query, params=None):
    """
    Execute a SQL query on the provided database connection and return the result as a pandas DataFrame.

    Parameters:
    - dbconn: Database connection object.
    - sql_query: SQL query string to be executed.
    - params: Dictionary of query parameters for placeholder substitution.


    Returns:
    - DataFrame: The resulting data from the SQL query.
    
    TODO:
    - Handle cases where the query returns no output.
    """
    # Log the input SQL query for debugging purposes
    logger.info("Input sql_query = {}", sql_query)
    if params:
        logger.info("Query parameters = {}", params)
    # Execute the SQL query and store the result in a DataFrame
    df_output = pd.read_sql_query(sql_query, dbconn, params=params)
    
    # Log the first and last few rows of the DataFrame for inspection
    m_oth.fn_df_print_first_last_rows(df_output, 3, 'ALL_COLS')
 
    # Return the resulting DataFrame
    return df_output



def fn_run_conn_sqlalchemy_query(engine, sql_query, dct_params=None):
    """
    Execute a SQL query using SQLAlchemy and return results as a pandas DataFrame.
    
    Parameters:
      engine: SQLAlchemy engine object
      sql_query (str): SQL query with optional parameter placeholders
      dct_params (dict, optional): Dictionary of parameter values for query placeholders
    
    Returns:
      pandas.DataFrame: Query results as a DataFrame
    
    Example invocation 1:
      wildcard_value_1 = "%FA%"
      wildcard_value_2 = "%SB%"
      dct_params = {"param1": wildcard_value_1, "param2": wildcard_value_2}
      sql_query = "SELECT * FROM viw_instrument_in_us_top100_etfs_by_aum WHERE symbol LIKE :param1 OR symbol LIKE :param2;"
      df_symbols = m_udb.fn_run_conn_sqlalchemy_query(sa_engine, sql_query, dct_params)  
    Example invocation 2:
      dct_params = {"sector_nm": "Industrials", "indgrp_nm": "Capital Goods", "ind_nm": "Machinery"}
      sql_query = \"\"\"                           # commented as it is in docstring
        select * from tbl_gics_sector 
        where 
        sector_name = :sector_nm
        and industry_group_name = :indgrp_nm
        and industry_name = :ind_nm 
      \"\"\"    
      df_symbols = m_udb.fn_run_conn_sqlalchemy_query(sa_engine, sql_query, dct_params)

    TODO:
    - Handle cases where the query returns no output.
    """
    # Log the input SQL query for debugging purposes
    logger.debug("Input sql_query = {}", sql_query)
    if dct_params:
      logger.debug("Input sql query parameters = {}", dct_params)
        
    # Print the SQL query with the actual values substituted
    formatted_query = sql_query
    for key, value in dct_params.items():
      formatted_value = f"'{value}'" if isinstance(value, str) else str(value)
      formatted_query = formatted_query.replace(f":{key}", formatted_value)
    logger.info("Complete SQL Query with values = \n{}", formatted_query)

    # Create the SQLAlchemy text object (no parameters bound yet to this query)
    sql_query_text = sa.text(sql_query)

    with engine.connect() as connection:
      # Execute the query and pass parameters at execution time
      result = connection.execute(sql_query_text, dct_params)
      df_output = pd.DataFrame(result.fetchall(), columns=result.keys())    

    # Log the first and last few rows of the DataFrame for inspection
    m_oth.fn_df_print_first_last_rows(df_output, 3, 'ALL_COLS')

    # Return the resulting DataFrame
    return df_output



def fn_get_symbol_price_data_stats_from_database(dbconn: object, symbol: str) -> pd.DataFrame:
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

  Returns:
         pd_symbol       name exchange_code asset_type        oldest_rec_pd_time        latest_rec_pd_time  num_records  time_difference_in_days  days_since_latest  weekdays_between_oldest_and_latest
  0      TSLA  Tesla Inc        NASDAQ      STOCK 2022-01-03 00:00:00+00:00 2025-01-10 00:00:00+00:00          759                   1103.0               27.0                                 790
  """
  logger.debug("Received arguments : dbconn={} symbol={}", dbconn, symbol)

  sql_query = sa.text("SELECT * FROM viw_price_data_stats_by_symbol WHERE pd_symbol = :prm_symbol").bindparams(prm_symbol=symbol)
  logger.info("Looking up price data table stats from database for symbol {}. SQL Query=[{}]", symbol, sql_query)
  df_result = pd.read_sql_query(sql_query, dbconn)
  logger.info("DB table contains this data for {} :\n{}", symbol, df_result)

  return df_result


def fn_insert_symbol_price_data_into_db(dbconn, symbol, df, table_name, to_insert_indicator_values: bool):
  """Using the df provided, insert OHLC data into the table for this particular symbol

  NOTE: this will not check whether symbol exists, or if the data in the price data table exists for these days, it assumes all that has been done already.
  Args:
      dbconn (db connection object): SQLAlchemy db connection handle
      symbol (string): symbol for which we need the data inserted
      df (dataframe): dataframe containing olhc data for the symbol
      table_name (string): name of the table into which we need this data inserted
      to_insert_indicator_values (boolean): this will tell the function if the advanced indicator values also need to be computed AND inserted into the respective columns

  df format:
  pd_symbol                   pd_time   open   high    low  close  volume ema_5  ema_13  sma_50  sma_200  rsi_14   macd_sig_hist          dm_dp_adx  crs_50
50    VWRL.L 2024-01-23 00:00:00+00:00  93.65  94.02  93.44  93.88   25863   NaN     NaN     NaN      NaN   58.83  0.32;0.26;0.06   25.18;36.05;9.18  -0.057
51    VWRL.L 2024-01-24 00:00:00+00:00  94.37  94.51  94.01  94.37   19136   NaN     NaN     NaN      NaN   61.41   0.4;0.29;0.11  23.89;38.19;10.17  -0.039
52    VWRL.L 2024-01-25 00:00:00+00:00  94.12  94.57  94.03  94.57   30139   NaN     NaN     NaN      NaN   62.44  0.47;0.32;0.15  22.81;36.97;11.13  -0.049
68    VWRL.L 2024-02-16 00:00:00+00:00  97.99  98.35  97.62  97.98   44746   NaN     NaN     NaN      NaN   68.75   1.12;1.0;0.13  13.68;43.25;38.43     NaN
69    VWRL.L 2024-02-19 00:00:00+00:00  97.48  97.95  97.30  97.84   59012   NaN     NaN     NaN      NaN   67.39  1.14;1.03;0.11  15.33;41.11;38.95     NaN
70    VWRL.L 2024-02-20 00:00:00+00:00  97.57  97.75  96.74  96.91  425346   NaN     NaN     NaN      NaN   58.99  1.06;1.03;0.03  18.15;37.86;38.68     NaN

  """

  logger.debug("---------- fn_insert_symbol_price_data_into_db ---- STARTED ----------")

  logger.log("MYNOTICE", "START: LOG-TAG-001 : Inserting downloaded price data into table for {}", symbol)
  m_oth.fn_inspect_caller_functions()
  logger.debug("Received arguments : dbconn={} symbol={} tbl_name={} to_insert_indicator_values={} df={} rows and columns", dbconn, symbol, table_name, to_insert_indicator_values, df.shape)
  m_oth.fn_df_print_first_last_rows(df, 3, 'ALL_COLS')
  bch_symbol = "SPY"
  ##m_yfn.fn_sync_price_data_in_table_for_symbol("YFINANCE",  dbconn, bch_symbol)
  
  # if symbol == bch_symbol:
  #   #TODO: need to handle this properly
  #   # syncing of the benchmark symbol price data needs to be done before this i think as otherwise it will cause a recursive loop
  #   logger.warning("This is the same symbol as the benchmark symbol. Skipping insert of price data into the database")
  #   return
  if to_insert_indicator_values:
    # to compute the indicator values, we need to check if there is a minimum of 50 records of historical data from the table
    # which is older than the oldest record in the current df that is going to be inserted
    NUM_OLDER_RECS = 75   # approx 50 trading days

    if not df.empty:
      dt_df_first_date = df.iloc[0]["pd_time"]
      dt_df_last_date = df.iloc[-1]["pd_time"]
    else:
      logger.error("DataFrame is empty. No data to process.")
    # Handle the empty DataFrame case, e.g., return or raise an exception

    dt_50periods_prior_to_first_date  = dt_df_first_date - timedelta(days=NUM_OLDER_RECS)
    logger.debug("For the df passed as argument for {} : dt_df_first_date = {}, dt_df_last_date = {}, dt_50periods_prior_to_first_date = {}", 
                  symbol, dt_df_first_date, dt_df_last_date, dt_50periods_prior_to_first_date)
    
    logger.info("We now need to get the previous 50 days data from the table so that we can calculate indicators on the latest downloaded data")
    df_prev_50periods = fn_get_table_data_for_symbol(dbconn, symbol, dt_50periods_prior_to_first_date, dt_df_first_date)

    
    # TODO: need to check if benchmark symbol has the required amount of data
    logger.info("We also need to get the exact same amount of data for the benchmark symbol {} so that we can compute the indicators (mainly the CRS)", bch_symbol)
    df_bch_sym = fn_get_table_data_for_symbol(dbconn, bch_symbol, dt_50periods_prior_to_first_date, dt_df_last_date)

    df_prev_50periods["source"] = "older-data"
    df["source"] = "newer-data"
    df_combined = pd.concat([df_prev_50periods, df])
    # Reset the index, it will have a new index starting from 0
    df_combined = df_combined.reset_index(drop=True)
    logger.debug("----COMBINED-----")
    m_oth.fn_df_print_first_last_rows(df_combined, 3, 'ALL_COLS')

    #df_combined = m_tin.fn_relative_strength_indicator(df_combined)
    #df_combined = m_tin.fn_macd_indicator(df_combined, "macd_sig_hist")
    #df_combined = m_tin.fn_adx_indicator(df_combined, "dm_dp_adx")
    #df_combined = m_tin.fn_comparative_relative_strength_CRS_indicator(bch_symbol, df_bch_sym, symbol, df_combined, "crs_50")
    df_combined = m_tin.fn_compute_all_required_indicators(bch_symbol, df_bch_sym, symbol, df_combined)
    logger.debug("---7000--------------", df_combined)

    # extract back from the combined df only the rows that were in df
    df = df_combined[df_combined["source"] == "newer-data"]
    df = df.drop(columns=["source"])
    logger.debug("----COMPUTED INDICATORS AND df NOW UPDATED WITH THE VALUES -----")
    m_oth.fn_df_print_first_last_rows(df,  3, 'ALL_COLS')

  logger.log("MYNOTICE", "Now inserting the new data (above df) using SQLAlchemy function df.to_sql() for {} into DB table {} ...", symbol, table_name)
  logger.log("MYNOTICE", "using first_and_last_date = {}", m_oth.fn_df_get_first_last_dates(df))
  
  tm_before_insert = time.time()
  # Insert the DataFrame into the specified table
  # index=False to avoid saving the DataFrame index as a separate column in the table
  df.to_sql(name=table_name, con=dbconn, if_exists="append", index=False)
  tm_after_insert = time.time()
  logger.debug("---- AFTER INSERT df.to_sql() ----------")
  tm_taken_for_insertion_secs = tm_after_insert - tm_before_insert 
  tm_taken_for_insertion_secs  = "{:.3f}".format(tm_taken_for_insertion_secs)
  logger.debug("{} rows inserted into table {} for symbol {}", df.shape[0], table_name, symbol)
  logger.debug("DB insert completed in {} seconds", tm_taken_for_insertion_secs)
  logger.trace("Exiting function fn_insert_symbol_price_data_into_db() ...")
  m_oth.fn_df_print_first_last_rows(df, 3, 'ALL_COLS')

  logger.log("MYNOTICE", "END: LOG-TAG-001 : Completed inserting downloaded price data into table for {}, took {} seconds to complete", symbol, tm_taken_for_insertion_secs)
  logger.debug("---------- fn_insert_symbol_price_data_into_db ---- COMPLETED ----------")
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
    sql_query = sa.text(
        """
      SELECT 1
      FROM tbl_price_data_1day
      WHERE pd_symbol = :symbol AND pd_time = :time
  """
    )

    result = dbconn.execute(sql_query, symbol=pd_symbol, time=pd_time)
    return result.fetchone() is not None



def fn_check_symbol_exists_in_instrument_table(sa_engine, symbol):
    """
    Check if a symbol exists in the tbl_instrument table.

    Parameters:
    - engine: SQLAlchemy engine object
    - symbol: The symbol to check for existence

    Returns:
    - bool: True if the symbol exists in the table, False otherwise
    """
    sql_query = sa.text("SELECT * FROM tbl_instrument WHERE symbol = :symbol")
    with sa_engine.connect() as connection:
      result = connection.execute(sql_query, {"symbol": symbol})
      rows = result.fetchall()  # Fetch all rows as a list
      count = len(rows)         # Count the number of rows
      if count > 0:
        logger.debug("query result data : {}", rows)
        return True
      else:
        return False



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
    logger.debug("------------------ fn_get_table_data_for_symbol ------- START ---------------")
    logger.debug("Received arguments : dbconn={} symbol={} start_date={} end_date={}", dbconn, symbol, start_date, end_date)

    # NOTE - it took me a fair bit of time with chatgpt etc to build this SQLAlchemy syntax specific query
    conditions = []
    if start_date:
      conditions.append(sa.text("pd_time >= :start_date"))
    if end_date:
      conditions.append(sa.text("pd_time <= :end_date"))
    conditions.append(sa.text("pd_symbol = :param"))
    where_clause = " AND ".join([str(condition) for condition in conditions])

    sql_query = sa.text(f"SELECT * FROM tbl_price_data_1day WHERE {where_clause}")
    dct_params = {"start_date": start_date, "end_date": end_date, "param": symbol}
    logger.info("Fetching price data from Database for {} using below constructed sql query :", symbol)
    logger.info("query=[{}] and dct_params=[{}]", sql_query, dct_params)

    # Execute the SQLAlchemy query and fetch data
    df_ohlcv_symbol = pd.read_sql_query(sql_query, dbconn, params=dct_params)

    logger.debug("End of function -    Returning df =")
    m_oth.fn_df_print_first_last_rows(df_ohlcv_symbol,3,'IND_COLS')

    logger.debug("----------------- fn_get_table_data_for_symbol ------- END -------------")
    return df_ohlcv_symbol


# --------------------------------------------------------------------------------

'''
**** i think this section needs to go into sqlalchemy section ?? ******

engine = db.create_engine('sqlite:///census.sqlite')
conn = engine.connect()
metadata = db.MetaData()
#census= db.Table('census', metadata, autoload=True, autoload_with=engine) #Table object

This code is written in Python and it is using SQLAlchemy library to interact with a database.
•  The first line creates a MetaData object which is used to store information about the database schema.
•  The second line creates a Table object named census by passing the table name census, the metadata object, and two optional arguments autoload=True and autoload_with=engine.
•  The autoload=True argument tells SQLAlchemy to automatically load the table schema from the database, and autoload_with=engine specifies the database connection to use.
•  Overall, this code is extracting metadata and creating a Table object for the census table in the database.

#engine = db.create_engine('dialect+driver://user:pass@host:port/db')
census = db.Table('census', metadata, autoload=True, autoload_with=engine)
# Print the column names
print(census.columns.keys())
  The census variable is assumed to be a Pandas DataFrame.
•  The columns attribute of a DataFrame returns a pandas.core.indexes.base.Index object that contains the column labels of the DataFrame.
•  The keys() method is then called on this Index object to return a list of the column labels as strings.
•  Finally, the print() function is used to output this list of column labels to the console.
['state', 'sex', 'age', 'pop2000', 'pop2008']
# Print full table metadata
print(repr(metadata.tables['census']))
•  The code is accessing the census table by using its name as the key in the tables dictionary.
•  The repr() function is used to return a string representation of the census table object.

Table('census', MetaData(bind=None), Column('state', VARCHAR(length=30), table=<census>), Column('sex', VARCHAR(length=1), table=<census>), Column('age', INTEGER(), table=<census>), Column('pop2000', INTEGER(), table=<census>), Column('pop2008', INTEGER(), table=<census>), schema=None)

#Equivalent to 'SELECT * FROM census'
query = db.select([census]) 
print(query)

results = conn.execute(query)

ResultSet = results.fetchall()
•  The output.fetchall() method retrieves all the rows of the query result as a list of tuples.

ResultSet[:3]

[('Illinois', 'M', 0, 89600, 95012),
 ('Illinois', 'M', 1, 88445, 91829),
 ('Illinois', 'M', 2, 88729, 89547)]

#Convert to dataframe
df = pd.DataFrame(ResultSet)
df.columns = ResultSet[0].keys()
•  The code sets the column names of the DataFrame to be the keys of the first dictionary in the results list.
•  This assumes that all dictionaries in the list have the same keys.

# Write csv file data into database table
df = pd.read_csv('Stock Exchange Data.csv')
df.to_sql(con=engine, name="Stock_price", if_exists='replace', index=False)
This code reads a CSV file named "Stock Exchange Data.csv" using the pandas library's read_csv() function and stores it in a pandas DataFrame object named df.
•  Then, it uses the to_sql() method to write the contents of the DataFrame to a SQL database table named "Stock_price" using the SQLAlchemy library's engine object.
•  The if_exists parameter is set to 'replace', which means that if the table already exists, it will be dropped and recreated with the new data.
•  The index parameter is set to False, which means that the DataFrame's index will not be included in the SQL table.
'''
