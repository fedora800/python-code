import psycopg2
from psycopg2 import Error
import streamlit as st
import pandas as pd
# UserWarning: pandas only supports SQLAlchemy connectable (engine/connection) or database string URI or sqlite3 DBAPI2 connection. Other DBAPI2 objects are not tested. Please consider using SQLAlchemy.
import plotly.graph_objects as gobj


# connect to the database
def connect_db():
    # Set up a connection string
    username = 'postgres'
    password = 'postgres#123'
    host = 'localhost'
    database = 'dbs_invest'
    port = '5432'
    #sslmode = 'require'  # or 'prefer' if you don't want to use SSL encryption
    #conn_str = f"postgresql://{username}:{password}@{host}:{port}/{database}?sslmode={sslmode}"
    connect_str = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    #print('DB conn_str = ', connect_str)

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


def run_sql_query(db_conn, sql_query):
  """
  input is the db connection and the sql_query. it will run against the database and return output in a pandas df.
  TODO - what about no output ???
  """
  print("Input sql_query = ", sql_query)

  df_output = pd.read_sql_query(sql_query, db_conn)
  print('Output df = ', df_output)
  generate_table_plot(df_output)

  return df_output



def streamlit_sidebar_selectbox_symbol_group(dbconn):
  """
  this the top-left 1st selectbox on the sidebarinput 
  user will select the group of symbols he wants to start on (eg US ETFs, UK ETFs, US S&P500 constituents etc)
  TODO - what about no output ???
  """

  dct_options = {
    "scan_name": [
       "US S&P500 constituents",
       "US ETFs",
       "UK ETFs (incomplete)"
    ],
    "symlist_sqlquery": [
       "select * from viw_instrument_us_sp500_constituents where symbol like 'O%'",
       "select symbol from viw_instrument_uk_equities where symbol like 'JP%'",
       "select * from viw_instrument_uk_equities"
    ]
  }

  #load data into a DataFrame object:
  df_select_options = pd.DataFrame(dct_options)
  sg_chosen_option = st.sidebar.selectbox( 
    "symbolgroups",
    df_select_options,
    key='sg_chosen_option',
    index=None
  )
  st.write('symbolgroup sg_chosen_option : ', sg_chosen_option)
  print("streamlit_sidebar_selectbox_symbolgroup - sg_chosen_option = ", sg_chosen_option)


def get_symbol_input_check_against_db(dbconn):
  """
  user will input symbol. we will check in instrument table if it exists.
  if yes, we will return that entire row
  if not, we will say that symbol not found
  """

  # Take a text input for symbol from user 
  text_input = st.text_input(
      "Enter some text 👇"
#       label_visibility=st.session_state.visibility,
#       disabled=st.session_state.disabled,
#       placeholder=st.session_state.placeholder,
  )
  if text_input:
      print('You entered Symbol : ', text_input)
      st.write("You entered Symbol : ", text_input)
  sql_query = "select * from tbl_instrument where symbol= '%s'" % text_input
  run_sql_query(dbconn, sql_query)

  sql_query = "select * from viw_price_data_stats_by_symbol where pd_symbol = '%s'" % text_input
  run_sql_query(dbconn, sql_query)


def generate_chart_plot(df):

# this works
#  fig = gobj.Figure(data=[gobj.Candlestick(x=df['pd_time'], 
#                                       open=df['open'], 
#                                       high=df['high'], 
#                                       low=df['low'], 
#                                       close=df['close']
#                                      ),
#                        gobj.Scatter(x=df['pd_time'], y=df['sma_50'], line=dict(color='red', width=2))  # plots the moving average on top as a scatter plot
#                       ]
#                 )


 
  # Create a gobj.Candlestick object, assign these fields and then assign it to a variable named chart_data
  chart_data = gobj.Candlestick(x=df['pd_time'], open=df['open'], high=df['high'], low=df['low'], close=df['close'])

#  layout = go.Layout(
#      autosize=False,
#      width=1000,
#      height=1000,
#      xaxis=go.layout.XAxis(linecolor="black", linewidth=1, mirror=True),
#      yaxis=go.layout.YAxis(linecolor="black", linewidth=1, mirror=True),
#      margin=go.layout.Margin(l=50, r=50, b=100, t=100, pad=4),
#  )
#  
#  fig = go.Figure(data=data, layout=layout)

  # Now create a gobj.Figure called fig to display the data. Create this object passing in chart_data and assigning it to a variable named fig:
  fig = gobj.Figure(data=[chart_data])

  # To plot the moving average on top of this chart/figure, create a gobj.Scatter object, setting x with the same df time and y with the movavg df. 
  # we can also specify other settings like mode, colour, width etc
  # name value is what we will see as the the label/legend on the side of the chart, the sma line can have its own properties defined by a dict below
  # marker=dict(size=25, color=color_4, symbol=marker_list_2, line=dict(width=0.5))
  dct_textfont=dict(color="black", size=18, family="Times New Roman")
  trace_sma_50 = gobj.Scatter(x=df['pd_time'], y=df['sma_50'], mode='lines', name='50-SMA', textfont=dct_textfont, line=dict(color='blue', width=2))
  trace_sma_200 = gobj.Scatter(x=df['pd_time'], y=df['sma_200'], mode='lines', name='200-SMA', textfont=dct_textfont, line=dict(color='red', width=2))

  # To add the new scatter plot, call fig.add_trace and pass in the variable trace_sma
  fig.add_trace(trace_sma_50)
  fig.add_trace(trace_sma_200)

  fig.update_layout(xaxis_rangeslider_visible=False)    # remove the bottom range slider

  dct_y_axis=dict(
    title_text="Y-axis Title for the Symbol Chart",    # this text will appear 180 turned on the left of the y axis
    titlefont=dict(size=30),                           # font size for title_text
  #  tickvals=[100, 200, 300, 400],                     # these will be fixed horizontal lines on the chart at the defined values
  #  ticktext=["pricelevel 100", "pricelevel 200", "pricelevel 300 (getting expensive)", "pricelevel 400"],   # for the tickvals, these texts will appear on the left
  #  tickmode="array",
  )
  dct_margin=dict(l=20, r=20, t=20, b=20)
  fig.update_layout(width=1100, height=600, 
    yaxis=dct_y_axis,
#    margin=dct_margin,
#    paper_bgcolor="LightSteelBlue"
  )
  #fig.update_layout(width=1100, height=900)            # default size of chart is small, increase it
  #fig.show()
  
  # Render plot using plotly_chart
  st.plotly_chart(fig,width=1100, height=600)         # make sure to increase this appropriately with the other objects

# plot the candlesticks


#  ----
#                 # Add the moving average
#                 gobj.Scatter(x=stock_data['moving3'].index,
#                            y=stock_data['moving3']),
#                 gobj.Scatter(x=stock_data['moving8'].index,
#                            y=stock_data['moving8'])
#                 ])
# 
# # Mask a default range slider
# fig.update_layout(xaxis_rangeslider_visible=False)
# 
# 
# # Set layout size
# fig.update_layout(
#     autosize=False,
#     width=600,
#     height=500,
#     legend=dict(
#         x=0.82,  # Adjust the legend's x position
#         y=0.98,  # Adjust the legend's y position
#         font=dict(size=12)  # Customize font size
#     )
# )
#  ---


def streamlit_sidebar_selectbox_symbol_only(dbconn, df):
  # Selectbox (dropdown) Sidebar
  xx_chosen_symbol = st.sidebar.selectbox(           # Drop-down named Widget-02 with 3 selectable options
    "Widget-02",
    df,
    key='xx_chosen_symbol',
    index=None
  )
  st.write('You selected:', xx_chosen_symbol)
  print("Symbol chosen from the select box = ", xx_chosen_symbol)

  sql_query = "select * from tbl_price_data_1day where pd_symbol= '%s'" % xx_chosen_symbol
  print("sql_query = ", sql_query)

  # Parameterized query
  # parameters are specified using the colon ( : )
  #sql_with_param = text("""select * from tbl_price_data_1day where pd_symbol= :in_symbol""")
  # dictionary containing parameter name value
  #input_param = {'in_symbol': 'TSLA'}

#   # -- using list ---
#   try:
#     cursor = db_conn.cursor()
#     cursor.execute(sql_query)
#     lst_records = cursor.fetchall()
# 
#     #print("Print each row and it's columns values")
#     #for row in lst_records:
#     #    print(row[0], " - ", row[1], " - ", row[2], "\n")
#     print('list first element=', lst_records[0])
#     print('list last element=', lst_records[-1]) 
# 
#   except (Exception, psycopg2.Error) as error:
#     print("Error while fetching data from PostgreSQL", error)
# 
#   finally:
#     cursor.close()
# 
#   print("Closing db connection ...")
#   db_conn.close()
#   # convert list to pandas dataframe
#   df_olhcv_symbol = pd.DataFrame(lst_records)
#   print(df_olhcv_symbol.shape)
#   print(df_olhcv_symbol.head(1))
#   print(df_olhcv_symbol.tail(1))
#   # i notice that the column names are missing
# 
#   # multiple ways of getting column names as list
#   print("\nThe column headers :")
#   print("Column headers from list(df.columns.values):", list(df_olhcv_symbol.columns.values))
#   print("Column headers from list(df):", list(df_olhcv_symbol))
#   print("Column headers from list(df.columns):", list(df_olhcv_symbol.columns))

  # --- using pandas functions ---
  df_ohlcv_symbol = pd.read_sql_query(sql_query, dbconn)
  print(df_ohlcv_symbol.tail(1))
  generate_chart_plot(df_ohlcv_symbol)

  data = {
    "scan_name": ["stocks below SMA50", "stocks_above_SMA50"],
    "scan_sqlquery": ["select * from viw_latest_price_data_by_symbol where close < sma_50", "select * from viw_latest_price_data_by_symbol where close > sma_50"]
  }

  #load data into a DataFrame object:
  df_scans = pd.DataFrame(data)
  chosen_sb2_option = st.selectbox( 
     "My Scans",
      df_scans,
      key='chosen_sb2_option'
  )
  st.write('The scan you selected:', chosen_sb2_option)
  #print("Symbol chosen from the select box = ", chosen_symbol)

  print("selection OPTION chosen = ", chosen_sb2_option)
  x11 = df_scans[df_scans["scan_name"]==chosen_sb2_option]["scan_sqlquery"].values[0]
  print("which maps to VALUE = ", x11)
  df_scan_output = pd.read_sql_query(x11, dbconn)
  print(df_scan_output.tail(3))
  generate_table_plot(df_scan_output)

#df[df['B']==3]['A'].item()
#Use df[df['B']==3]['A'].values[0] if you just want item itself without the brackets


def generate_table_plot(df):
  st.table(df)
  #st.dataframe(df, 100, 200)


def main():
  db_conn = connect_db() 
 # sql_query = "select symbol from tbl_instrument order by symbol"
  #sql_query = "select symbol from tbl_instrument where exchange_code not like 'UNL%' and symbol like 'T%' order by symbol"
  #sql_query = "select symbol from tbl_instrument where exchange_code not like 'UN%' order by symbol"
  sql_query = "select symbol, name from viw_instrument_uk_equities where symbol like 'V%' order by symbol"
  df_symbols = pd.read_sql_query(sql_query, db_conn)
  print(df_symbols.head(2))

  streamlit_sidebar_selectbox_symbol_group(db_conn)
  streamlit_sidebar_selectbox_symbol_only(db_conn, df_symbols)


# main
if __name__ == '__main__':


  APP_NAME = "Stock App!"
  
  print('--------------------------------------------------------------------------------')

  # Page Configuration
  st.set_page_config(
      page_title=APP_NAME,
      layout="wide",
      initial_sidebar_state="expanded",
  )
  
  # Add some markdown
  st.sidebar.markdown("Made with love using [Streamlit](https://streamlit.io/).")
  st.sidebar.markdown("# :chart_with_upwards_trend:")
  
  # Add app title
  st.sidebar.title(APP_NAME)

  main()

#  streamlit run streamlit_1.py --server.port 8000


