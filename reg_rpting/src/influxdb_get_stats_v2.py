from datetime import datetime
import inspect
import re

import pandas as pd
import plotly as pl
import plotly.graph_objects as gobj


#import sys
#from datetime import *
#from plotly.offline import plot
# INPUT_FILE='C:\\mytmp\\file-downloads\\im_max_count_2020-02-03_fmtd.csv'
#INPUT_FILE_IM = 'C:\\mytmp\\file-downloads\\im_max_count.archive_2020-02-25.prod_archive_fmtd.csv'
INPUT_FILE_IM = 'C:\\mytmp\\influxdb_stats\\IM\\im_max_count_2020-07-16.prod_archive_fmtd.csv'
#INPUT_FILE_STREAMER = 'C:\\mytmp\\file-downloads\\streamer_max_count_2020-03-09.prod_archive_fmtd.csv'
INPUT_FILE_STREAMER = 'C:\\mytmp\\influxdb_stats\\Streamer\\streamer_max_count_2020-07-16.prod_archive_fmtd.csv'
OUTPUT_DIR = 'C:\\mytmp\\influxdb_stats'
TRADING_HOLIDAYS_AMER = ['2020-01-01', '2020-01-20',
                         '2020-02-17', '2020-04-10', '2020-05-25', '2020-07-03']
color_palette_list = ['#009ACD', '#ADD8E6',
                      '#63D1F4', '#0EBFE9', '#C1F0F6', '#0099CC']   # will need to see how to handle to colours


def show_packages_version():
    """Shows the versions of all the packages being used in the program

    Parameters:
    none

    Returns:
    none

    """
    print('-In function', inspect.currentframe().f_code.co_name,
          '    was called by ', inspect.stack()[1].function)
    print('pandas version=', pd.__version__)
    print('plotly version=', pl.__version__)


def load_csv_file_into_dataframe(input_file):
    """Loads contents of the csv file passed into a pandas dataframe

    Parameters:
    none

    Returns:
    dataframe

   """
    print('-In function', inspect.currentframe().f_code.co_name,
          '    was called by ', inspect.stack()[1].function)

    # print('Loading data from file ', INPUT_FILE)
    print('Loading data from file ', input_file)
    print('dateime today=', datetime.today())
    # infer_datetime_format makes it 10x faster
    df_param = pd.read_csv(INPUT_FILE_STREAMER, infer_datetime_format=True,
                           parse_dates=['time'], encoding='UTF-8')
    print(df_param.head)
    print(df_param.info())
    return df_param


def customize_data(df_param):
    """Changes data in the dataframe according to our requirements

     Parameters:
     dataframe

     Returns:
     Modified dataframe

    """

    SATURDAY = 5
    SUNDAY = 6

    print('-In function', inspect.currentframe().f_code.co_name,
          '    was called by ', inspect.stack()[1].function)
    # change the column name in header in place
    df_param.rename(columns={'time': 'trade_date'}, inplace=True)
    # create a additional column in the dataframe that will contain the
    # corresponding day of the week
    df_param = df_param.assign(day_of_week=df_param['trade_date'].dt.weekday)
    # Monday is 0 and Sunday is 6
    # remove records for weekend dates from the dataset in place
    df_param.drop(df_param[df_param['day_of_week']
                           == SATURDAY].index, inplace=True)
    df_param.drop(df_param[df_param['day_of_week']
                           == SUNDAY].index, inplace=True)
    # df_param['trade_date'] = df_param['trade_date'].astype('datetime64[ns]')
    # # no difference
    df_param['trade_date'] = pd.to_datetime(df_param['trade_date'])

    # this is temporary for testing, to remove later ---
    # df_param.drop(df_param[df_param['trade_date']
    # df_test = df_param[(df_param['trade_date'] == '2019-04-17')
    #                   & (df_param['processname'] != 'Streamer_CANADA_0-Z')]

    print('---test2--')
    # df_test2 = df_param[(df_param['max_streamer_orders_count'] <= 10) & ((  # good way to get the exceptions
    # df_param['processname'] == 'Streamer_USA_0-B') |
    # (df_param['processname'] == 'Streamer_USA_U-Z'))]

    filter_list = ['Streamer_USA_C-D', 'Streamer_USA_E-G', 'Streamer_USA_H-K']
    df_test2 = df_param[df_param['processname'].isin(filter_list)]
    print(df_test2)

    print('---test3--')
    df_test3 = df_test2[df_test2['trade_date'].isin(TRADING_HOLIDAYS_AMER)]
    print(df_test3)

    df_test = df_param[(df_param['trade_date'] != '2019-04-19')]
    print('---555--')
    print(df_test)
    print(df_test.info())
    df_param = df_test

    # todo- need to also remove 25-dec and 01-jan data as holidays for all regions -   so wil need to probably define a holiday list
    # remove 26-dec for emea as boxing day ---
    # also there are other bank holidays that need removal from display for
    # EMEA
    # we will likely need to do different holidays for different regions

    print('---444---')
    #holiday_date_test = datetime(2019, 4, 19)
    #print('holiday_date_test  ', holiday_date_test)

    print(df_param)
    print(df_param.info())

    return df_param


def prepare_chart(df_param, column_param):
    '''
    uses the pandas dataframe that contains the data
    also takes the name of the column that needs to be graphed as an input
    '''

    print('-In function', inspect.currentframe().f_code.co_name,
          '    was called by ', inspect.stack()[1].function)
    column_name = 'processname'
    print('Dataframe has below unique list of values on filtered column '
          + column_name)
    processnames_list = df_param[column_name].unique()
    print(processnames_list)
    # get a list of unique values under column processname
    # process_list = df_param.processname.unique()   # use later when we are
    # ready to do this in a loop

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
'''


def main():
    '''
    the main function
    '''
    show_packages_version()
    # df_csv = load_csv_file_into_dataframe(INPUT_FILE)
    df_csv = load_csv_file_into_dataframe(INPUT_FILE_STREAMER)
    df_fmtd = customize_data(df_csv)
    # prepare_chart(df_fmtd, 'max_indication_count')
    prepare_chart(df_fmtd, 'max_streamer_orders_count')


if __name__ == '__main__':
    main()

print('Exiting..')

'''
mine:
- save in png/html file

IndicationManager_Europe_0-4
IndicationManager_Europe_5-9
IndicationManager_Europe_A-C
IndicationManager_Europe_D-E
IndicationManager_Europe_F-H
IndicationManager_Europe_I-L
IndicationManager_Europe_M-O
IndicationManager_Europe_P-R
IndicationManager_Europe_S-T
IndicationManager_Europe_U-Z

$ awk -F',' '{print $2}' im_max_count.archive_2020-02-25.prod_archive_fmtd.csv | sort | uniq -c | grep Europe | awk '{print $2}' | tr '[A-Z]' '[a-z]' | sed 's/indicationmanager_europe/im_eu/' | sed 's/-/_/g'
im_eu_0_4
im_eu_5_9
im_eu_a_c
im_eu_d_e
im_eu_f_h
im_eu_i_l
im_eu_m_o
im_eu_p_r
im_eu_s_t
im_eu_u_z



darren:
need streamers
Weekends/Bank Holidays (remove)            # need to get trading holidays from somewhere
Consider/handle bad data days from extract process
    (where anomalous data is extracted and is clearly wrong)
Converting to a % utilisation (as per XL sheet)
Annotating graphs to show avg and peak utilisation
US instances need to be included
Possibly outputting to a Confluence page - Nice to have!
Record/extract data for uk2 and va hosts - not urgent as this is DR
'''
