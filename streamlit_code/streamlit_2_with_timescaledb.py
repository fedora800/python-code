import sys
import os
from loguru import logger
import streamlit as st
import pandas as pd
import talib as ta
from config import DB_INFO, DEBUG_MODE


# UserWarning: pandas only supports SQLAlchemy connectable (engine/connection) or database string URI or sqlite3 DBAPI2 connection. Other DBAPI2 objects are not tested. Please consider using SQLAlchemy.
import plotly.graph_objects as gobj
from plotly.subplots import make_subplots

# from mod_utils_db import connect_to_db_using_sqlalchemy
import mod_utils_db as m_udb
import mod_yfinance as m_yfn
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


def fn_st_sb_selectbox_symbol_group(dbconn):
    """
    this the top-left 1st selectbox on the sidebarinput
    user will select the group of symbols he wants to start on (eg US ETFs, UK ETFs, US S&P500 constituents etc)
    TODO - what about no output ???

    returns:
      a df with the output of the the sql_query results (symbols list) corresponding to what option we chose from the dropdown
    """

    print("---100---fn_st_sb_selectbox_symbol_group------START-----")
    logger.debug("Arguments : {}", dbconn)

    dct_options = {
        "symbol_groups": ["US S&P500 constituents", "US ETFs", "UK ETFs"],
        "symbol_groups_sqlquery": [
            """select symbol, name from viw_instrument_us_sp500_constituents where symbol like '%CO%';""",
            """select symbol, name from viw_instrument_us_etfs where symbol like '%AC%';""",
            """select symbol, name from viw_price_data_uk_most_traded;""",
        ],
    }

    # load data into a df
    df_select_options = pd.DataFrame(dct_options)
    logger.debug(
        "type={}. df_select_options={}", type(df_select_options), df_select_options
    )

    # Take input from Sidebar selectbox to select a symbol list group
    sg_chosen_option = st.sidebar.selectbox(
        "Symbol Groups Dropdown",  # Drop-down named Symbol Dropdown
        df_select_options["symbol_groups"],
        key="sg_chosen_option",
        index=None,
    )
    st.markdown("You selected from symbol_groups dropdown: :red[{}]".format(sg_chosen_option))
    logger.info("You selected from the Symbol Groups Dropdown - sg_chosen_option={}", sg_chosen_option)

    # initial the return df
    df_symbols = pd.DataFrame()

    # if user chooses from the symbol group dropdown, then run the sql query and return values into a dataframe
    if sg_chosen_option:
        sg_chosen_sql_query = df_select_options[
            df_select_options["symbol_groups"] == sg_chosen_option
        ]["symbol_groups_sqlquery"].iloc[0]
        logger.info(
            "streamlit_sidebar_selectbox_symbolgroup - CHOSEN SQL_QUERY = {}",
            sg_chosen_sql_query,
        )
        logger.info("User chose from Symbol Groups Dropdown : {} ", sg_chosen_sql_query)
        sql_query = text(sg_chosen_sql_query)
        df_symbols = pd.read_sql_query(sql_query, dbconn)

    df_head_foot = pd.concat([df_symbols.head(1), df_symbols.tail(1)])
    logger.debug("Returning Symbol List as df_head_foot = {} ", df_head_foot)

    print("---100---fn_st_sb_selectbox_symbol_group------FETCHING DATA FOR ALL SYMBOLS IN THIS GROUP -----")
    # *** IT DOES THIS AGAIN AND AGAIN *****
    # for index, row in df_symbols.iterrows():
    #   logger.trace("Syncing data for {} - {}", row["symbol"], row["name"])
    #   m_yfn.sync_price_data_in_table_for_symbol("YFINANCE", dbconn, row["symbol"])
    #   st.markdown("Syncing data for :blue[{}]".format(row["symbol"]))

    print("---100---fn_st_sb_selectbox_symbol_group------END     RETURNING-----")
    return df_symbols


def generate_plotly_chart(dbconn, symbol, df):
    """
    https://stackoverflow.com/questions/64689342/plotly-how-to-add-volume-to-a-candlestick-chart
    https://plotly.com/python/subplots/
    https://plotly.com/python/mixed-subplots/
    https://plotly.com/python/table-subplots/
    """

    # Create subplots with specific settings
    #
    fig = make_subplots(
        rows=6,  # 6 means each plot below the other plot vertically
        cols=1,  # just 1, but 2 would mean one plot besides the other horizontally
        shared_xaxes=True,  # Share axes among subplots in the same column
        vertical_spacing=0.03,  # Space between subplot rows in normalized plot coordinates. Must be a float between 0 and 1
        subplot_titles=(
            "OHLC",
            "Volume",  # Title of each subplot need mentioning as a list in row-major ordering.
            "RSI",
            "MACD",
            "ADX",
            "CRS",
        ),
        row_width=[
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.5,
        ],  # the relative HEIGHTS for each row of subplots, should total 1.0
        # NOTE - they seem to be in reverse, ie biggest 0.5 is the top-most
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

    # Clean the 'close' column from NaN values
    # df['close'].fillna(method='ffill', inplace=True)  # Forward fill NaN values
    df["close"].ffill(inplace=True)
    # df['close'].fillna(method='bfill', inplace=True)  # Backward fill remaining NaN values
    df["close"].bfill(inplace=True)

    # --- subplot 3 on row 1 and column 1 (RSI) ---
    # Calculate RSI(14)
    # TODO:  update the "rsi_14" column back in the table
    df["rsi_14"] = ta.RSI(df["close"], timeperiod=14)
    logger.trace("--dfhead={}----dftail={}----", df.head(1), df.tail(1))

    # Prepare subplot with a gobj.Scatter object trace for RSI
    trace_subplot_row_3 = gobj.Scatter(
        x=df["pd_time"],
        #                           y=df['rsi_14'], mode='lines', name='RSI', textfont=dct_textfont,
        y=df["rsi_14"],
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
        row=3,
        col=1,  # Specify the subplot
        # showgrid=False,  # Hide grid lines
        # zeroline=False,  # Hide the zero line
        # showline=False,  # Hide the axis line
        ticks="",  # Hide tick marks
    )

    # Add horizontal lines at 20 and 80 levels on the RSI sub-plot
    fig.add_shape(
        dict(
            type="line",
            x0=df["pd_time"].iloc[0],
            x1=df["pd_time"].iloc[-1],
            y0=40,
            y1=40,
            line=dict(color="red", width=1),
        ),
        row=3,
        col=1,
    )

    fig.add_shape(
        dict(
            type="line",
            x0=df["pd_time"].iloc[0],
            x1=df["pd_time"].iloc[-1],
            y0=60,
            y1=60,
            line=dict(color="blue", width=1),
        ),
        row=3,
        col=1,
    )

    # --- subplot 4 on row 4 and column 1 (MACD) --- TODO --
    df_macd = pd.DataFrame()
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    na_macd, na_macd_signal, na_macd_hist = ta.MACD(
        df["close"].to_numpy(),
        fastperiod=MACD_FAST,
        slowperiod=MACD_SLOW,
        signalperiod=MACD_SIGNAL,
    )
    df_macd["macd"] = na_macd
    df_macd["signal"] = na_macd_signal
    df_macd["histogram"] = na_macd_hist
    logger.trace("-------df_macd.info={}---df_macd={}---", df_macd.info(), df_macd)

    trace_macd_macd = gobj.Scatter(
        x=df["pd_time"],
        y=df_macd["macd"],
        mode="lines",
        name="MACD",
        textfont=dct_textfont,
        line=dict(color="blue", width=2),
    )
    trace_macd_signal = gobj.Scatter(
        x=df["pd_time"],
        y=df_macd["signal"],
        mode="lines",
        name="MACD Signal",
        textfont=dct_textfont,
        line=dict(color="red", width=2),
    )
    trace_macd_histogram = gobj.Bar(
        x=df["pd_time"],
        y=df_macd["histogram"],
        name="MACD Histogram",
        # textfont=dct_textfont,
        # marker=dict(color="green", width=2),
        marker={
            "color": "rgba(50,120,70,0.5)",
        },
    )

    # add the trace object for corresponding subplot and associated scatter plots onto the fig object
    fig.add_trace(trace_macd_macd, row=4, col=1)
    fig.add_trace(trace_macd_signal, row=4, col=1)
    fig.add_trace(trace_macd_histogram, row=4, col=1)

    # --- subplot 5 on row 1 and column 1 (ADX) ---
    df_adx = pd.DataFrame()
    TIME_PERIOD = 14
    na_ADX = ta.ADX(df["high"], df["low"], df["close"], TIME_PERIOD)
    na_DMI_MINUS = ta.MINUS_DI(df["high"], df["low"], df["close"], TIME_PERIOD)
    na_DMI_PLUS = ta.PLUS_DI(df["high"], df["low"], df["close"], TIME_PERIOD)

    df_adx["adx"] = na_ADX
    df_adx["dmi_minus"] = na_DMI_MINUS
    df_adx["dmi_plus"] = na_DMI_PLUS
    print(f"-------{df_adx.info()}---df_adx = {df_adx}---")

    trace_adx_adx = gobj.Scatter(
        x=df["pd_time"],
        y=df_adx["adx"],
        mode="lines",
        name="MACD",
        textfont=dct_textfont,
        line=dict(color="blue", width=2),
    )
    trace_adx_minus = gobj.Scatter(
        x=df["pd_time"],
        y=df_adx["dmi_minus"],
        mode="lines",
        name="DMI MINUS",
        textfont=dct_textfont,
        line=dict(color="red", width=1),
    )
    trace_adx_plus = gobj.Scatter(
        x=df["pd_time"],
        y=df_adx["dmi_plus"],
        mode="lines",
        name="DMI PLUS",
        textfont=dct_textfont,
        line=dict(color="green", width=1),
    )

    # add the trace object for corresponding subplot and associated scatter plots onto the fig object
    fig.add_trace(trace_adx_adx, row=5, col=1)
    fig.add_trace(trace_adx_minus, row=5, col=1)
    fig.add_trace(trace_adx_plus, row=5, col=1)

    # add a line at 25 level on this sub-plot
    fig.add_shape(
        dict(
            type="line",
            x0=df["pd_time"].iloc[0],
            x1=df["pd_time"].iloc[-1],
            y0=25,
            y1=25,
            line=dict(color="brown", width=1),
        ),
        row=5,
        col=1,
    )



    # --- subplot 6 on row 1 and column 1 (CRS) ---
    benchmark_symbol = "SPY"
    df_benchmark_symbol = m_udb.get_table_data_for_symbol(dbconn, benchmark_symbol)

    #df_CRS = m_ti.fn_02_comparative_relative_strength_CRS_indicator(benchmark_symbol, df_benchmark_symbol, symbol, df)

    # TODO:  update the "CRS" column back in the table
    #logger.trace("--dfhead={}----dftail={}----", df_CRS.head(1), df_CRS.tail(1))

    # Prepare subplot with a gobj.Scatter object trace for CRS
    trace_subplot_row_6 = gobj.Scatter(
        x=df["pd_time"],
        y=df["crs_50"],
        mode="lines",
        name="CRS",
        textfont=dct_textfont,
        line=dict(color="orange", width=4),
    )

    fig.add_trace(trace_subplot_row_6, row=6, col=1)

    # Add horizontal lines at 0 level on the CRS sub-plot
    fig.add_shape(
        dict(
            type="line",
            x0=df["pd_time"].iloc[0],
            x1=df["pd_time"].iloc[-1],
            y0=0,
            y1=0,
            line=dict(color="black", width=1),
        ),
        row=6,
        col=1,
    )


    # --- Now that all traces have been added, prepare the fig object to be displayed ---
    # Update layout to show y-axis titles
    fig.update_layout(
        yaxis_title_text="OHLC",
        yaxis2_title_text="Volume",
        yaxis3_title_text="RSI",
        yaxis4_title_text="MACD",
        yaxis5_title_text="ADX",
        yaxis6_title_text="CRS",
    )

    # Do not show OHLC's rangeslider sub plot
    fig.update_layout(xaxis_rangeslider_visible=False)

    # Update layout to show the title for the new row
    fig.update_layout(
        title_text="Multiple Subplots with OHLC, Volume, RSI, MACD, ADX, CRS",
        title_x=0.5,
        title_font=dict(size=14),
    )

    #     # Update the layout for X-axis so that weekends and holidays (shows gaps on chart) are omitted from plotting
    #     fig.update_xaxes(
    #         rangebreaks = [
    #             # NOTE: Below values are bound (not single values), ie. hide x to y
    #             dict(bounds=["sat", "mon"]),                 # hide weekends, eg. hide sat to before mon
    #             dict(bounds=[16, 9.5], pattern="hour"),      # hide hours outside of 9.30am-4pm
    #             # dict(values=["2023-12-25", "2024-01-01"])  # hide holidays (Christmas and New Year's, etc)
    #         ]
    #     )

    fig.update_layout(
        width=1100,
        # height=600,
        height=1500,
        # paper_bgcolor="LightSteelBlue"
    )

    # Render plot using st.plotly_chart
    st.plotly_chart(
        fig,
        width=1100,
        # height=900
        height=1500,
    )  # make sure to match it with the fig layout, but can also do like below
    # st.plotly_chart(fig, use_container_height=True, use_container_width=True)

    logger.debug("End of function generate_chart_plot_2 ...")





def fn_st_sb_selectbox_symbol_only(dbconn, df):
  """
  this the top-left 2nd selectbox on the sidebarinput
  it shows a list of symbols from which user will select one symbol
  this symbol list changes dynamically based off the group chosen on the previous dropdown
  TODO - what about no output ???

  returns:
    symbol
    a df with price data generated by the sql_query results for the symbol chosen by user from the Symbol Dropdown
  """

  df_head_foot = pd.concat([df.head(1), df.tail(1)])
  logger.debug("----- ENTERED fn_st_sb_selectbox_symbol_only -----")
  logger.debug("Arguments : dbconn = {}, df_head_foot = {}", dbconn, df_head_foot)

  # Selectbox (dropdown) Sidebar
  sm_chosen_symbol = st.sidebar.selectbox(  # Drop-down named Symbol Dropdown with 3 selectable options
      "Symbol Dropdown", df, key="sm_chosen_symbol", index=None
  )
  st.markdown("You selected from Symbol dropdown: :red[{}]".format(sm_chosen_symbol))
  logger.info("You selected from the Symbol Dropdown - sm_chosen_symbol={}", sm_chosen_symbol)

  if sm_chosen_symbol:
      # TODO: for efficiency, i should be remove this sync bit from here and put it 1 level up, when we select the symbol group
      # at that level, we can sync all the symbols for that symbol group in 1 shot, so then when we do lookup here, that data is all in sync
      df_ohlcv_symbol, df_sym_stats = m_yfn.sync_price_data_in_table_for_symbol(
          "YFINANCE", dbconn, sm_chosen_symbol
      )
      logger.debug("df_ohlcv_symbol = {}, df_sym_stats = {}", df_ohlcv_symbol, df_sym_stats)
      if not df_sym_stats.empty:
        ps_sym_stats = df_sym_stats.iloc[0]  # Extract the first row as a Series
        st_sym_stats = '  /  '.join(map(str, ps_sym_stats))  # Convert each value to string and join them with given delimiter
        logger.debug("Arguments : dbconn = {}, df_head_foot = {}", dbconn, df_head_foot)
        st.markdown("Symbol Stats from DB : **:blue[{}]**".format(st_sym_stats))
      print("---200---fn_st_sb_selectbox_symbol_only------END    RETURNING-----")
      return sm_chosen_symbol, df_ohlcv_symbol
  else:
      print(
          "-----200--user has not yet chosen from the symbol group dropdown-------------"
      )
      return None, None
      print("---200---fn_st_sb_selectbox_symbol_only------END    NOTHING RETURNED-----")


def sb_inputbox_symbol(data_venue: str, dbconn, symbol: str) -> str:
    """
    User inputs a symbol in sidebar input box and this will first check if the symbol exists on the data venue we chose.

    Parameters:
    - data_venue (str): The string representing the data venue.
    - dbconn : DB connection handle
    - symbol (str): The string representing the symbol.

    Returns:
    str: a string containing some summary information

    Example:
    >>> sb_inputbox_symbol("YFINANCE", dbconn, "AAPL")
    """

    # TODO: first check if symbol exists on the data source and throw error if not
    logger.warning("TODO: Need to code the function where it checks if the symbol is valid for that data venue ...")
    df_ohlcv_symbol, df_sym_stats = m_yfn.sync_price_data_in_table_for_symbol(data_venue, dbconn, symbol)
    generate_plotly_chart(dbconn, symbol, df_ohlcv_symbol)



def generate_table_plot(df):
    st.table(df)
    # st.dataframe(df, 100, 200)


def fn_st_selectbox_scans(dbconn):
    """_summary_

    Args:
        dbconn (_type_): db connection handle

    Returns:
        _type_: _description_
    """

    """
  this the top-left 1st selectbox on the sidebarinput
  user will select the group of symbols he wants to start on (eg US ETFs, UK ETFs, US S&P500 constituents etc)
  TODO - what about no output ???

  returns:
    a df with the output of the the sql_query results (symbols list) corresponding to what option we chose from the dropdown
  """

    logger.debug("Arguments : {}", dbconn)

    dct_options = {
        "scan_name": ["stocks below SMA50", 
                      "stocks_above_SMA50",
                      "UK_most_traded_stocks_above_SMA50"
        ],
        "scan_sqlquery": [
            "select * from viw_latest_price_data_by_symbol where close < sma_50",
            "select * from viw_latest_price_data_by_symbol where close > sma_50",
#            "select * from viw_price_data_uk_most_traded"
            "select * from viw_tmp_001"
        ],
    }

    # load data into a DataFrame object:
    df_select_options = pd.DataFrame(dct_options)
    logger.debug(
        "type={}. df_select_options={}", type(df_select_options), df_select_options
    )

    # Take input from selectbox to select a specific scan
    chosen_sb_option_scan = st.selectbox(
        "Scans Dropdown",  # Drop-down named Scans Dropdown
        df_select_options["scan_name"],
        key="chosen_sb_option_scan",
        index=None,
    )
    st.markdown("You selected from scans dropdown: :red[{}]".format(chosen_sb_option_scan))
    logger.info("You selected from the Scans Dropdown - chosen_sb_option_scan={}", chosen_sb_option_scan)

    # initial the return df
    df_symbols = pd.DataFrame()

    # if user chooses from the Scans dropdown, then run the sql query and return values into a dataframe
    if chosen_sb_option_scan:
        chosen_sql_query_scan = df_select_options[
            df_select_options["scan_name"] == chosen_sb_option_scan
        ]["scan_sqlquery"].iloc[0]
        logger.info("st_selectbox_scans - CHOSEN SQL_QUERY = {}", chosen_sql_query_scan)
        sql_query = text(chosen_sql_query_scan)
        df_symbols = pd.read_sql_query(sql_query, dbconn)

        # Now display this dataframe data as a nice table on the frontend. (note - will break down when you have >1000 rows)
        st.write("### ", chosen_sb_option_scan)
        st.write(df_symbols)
        # TODO: below stuff when we need user to choose some from among the rows
        # selected_indices = st.multiselect('Select rows:', df_symbols.index)
        # selected_rows = df_symbols.loc[selected_indices]
        # st.write('### Selected Rows', selected_rows)

        logger.debug("Returning df ={} ", df_symbols)

    return df_symbols


def main():
  
  # db_conn = connect_to_db_using_psycopg2()
  # my_db_uri = "postgresql://postgres:postgres#123@localhost:5432/dbs_invest"
  my_db_uri = f"postgresql://{DB_INFO['USERNAME']}:{DB_INFO['PASSWORD']}@{DB_INFO['HOSTNAME']}:{DB_INFO['PORT']}/{DB_INFO['DATABASE']}"

  logger.debug(my_db_uri)
  db_conn = m_udb.create_database_engine_sqlalchemy(my_db_uri)
  wildcard_value_1 = "LSE%"
  wildcard_value_2 = "A%"
  # sql_query = text(
  #   """
  #   SELECT symbol FROM tbl_instrument
  #   WHERE exchange_code NOT LIKE :wildcard_1 AND symbol LIKE :wildcard_2
  #   ORDER BY symbol
  #   """
  # ).bindparams(wildcard_1=wildcard_value_1, wildcard_2=wildcard_value_2)

  sql_query = text(
      """
    SELECT symbol FROM tbl_instrument 
    WHERE exchange_code LIKE :wildcard_1 AND symbol LIKE :wildcard_2
    ORDER BY symbol
    """
  ).bindparams(wildcard_1=wildcard_value_1, wildcard_2=wildcard_value_2)

  # # sql_query = "select symbol, name from viw_instrument_uk_equities where symbol like 'V%' order by symbol"
  logger.debug(
      "Testing DB connection with a test SQL query and retreiving data. sql_query = {} {} {}",
      sql_query,
      wildcard_value_1,
      wildcard_value_2,
  )
  df_symbols = pd.read_sql_query(sql_query, db_conn)
  logger.debug(df_symbols.head(5))

  # --- SIDEBAR -- SELECTBOX -- FOR SYMBOL_GROUP DROPDOWN ---
  # accept the user's selection on the symbols_group dropdown and returns list of symbols from that symbols group only
  df_symbols_list = fn_st_sb_selectbox_symbol_group(db_conn)
  # using the above list of symbols, now await the user's selection on the next dropdown selectbox, which is to choose only one symbol from the list
  # when chosen, it will return a full price data df for that symbol
  if not df_symbols_list.empty:
      print(f"---2000--type= {type(df_symbols_list)} ----")
      df_symbol_price_data = pd.DataFrame()
      # --- SIDEBAR -- SELECTBOX -- FOR SYMBOL DROPDOWN ---
      symbol, df_symbol_price_data = fn_st_sb_selectbox_symbol_only(db_conn, df_symbols_list)
      print(
          f"---222--type= {type(df_symbol_price_data)} ----df = {df_symbol_price_data}----"
      )
      if df_symbol_price_data is not None:
          # generate the main chart with all the indicators
          # generate_chart_plot(df_symbol_price_data)
          logger.debug("df_symbol_price_data = {}", df_symbol_price_data)
          generate_plotly_chart(db_conn, symbol, df_symbol_price_data)
          # generate_chart_plot_with_sub_plots(df_symbol_price_data)

  print("---3000---")

  # --- SIDEBAR -- TEXT INPUT BOX -- SYMBOL FOR DATA DOWNLOAD ---
  sb_symbol = st.sidebar.text_input("Symbol for Data Download", value=None, max_chars=7)
  st.markdown("You selected symbol via text_input box : :red[{}]".format(sb_symbol))
  logger.info("You selected symbol via text_input box ={}", sb_symbol)
  if sb_symbol:
    st_response = sb_inputbox_symbol("YFINANCE", db_conn, sb_symbol)
    st.write("sb_inputbox_symbol return string = {}", st_response)
    logger.info("sb_inputbox_symbol return string = {}", st_response)

  print("---4000---")
  df_scans = fn_st_selectbox_scans(db_conn)
  print("----df_scans result = ", df_scans)
  print("--- end of main() ---")


# main
if __name__ == "__main__":
    dashline = "-" * 80
    for i in range(2):
        print(dashline)

    print("Python path:", sys.path)
    # Add the project directory to the Python path
    project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, project_directory)
    from technical_analysis import mod_technical_indicators as m_ti

    logger.remove()  # First remove the default logger

    if DEBUG_MODE:
        LOGGING_LEVEL = "TRACE"
        # LOGGING_LEVEL = 'DEBUG'     # this is the loguru default
    else:
        LOGGING_LEVEL = "INFO"  # our default logging level

    logger.add(sys.stderr, level=LOGGING_LEVEL)  # sets the logging level
    logger.info("Logging level set to {} ", LOGGING_LEVEL)

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
