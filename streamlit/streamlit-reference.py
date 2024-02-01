
# https://docs.streamlit.io/library/advanced-features/theming  (bg, fg colours, fonts)
# https://docs.streamlit.io/library/advanced-features/caching   (for caching)

import streamlit as st
# All SQLConnections in Streamlit use SQLAlchemy
import sqlalchemy as db


# --------------------------------------------------------------------------------

'''
**** i think this section needs to go into sqlalchemy directory ******

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



# --------------------------------------------------------------------------------
# Layouts and Containers  - https://docs.streamlit.io/library/api-reference/layout

# --  SIDEBAR --
# Each element that's passed to st.sidebar is pinned to the left, allowing users to focus on the content in your app.
# Object notation
# Text Sidebar
symbol = st.sidebar.text_input("Widget-01", value='AAPL', max_chars=5)    # Text input box named Widget-01 which will take max 5 chars
# Selectbox (dropdown) Sidebar
chosen_sb_option = st.sidebar.selectbox(           # Drop-down named Widget-02 with 3 selectable options
    "Widget-02",
    ("Email", "Home phone", "Mobile phone"),
    key='chosen_sb_option_key',                    # this needs to be unique else "streamlit.errors.DuplicateWidgetID: There are multiple widgets with the same `key=..."
    index=None                                     # on start up, this will make it select no option, whereas default is select 1st item
)
st.write('You selected:', chosen_sb_option)
# Radio button Sidebar
chose_rd_option = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

# ....remaining to do .....

# --------------------------------------------------------------------------------
# Load a pandas dataframe into a static streamlit table
st.table(df)

# Load a pandas dataframe into an interactive streamlit table
st.dataframe(df, 100, 200)

# highlighting maximum values in each column
st.dataframe(df.style.highlight_max(axis=0))

# --------------------------------------------------------------------------------
# https://docs.streamlit.io/library/api-reference/widgets

# Text Input Box


# --------------------------------------------------------------------------------
# --- below worked when i ran on acloudguru aws VPS and was able to access via browser from my PC ---
#  sudo ufw allow 8000/tcp comment 'My Web Server Port'
#  streamlit run streamlit_1.py --server.port 8000
# but access can take time/be flaky. i saw that via IP:port it was not accessible during some times, but via fqdns and port it was ...
# --------------------------------------------------------------------------------






