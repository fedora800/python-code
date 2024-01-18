from sqlalchemy import create_engine
import pandas as pd

def run_sql_query(db_uri, sql_query):
    """
    Connect to a database using SQLAlchemy and execute an SQL query.

    Parameters:
    - db_uri (str): PostgreSQL database URI.
    - query (str): SQL query to execute.
    
    Returns:
    pd.DataFrame: Result of the SQL query as a DataFrame.
    """
    # Create a SQLAlchemy engine
    engine = create_engine(db_uri)

    # Execute the SQL query and fetch the results into a DataFrame
    with engine.connect() as connection:
        result_df = pd.read_sql(sql_query, connection)

    return result_df

