from sqlalchemy import create_engine
import psycopg2
from loguru import logger
from config import DB_INFO, DEBUG_MODE
import pandas as pd
from sqlalchemy import text


def connect_to_db_using_sqlalchemy(db_uri):
    """
    Connect to a database using SQLAlchemy and execute an SQL query.

    Parameters:
    - db_uri (str): PostgreSQL database URI.
    
    Returns:
    --pd.DataFrame: Result of the SQL query as a DataFrame.
    """
    # Create a SQLAlchemy engine
    engine = create_engine(db_uri)             # db_uri should be of format -  dialect+driver://username:password@host:port/database

    return engine



# connect to the database
def connect_to_db_using_psycopg2():
    # Set up a connection string
    #sslmode = 'require'  # or 'prefer' if you don't want to use SSL encryption
    #conn_str = f"postgresql://{username}:{password}@{host}:{port}/{database}?sslmode={sslmode}"
    #connect_str = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    connect_str = f"postgresql://{DB_INFO['USERNAME']}:{DB_INFO['PASSWORD']}@{DB_INFO['HOSTNAME']}:{DB_INFO['PORT']}/{DB_INFO['DATABASE']}"
    #print('DB conn_str = ', connect_str)

    print(f"Debug mode is enabled. Connection String: {connect_str}") if DEBUG_MODE else None

    try:
      # Connect to an existing database
#      connection = psycopg2.connect(user="postgres",
#                                    password="pynative@#29",
#                                    host="127.0.0.1",
#                                    port="5432",
#                                    database="postgres_db")
      connection = psycopg2.connect(connect_str)
  
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
  
    except (Exception, Error) as error:
      print("Error while connecting to PostgreSQL", error)
    
#    finally:
#      if (connection):
#          cursor.close()
#          connection.close()
#          print("PostgreSQL connection is closed")

    cursor.close()

    # return handle to an opened db connection
    #print(type(connection), "---", connection)
    return connection


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
 
    sql_query = text("SELECT * FROM viw_price_data_stats_by_symbol WHERE pd_symbol = :prm_symbol"
                    ).bindparams(prm_symbol=symbol)
    logger.info("Now fetching price data table stats from database for symbol {}", symbol)
    logger.debug("symbol chosen = {} | sql_query = {}", symbol, sql_query)
    df_result = pd.read_sql_query(sql_query, dbconn)
    logger.debug("Returning results df = {}", df_result)

    return df_result


def insert_symbol_price_data_stats_from_database(dbconn, symbol, df, table_name):

    '''
    70                          Open        High        Low         Close       Adj Close    Volume
    71   Date       2023-02-15  176.210007  178.820007  175.000000  177.419998  176.321732   815900
    '''

    print('---- here 666 ---')
    logger.debug("INSERT DATA IN TABLE - dbconn={} symbol={} df={} tbl_name={}", dbconn, symbol, df.tail(2), table_name)
    # prepare the df for inserting into the table
    df.reset_index(inplace=True)   # reset the Date index and make it into a column by itself. will be the 1st column
    df.insert(0, "Symbol", symbol) # add Symbol as 2nd column after date
    df.drop(columns=['Adj Close'], inplace=True)
    column_mapping = {
        'Symbol'   : 'pd_symbol',
        'Date'     : 'pd_time',
        'Open'     : 'open',
        'High'     : 'high',
        'Low'      : 'low',
        'Close'    : 'close',
        'Volume'   : 'volume',
        'ema_5'    : None,
        'ema_13'   : None,
        'sma_50'   : None,
        'sma_200'  : None,
        'rsi_14'   : None
    }
    if column_mapping:
        df = df.rename(columns=column_mapping)
    logger.debug("df before inserting into table {} = {} {}", table_name, df.head(1), df.tail(1))
    # Insert the DataFrame into the specified table
    # index=False to avoid saving the DataFrame index as a separate column in the table
    df.to_sql(name=table_name, con=dbconn, if_exists='append', index=False)

