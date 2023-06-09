from datetime import datetime
import inspect
import pandas as pd
import plotly as pl
import plotly.graph_objects as go
from plotly.subplots import make_subplots

INPUT_FILE = 'C:\mytmp\INS-128_FISN_warnings_20220113.csv'


def load_csv_file_into_dataframe(input_file):
    """Loads contents of the csv file passed into a pandas dataframe

    Parameters:
    none

    Returns:
    dataframe

   """
    print('-In function', inspect.currentframe().f_code.co_name,
          '    was called by ', inspect.stack()[1].function)

    print('Loading data from file ', input_file)
    print('dateime today=', datetime.today())
    df_param = pd.read_csv(input_file, infer_datetime_format=True, parse_dates=[
                           'FILE_SUBMISSION_DATE'], encoding='UTF-8')
    print(df_param.head)
    return df_param


def prepare_chart(df):
    '''
    uses the pandas dataframe that contains the data
    '''

    print('-In function', inspect.currentframe().f_code.co_name, '    was called by ', inspect.stack()[1].function)

    fig = go.Figure()   

    # ---- prepare how many individual subplots we need on the entire graph ---
    # The plotly.subplots.make_subplots() function produces a graph object figure that is preconfigured with a grid of subplots that traces can be added to.
    # Initialize figure with subplots
    # graph will have 2 charts (so 2 rows), one on top of the other (so 1 column)
    fig = make_subplots(rows=1, cols=1)

    # ---- prepare all the traces we need on the entire graph ---
    # you can build a complete figure by passing trace and layout specifications to the plotly.graph_objects.Figure constructor.
    # These trace and layout specifications can be either dictionaries or graph objects.
    traces_list = []
    trace11 = go.Scatter(x=df['FILE_SUBMISSION_DATE'],
                            y=df['WARN_CNT'],
                            mode='lines',          # gives us a line chart
                            name='NUMBER OF WARNINGS SEEN ON FISN SUBMISSIONS FOR LEUE',        # legend name
                            # marker=dict(color=color_palette_list),
                            text='FISN warnings for last 300 days')        # text that appears when mouse hovers over this line
    traces_list.append(trace11)
    trace12 = go.Scatter(x=df['MA_13'],
                            y=df['WARN_CNT'],
                            mode='lines',          # gives us a line chart
                            name='MA_13 of Count',        # legend name
                            # marker=dict(color=color_palette_list),
                            text='xxxx')        # text that appears when mouse hovers over this line
    traces_list.append(trace12)
    trace13 = go.Scatter(x=df['FILE_SUBMISSION_DATE'],
                            y=df['MA_50'],
                            mode='lines',          # gives us a line chart
                            name='MA_50 of Count',        # legend name
                            # marker=dict(color=color_palette_list),
                            text='yyyyy')        # text that appears when mouse hovers over this line
 #   traces_list.append(trace13)
    
    #trace2 = go.Bar(x=[1, 2, 3], y=[1, 3, 2])
    #traces_list.append(trace2)
    print('traces_list=')
    print(traces_list)
  
    fig.append_trace(trace11, row=1, col=1)
#    fig.append_trace(trace12, row=1, col=1)
    fig.add_trace(trace13, row=1, col=1)

    #fig.add_trace(trace2)
    # ---- prepare all the layout configuration we need on the entire graph ---
        # set the layout of the chart including how it looks and
        # changeable features such as title, axis titles, font, and spacing.
        # Just like trace, it is a dictionary of dictionaries


    fig.show()

"""
fig = go.Figure()
for contestant, group in df.groupby("Contestant"):
    fig.add_trace(go.Bar(x=group["Fruit"], y=group["Number Eaten"], name=contestant,
      hovertemplate="Contestant=%s<br>Fruit=%%{x}<br>Number Eaten=%%{y}<extra></extra>"% contestant))
fig.update_layout(legend_title_text = "Contestant")
fig.update_xaxes(title_text="Fruit")
fig.update_yaxes(title_text="Number Eaten")
fig.show()





# Add count line chart  (Scatter is also a line chart)
fig.add_trace(go.Scatter(y=[4, 2, 1], mode="lines"), row=1, col=1)
fig.add_trace(go.Bar(y=[2, 1, 3]), row=1, col=2)

# Set theme, margin, and annotation in layout
fig.update_layout(
    template="plotly_dark",
    margin=dict(r=10, t=25, b=40, l=60),
    annotations=[
        dict(
            text="Source: NOAA",
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=0)
    ]
)

# another example of update
fig.update_layout(
    title='The Great Recession',
    yaxis_title='AAPL Stock',
    shapes = [dict(
        # draws a vertical line
        x0='2016-12-09', x1='2016-12-09', y0=0, y1=1, xref='x', yref='paper',
        line_width=2)],
    annotations=[dict(
        x='2016-12-09', y=0.05, xref='x', yref='paper',
        showarrow=False, xanchor='left', text='Increase Period Begins')]
)

# custom candlestick colors
fig = go.Figure(data=[go.Candlestick(
    x=df['Date'],
    open=df['AAPL.Open'], high=df['AAPL.High'],
    low=df['AAPL.Low'], close=df['AAPL.Close'],
    increasing_line_color= 'cyan', decreasing_line_color= 'gray'
)])


fig.update_xaxes(title_text='Date') # Set X-Axis title
fig.update_yaxes(title_text='Warnings Count') # Set &-Axis title
fig.update_layout(title = 'INS-128 Warnings on FISN for last 300 days for MIC: LEUE')

fig.show()

# Then we re-structure the DataFrame index to change the *Date* column from an index column to a data column.
df_1.reset_index(level=0, inplace=True)







New traces can be added to a graph object figure using the add_trace() method. This method accepts a graph object trace (an instance of go.Scatter, go.Bar, etc.) and adds it to the figure. This allows you to start with an empty figure, and add traces to it sequentially. The append_trace() method does the same thing, although it does not return the figure.

import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(go.Bar(x=[1, 2, 3], y=[1, 3, 2]))
fig.show()


"""

"""
  traces_list_AMER, traces_list_APAC, traces_list_EMEA = [], [], []

   # for proc_name in ['IndicationManager_Europe_0-4',
   # 'IndicationManager_Europe_5-9', 'IndicationManager_Europe_A-C']:
   for proc_name in processnames_list:
        # create df with records for this process name only
        print('Generating trace for ' + proc_name)
        df_for_this_proc = df_param[df_param[column_name] == proc_name]
        # print('dataframe created with shape ')
        # print(df_for_this_proc.shape)
        # trace is a dictionary of (dictionaries) parameters of the data to
        # be plotted, as well as information about the color and line types
        trace = gobj.Scatter(x=df_for_this_proc['trade_date'],
                             #                             y=df_for_this_proc['max_indication_count'],
                             y=df_for_this_proc[column_param],
                             mode='lines',          # gives us a line chart
                             name=proc_name,        # legend name
                             marker=dict(color=color_palette_list),
                             text=proc_name)        # hover line name
        print('Appending trace to trace_list')
        if ('USA' in proc_name or 'USA' in proc_name or 'Canada' in proc_name or 'CANADA' in proc_name or 'LATIN_AMERICA' in proc_name):
            print('---11--- ' + proc_name)
            traces_list_AMER.append(trace)
        elif ('Asia' in proc_name or 'ASIA' in proc_name):
            print('---22--- ' + proc_name)
            traces_list_APAC.append(trace)
        elif ('Europe' in proc_name or 'EUROPE' in proc_name):
            print('---33--- ' + proc_name)
            traces_list_EMEA.append(trace)
        print('End of Loop')

    # This is a list of all the individual trace objects that need to be
    # plotted onto the chart
    print('traces_list')
    print(traces_list_EMEA)
#    print(traces_list.__dict__)

    # set the layout of the chart including how it looks and
    # changeable features such as title, axis titles, font, and spacing.
    # Just like trace, it is a dictionary of dictionaries
    '''
    layout = dict(showlegend=True,
                  title='IndicationManager - All Regions - Max Indication '
                  'Count for last 1 year',
                  xaxis=dict(title='Dates', ticklen=5, zeroline=False)
                  )
    '''

    layout = dict(showlegend=True,
                  title='IndicationManager - All Regions - Max Indication '
                  'Count for last 1 year',
                  xaxis=dict(
                        title='Dates',
                        titlefont=dict(family='Arial, sans-serif',
                                       size=12, color='#909090'),
                      showticklabels=True,
                      tickangle=-45,
                      tickfont=dict(family='Arial, sans-serif',
                                    size=12, color='#909090'),
                  )
                  )
    # need to made title a variable ---

    '''
    an example --- 
    layout = go.Layout(
    title='Elephant in the Valley Survey Results',
    font=dict(color='#909090'),
    xaxis=dict(
        title='Question Key',
        titlefont=dict(
            family='Arial, sans-serif',
            size=12,
            color='#909090'
        ),
        showticklabels=True,
        tickangle=-45,
        tickfont=dict(
            family='Arial, sans-serif',
            size=12,
            color='#909090'
        ),
),
    yaxis=dict(
        range=[0,100],
        title="Percentage of Yes Responses to Question",
        titlefont=dict(
            family='Arial, sans-serif',
            size=12,
            color='#909090'
        ),
        showticklabels=True,
        tickangle=0,
        tickfont=dict(
            family='Arial, sans-serif',
            size=12,
            color='#909090'
        )
    )
)
    '''

    # finally compile the data and the layout which eventually gets passed to
    # the plotting function that we choose.
    output_file = OUTPUT_DIR + '/' + 'AMER' + '_' + column_param + '.html'
    print('Plotting chart for AMER into file ' + output_file)
    fig = dict(data=traces_list_AMER, layout=layout)
    pl.offline.plot(fig, filename=output_file, auto_open=False)


'''
    output_file = OUTPUT_DIR + '/' + 'APAC' + '_' + column_param + '.html'
    print('Plotting chart for APAC into file ' + output_file)
    fig = dict(data=traces_list_APAC, layout=layout)
    pl.offline.plot(fig, filename=output_file, auto_open=False)

    output_file = OUTPUT_DIR + '/' + 'EMEA' + '_' + column_param + '.html'
    print('Plotting chart for EMEA into file ' + output_file)
    # fig = dict(data=traces_list, layout=layout)
    fig = dict(data=traces_list_EMEA, layout=layout)
    # pl.offline.plot(fig)        # will display in browser
    # saves to a file and does not display to browser
    pl.offline.plot(fig, filename=output_file, auto_open=False)
    # todo - need to look at write_html
    # https://plotly.github.io/plotly.py-docs/generated/plotly.io.write_html.html
"""


def main():
    '''
    the main function
    '''
    df_csv = load_csv_file_into_dataframe(INPUT_FILE)
    df_csv['MA_13'] = df_csv['WARN_CNT'].rolling(window=13).mean()
    df_csv['MA_50'] = df_csv['WARN_CNT'].rolling(window=50).mean()
    df_csv.dropna(inplace=True)
    prepare_chart(df_csv)
    # prepare_chart(df_fmtd, 'max_streamer_orders_count')
    print('Exiting..')


if __name__ == '__main__':
    main()
