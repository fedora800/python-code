import psycopg2
from psycopg2 import Error
from loguru import logger
import streamlit as st
import pandas as pd
import talib as ta

# UserWarning: pandas only supports SQLAlchemy connectable (engine/connection) or database string URI or sqlite3 DBAPI2 connection. Other DBAPI2 objects are not tested. Please consider using SQLAlchemy.
import plotly.graph_objects as gobj
from plotly.subplots import make_subplots
from utils import connect_to_db_using_sqlalchemy
from sqlalchemy import text


def run_conn_sql_query(dbconn, sql_query):
    """
    input is the db connection and the sql_query. it will run against the database and return output in a pandas df.
    TODO - what about no output ???
    """
    print("Input sql_query = ", sql_query)

    df_output = pd.read_sql_query(sql_query, dbconn)
    print("Output df = ", df_output)
    generate_table_plot(df_output)

    return df_output


def streamlit_sidebar_selectbox_symbol_group(dbconn):
    """
    this the top-left 1st selectbox on the sidebarinput
    user will select the group of symbols he wants to start on (eg US ETFs, UK ETFs, US S&P500 constituents etc)
    TODO - what about no output ???

    returns:
      a df with the output of the the sql_query results (symbols list) corresponding to what option we chose from the dropdown
    """

    dct_options = {
        "symbol_groups": ["US S&P500 constituents", "US ETFs", "UK ETFs (incomplete)"],
        "symbol_groups_sqlquery": [
            """select symbol, name from viw_instrument_us_sp500_constituents where symbol like '%RS%';""",
            """select symbol, name from viw_instrument_us_etfs where symbol like 'JP%';""",
            """select symbol, name from viw_instrument_uk_equities;""",
        ],
    }

    # load data into a df
    df_select_options = pd.DataFrame(dct_options)
    logger.debug(df_select_options)

    # Sidebar selectbox
    sg_chosen_option = st.sidebar.selectbox(
        "Symbol Groups Dropdown",  # Drop-down named Symbol Dropdown
        df_select_options["symbol_groups"],
        key="sg_chosen_option",
        index=None,
    )
    st.write("symbol_groups sg_chosen_option : ", sg_chosen_option)
    logger.info(
        "streamlit_sidebar_selectbox_symbolgroup - type={} sg_chosen_option={}",
        type(sg_chosen_option),
        sg_chosen_option,
    )

    # if user chooses from the symbol group dropdown, then run the sql query and return values into a dataframe
    if sg_chosen_option is None:
        # on startup, choice has been set up to none, so return empty df
        df_symbols = []
    else:
        sg_chosen_sql_query = df_select_options[
            df_select_options["symbol_groups"] == sg_chosen_option
        ]["symbol_groups_sqlquery"].iloc[0]
        logger.info(
            "streamlit_sidebar_selectbox_symbolgroup - CHOSEN SQL_QUERY = {}",
            sg_chosen_sql_query,
        )
        print("--1B--", sg_chosen_sql_query)
        sql_query = text(sg_chosen_sql_query)
        df_symbols = pd.read_sql_query(sql_query, dbconn)
        logger.debug(df_symbols)

    return df_symbols


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
        print("You entered Symbol : ", text_input)
        st.write("You entered Symbol : ", text_input)
    sql_query = "select * from tbl_instrument where symbol= '%s'" % text_input
    run_sql_query(dbconn, sql_query)

    sql_query = (
        "select * from viw_price_data_stats_by_symbol where pd_symbol = '%s'"
        % text_input
    )
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
    chart_data = gobj.Candlestick(
        x=df["pd_time"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
    )

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
    dct_textfont = dict(color="black", size=18, family="Times New Roman")
    trace_ema_13 = gobj.Scatter(
        x=df["pd_time"],
        y=df["ema_13"],
        mode="lines",
        name="13-EMA",
        textfont=dct_textfont,
        line=dict(color="purple", width=2),
    )
    trace_sma_50 = gobj.Scatter(
        x=df["pd_time"],
        y=df["sma_50"],
        mode="lines",
        name="50-SMA",
        textfont=dct_textfont,
        line=dict(color="blue", width=2),
    )
    trace_sma_200 = gobj.Scatter(
        x=df["pd_time"],
        y=df["sma_200"],
        mode="lines",
        name="200-SMA",
        textfont=dct_textfont,
        line=dict(color="red", width=2),
    )

    # To add the new scatter plot, call fig.add_trace and pass in the various trace objects
    fig.add_trace(trace_ema_13)
    fig.add_trace(trace_sma_50)
    fig.add_trace(trace_sma_200)

    # Do not show OHLC's rangeslider sub plot
    fig.update_layout(xaxis_rangeslider_visible=False)

    dct_y_axis = dict(
        title_text="Y-axis Title for the Symbol Chart",  # this text will appear 180 turned on the left of the y axis
        titlefont=dict(size=30),  # font size for title_text
        #  tickvals=[100, 200, 300, 400],                     # these will be fixed horizontal lines on the chart at the defined values
        #  ticktext=["pricelevel 100", "pricelevel 200", "pricelevel 300 (getting expensive)", "pricelevel 400"],   # for the tickvals, these texts will appear on the left
        #  tickmode="array",
    )
    dct_margin = dict(l=20, r=20, t=20, b=20)
    fig.update_layout(
        width=1100,
        height=600,
        yaxis=dct_y_axis,
        #    margin=dct_margin,
        #    paper_bgcolor="LightSteelBlue"
    )
    # fig.update_layout(width=1100, height=900)            # default size of chart is small, increase it
    # fig.show()

    # Render plot using plotly_chart
    st.plotly_chart(
        fig, width=1100, height=600
    )  # make sure to increase this appropriately with the other objects


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


def generate_chart_plot_2(df):
    """
    https://stackoverflow.com/questions/64689342/plotly-how-to-add-volume-to-a-candlestick-chart
    https://plotly.com/python/subplots/
    https://plotly.com/python/mixed-subplots/
    https://plotly.com/python/table-subplots/
    """

    # Create subplots with specific settings
    #
    fig = make_subplots(
        rows=5,  # 5 means each plot below the other plot vertically
        cols=1,  # just 1, but 2 would mean one plot besides the other horizontally
        shared_xaxes=True,  # Share axes among subplots in the same column
        vertical_spacing=0.03,  # Space between subplot rows in normalized plot coordinates. Must be a float between 0 and 1
        subplot_titles=(
            "OHLC",
            "Volume",  # Title of each subplot need mentioning as a list in row-major ordering.
            "RSI",
            "MACD",
            "ADX",
        ),
        # row_width=[0.1, 0.1, 0.1, 0.1, 0.6] # the relative HEIGHTS for each row of subplots, should total 1.0
        row_width=[
            0.1,
            0.1,
            0.1,
            0.1,
            0.6
        ]  # the relative HEIGHTS for each row of subplots, should total 1.0
        # NOTE - they seem to be in reverse, ie biggest 0.6 is the top-most
    )

    dct_textfont = dict(color="black", size=18, family="Times New Roman")

    # --- subplot 1 on row 1 and column 1  (OHLC candlestick chart with 3 indicators) ---
    # Prepare subplot with a gobj.Candlestick object
    trace_subplot_row_1 = gobj.Candlestick(
        x=df["pd_time"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
    )

    # To plot the moving average on top of this chart/figure, create a gobj.Scatter object, setting x with the same df time and y with the movavg df.
    # we can also specify other settings like mode, colour, width etc
    # name value is what we will see as the the label/legend on the side of the chart, the sma line can have its own properties defined by a dict below
    # marker=dict(size=25, color=color_4, symbol=marker_list_2, line=dict(width=0.5))
    trace_ema_13 = gobj.Scatter(
        x=df["pd_time"],
        y=df["ema_13"],
        mode="lines",
        name="13-EMA",
        textfont=dct_textfont,
        line=dict(color="blue", width=2),
    )
    trace_sma_50 = gobj.Scatter(
        x=df["pd_time"],
        y=df["sma_50"],
        mode="lines",
        name="50-SMA",
        textfont=dct_textfont,
        line=dict(color="red", width=2),
    )
    trace_sma_200 = gobj.Scatter(
        x=df["pd_time"],
        y=df["sma_200"],
        mode="lines",
        name="200-SMA",
        textfont=dct_textfont,
        line=dict(color="orange", width=2),
    )

    # add the trace object for corresponding subplot and associated scatter plots onto the fig object
    fig.add_trace(trace_subplot_row_1, row=1, col=1)
    fig.add_trace(trace_ema_13, row=1, col=1)
    fig.add_trace(trace_sma_50, row=1, col=1)
    fig.add_trace(trace_sma_200, row=1, col=1)

    # --- subplot 2 on row 2 and column 1 (Volume) ---
    # Prepare subplot with a gobj.Bar object trace for volume without legend
    trace_subplot_row_2 = gobj.Bar(x=df["pd_time"], y=df["volume"], showlegend=False)
    fig.add_trace(trace_subplot_row_2, row=2, col=1)

    print('----BEFORE here subplot 3-------', df.head(3))
    # Clean the 'close' column from NaN values
    df['close'].fillna(method='ffill', inplace=True)  # Forward fill NaN values
    df['close'].fillna(method='bfill', inplace=True)  # Backward fill remaining NaN values

    # --- subplot 3 on row 1 and column 1 (RSI) ---
    # Hack RSI values (*********** temporary testing as the trigger function to calculate does not work **********)
    # Calculate RSI(14) and update the "rsi_14" column
    #df_tmp_rsi = df["close"] / 3
    df['rsi_14'] = ta.RSI(df['close'], timeperiod=14)
    print('----here subplot 3-------', df.head(3))
    print('----here subplot 3 tail -------', df.tail(3))

    # Prepare subplot with a gobj.Scatter object trace for RSI
    trace_subplot_row_3 = gobj.Scatter(
        x=df["pd_time"],
        #                           y=df['rsi_14'], mode='lines', name='RSI', textfont=dct_textfont,
        y=df['rsi_14'],
        mode="lines",
        name="RSI",
        textfont=dct_textfont,
        line=dict(color="green", width=2),
    )

    fig.add_trace(trace_subplot_row_3, row=3, col=1)

    # Remove the default horizontal lines at RSI levels 30, 40, 60, and 70
    fig.update_yaxes(
        rangemode="tozero",  # This ensures that the y-axis starts from 0
        range=[0, 100],  # Customize the y-axis range if needed
        row=3, col=1,  # Specify the subplot
        #showgrid=False,  # Hide grid lines
        #zeroline=False,  # Hide the zero line
        #showline=False,  # Hide the axis line
        ticks="",  # Hide tick marks
    )

    # Add horizontal lines at 20 and 80 levels on the RSI sub-plot
    fig.add_shape(
        dict(
            type="line",
            x0=df["pd_time"].iloc[0],
            x1=df["pd_time"].iloc[-1],
            y0=20,
            y1=20,
            line=dict(color="red", width=2),
        ),
        row=3,
        col=1,
    )

    fig.add_shape(
        dict(
            type="line",
            x0=df["pd_time"].iloc[0],
            x1=df["pd_time"].iloc[-1],
            y0=80,
            y1=80,
            line=dict(color="blue", width=2),
        ),
        row=3,
        col=1,
    )

    # --- subplot 4 on row 4 and column 1 (MACD) --- TODO --
    trace_subplot_row_4 = gobj.Scatter(
        x=df["pd_time"],
        y=df['rsi_14'],                   # ** temporary ***
        mode="lines",
        name="MACD",
        textfont=dct_textfont,
        line=dict(color="blue", width=2),
    )

    fig.add_trace(trace_subplot_row_4, row=4, col=1)

  
    # --- subplot 5 on row 1 and column 1 (ADX) --- TODO --
    trace_subplot_row_5 = gobj.Scatter(x=df['pd_time'],
                                        y=df['rsi_14'], mode='lines', name='ADX', textfont=dct_textfont,
                                        line=dict(color='red', width=2)
                                        )
    
    fig.add_trace(trace_subplot_row_5, row=5, col=1)
  
    # --- Now that all traces have been added, prepare the fig object to be displayed ---
    # Update layout to show y-axis titles
    fig.update_layout(
        yaxis_title_text="OHLC",
        yaxis2_title_text="Volume",
        yaxis3_title_text="RSI",
        yaxis4_title_text="MACD",
        yaxis5_title_text="ADX",
    )

    # Do not show OHLC's rangeslider sub plot
    fig.update_layout(xaxis_rangeslider_visible=False)

    # Update layout to show the title for the new row
    fig.update_layout(
        title_text="Multiple Subplots with OHLC, Volume, RSI, MACD, ADX",
        title_x=0.5,
        title_font=dict(size=14),
    )

    fig.update_layout(width=1100, height=900)

    # Render plot using st.plotly_chart
    st.plotly_chart(
        fig, width=1100, height=900
    )  # make sure to match it with the fig layout, but can also do like below
    # st.plotly_chart(fig, use_container_height=True, use_container_width=True)


def generate_chart_plot_with_sub_plots(df):
    """
    TODO
    https://stackoverflow.com/questions/64689342/plotly-how-to-add-volume-to-a-candlestick-chart
    https://web3-ethereum-defi.readthedocs.io/tutorials/uniswap-v3-price-analysis.html
    """

    candlesticks = gobj.Candlestick(
        x=df["pd_time"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        showlegend=False,
    )

    volume_bars = gobj.Bar(
        x=df["pd_time"],
        y=df["volume"],
        showlegend=False,
        marker={
            "color": "rgba(128,128,128,0.5)",
        },
    )

    fig = gobj.Figure(candlesticks)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(candlesticks, secondary_y=True)
    fig.add_trace(volume_bars, secondary_y=False)
    fig.update_layout(
        title="ETH/USDC pool price data at the very beginning of Uniswap v3",
        height=800,
        # Hide Plotly scrolling minimap below the price chart
        xaxis={"rangeslider": {"visible": False}},
    )
    fig.update_yaxes(title="Price $", secondary_y=True, showgrid=True)
    fig.update_yaxes(title="Volume $", secondary_y=False, showgrid=False)

    #  fig.show()

    # Render plot using plotly_chart
    st.plotly_chart(
        fig, width=1100, height=600
    )  # make sure to increase this appropriately with the other objects
    logger.info("plotly on streamlit main chart rendered")


def streamlit_sidebar_selectbox_symbol_only(dbconn, df):
    """
    this the top-left 2nd selectbox on the sidebarinput
    it shows a list of symbols from a group chosen by previous dropdown
    user will select a symbol
    TODO - what about no output ???

    returns:
      a df with price data generated by the sql_query results for the symbol chosen by user from the Symbol Dropdown
    """

    # Selectbox (dropdown) Sidebar
    sm_chosen_symbol = st.sidebar.selectbox(  # Drop-down named Symbol Dropdown with 3 selectable options
        "Symbol Dropdown", df, key="sm_chosen_symbol", index=None
    )
    st.write("You selected:", sm_chosen_symbol)
    logger.info("type={} sm_chosen_symbol={}", type(sm_chosen_symbol), sm_chosen_symbol)

    sql_query = (
        "select * from tbl_price_data_1day where pd_symbol= '%s'" % sm_chosen_symbol
    )
    logger.info(
        "To get the price data for {} - evaluated sql_query = {}",
        sm_chosen_symbol,
        sql_query,
    )

    # Parameterized query
    # parameters are specified using the colon ( : )
    # sql_with_param = text("""select * from tbl_price_data_1day where pd_symbol= :in_symbol""")
    # dictionary containing parameter name value
    # input_param = {'in_symbol': 'TSLA'}

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
    logger.debug(df_ohlcv_symbol)

    return df_ohlcv_symbol


def generate_table_plot(df):
    st.table(df)
    # st.dataframe(df, 100, 200)


def main():
    # db_conn = connect_to_db_using_psycopg2()
    my_db_uri = "postgresql://postgres:postgres#123@localhost:5432/dbs_invest"
    logger.debug(my_db_uri)
    db_conn = connect_to_db_using_sqlalchemy(my_db_uri)
    wildcard_value_1 = "UN%"
    wildcard_value_2 = "CM%"
    sql_query = text(
        """
      SELECT symbol FROM tbl_instrument 
      WHERE exchange_code NOT LIKE :wildcard_1 AND symbol LIKE :wildcard_2
      ORDER BY symbol
  """
    ).bindparams(wildcard_1=wildcard_value_1, wildcard_2=wildcard_value_2)
    # sql_query = "select symbol, name from viw_instrument_uk_equities where symbol like 'V%' order by symbol"
    logger.debug(
        "Testing DB connection with a test SQL query and retreiving data. sql_query = {} {} {}",
        sql_query,
        wildcard_value_1,
        wildcard_value_2,
    )
    df_symbols = pd.read_sql_query(sql_query, db_conn)
    logger.debug(df_symbols.head(5))

    # accept the user's selection on the symbols_group dropdown and returns list of symbols from that symbols group only
    df_symbols = streamlit_sidebar_selectbox_symbol_group(db_conn)
    # using the above list of symbols, accept the user's selection on  next dropdown selectbox, which is to choose only one symbol from the list
    # when chosen, it will return a full price data df for that symbol
    df_symbol_price_data = streamlit_sidebar_selectbox_symbol_only(db_conn, df_symbols)
    # generate the main chart with all the indicators
    # generate_chart_plot(df_symbol_price_data)
    generate_chart_plot_2(df_symbol_price_data)
    # generate_chart_plot_with_sub_plots(df_symbol_price_data)


# main
if __name__ == "__main__":
    APP_NAME = "Stock App!"
    logger.info("Running", APP_NAME)

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


# -----------------------------

"""   # --- temp --- this the Scans below the chart --- need to seperate out probably --
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
#Use df[df['B']==3]['A'].values[0] if you just want item itself without the brackets """

# ---------------------
