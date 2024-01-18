from sqlalchemy import create_engine
import psycopg2
from config import DB_INFO, DEBUG_MODE
import pandas as pd


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




