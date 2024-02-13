import sqlalchemy as sa
import psycopg2 as psy
from loguru import logger
#from technical_analysis.config import DB_INFO, DEBUG_MODE
from config import DB_INFO, DEBUG_MODE
import pandas as pd
from sqlalchemy import text
import mod_others as m_oth

def create_database_engine_sqlalchemy(db_uri: str)-> sa.Engine:
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


def get_symbol_price_data_stats_from_database(dbconn, symbol):
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
  logger.debug("Returning results df = {}", df_result)

  return df_result


def insert_symbol_price_data_into_db(dbconn, symbol, df, table_name):
  """Using the df provided, insert OHLC data into the table for this particular symbol

  Args:
      dbconn (db connection object): SQLAlchemy db connection handle
      symbol (string): symbol for which we need the data inserted
      df (dataframe): dataframe containing olhc data for the symbol
      table_name (string): name of the table into which we need this data inserted
  """

  """
  70                          Open        High        Low         Close       Adj Close    Volume
  71   Date       2023-02-15  176.210007  178.820007  175.000000  177.419998  176.321732   815900
  """
  df_head_foot = pd.concat([df.head(1), df.tail(1)])
  logger.debug(
      "Received arguments : dbconn={} symbol={} df={} tbl_name={}",
      dbconn,
      symbol,
      df_head_foot,
      table_name,
  )
  # prepare the df for inserting into the table
  df.reset_index(
      inplace=True
  )  # reset the Date index and make it into a column by itself. will be the 1st column
  df.insert(0, "Symbol", symbol)  # add Symbol as 2nd column after date
  df.drop(columns=["Adj Close"], inplace=True)
  column_mapping = {
      "Symbol": "pd_symbol",
      "Date": "pd_time",
      "Open": "open",
      "High": "high",
      "Low": "low",
      "Close": "close",
      "Volume": "volume",
      "ema_5": None,
      "ema_13": None,
      "sma_50": None,
      "sma_200": None,
      "rsi_14": None,
  }
  if column_mapping:
      df = df.rename(columns=column_mapping)
  df_head_foot = pd.concat([df.head(1), df.tail(1)])
  # Insert the DataFrame into the specified table
  # index=False to avoid saving the DataFrame index as a separate column in the table
  df.to_sql(name=table_name, con=dbconn, if_exists="append", index=False)
  logger.debug(
      "DB insert completed - {} into table {} = {}", symbol, table_name, df_head_foot
  )
  logger.info("TODO: print how much time it took to insert and well as how many rows ....")


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


def fn_get_table_data_for_symbol(dbconn, symbol):
  """
  Fetches data from tbl_price_data_1day for this symbol into a dataframe
  Assumptions:
    Symbol is a valid symbol on the data venue.
    Symbol record exists in tbl_instrumeent.
    Up to date price data exists in tbl_price_data_1day

  Returns:
    dataframe
  """

  logger.debug("Received arguments : dbconn={} symbol={}", dbconn, symbol)

  sql_query = text("""select * from tbl_price_data_1day where pd_symbol= :param""").bindparams(param=symbol)
  logger.info("To get the price data for {} - evaluated sql_query = {}", symbol, sql_query)
  df_ohlcv_symbol = pd.read_sql_query(sql_query, dbconn)
  df_head_foot = pd.concat([df_ohlcv_symbol.head(1), df_ohlcv_symbol.tail(1)])
  logger.debug("Returning df = \n{}", df_head_foot)
  return df_ohlcv_symbol



