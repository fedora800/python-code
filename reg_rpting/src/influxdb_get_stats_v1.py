from datetime import datetime

import pandas as pd
import plotly as pl
import plotly.graph_objects as gobj


#from plotly.offline import plot
# INPUT_FILE='C:\\mytmp\\file-downloads\\im_max_count_2020-02-03_fmtd.csv'
#INPUT_FILE = 'C:\\mytmp\\file-downloads\\im_max_count.archive_2020-02-25.prod_archive_fmtd.csv'
INPUT_FILE = 'C:\\mytmp\\influxdb_stats\\IM\\im_max_count_2020-07-16.prod_archive_fmtd.csv'
#INPUT_FILE = 'C:\\mytmp\\file-downloads\\streamer_max_count_2020-03-09.prod_archive_fmtd.csv'
OUTPUT_DIR = 'C:\\mytmp'
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
    print('plotly version=', pl.__version__)


def load_csv_file_into_dataframe():
    """Loads contents of the csv file into a pandas dataframe

    Parameters:
    none

    Returns:
    dataframe

   """
    print("-In load_csv_file_into_dataframe ...")
    print('Loading data from file ', INPUT_FILE)
    print('dateime today=', datetime.today())
    # infer_datetime_format makes it 10x faster
    df_param = pd.read_csv(INPUT_FILE, infer_datetime_format=True,
                           parse_dates=['time'], encoding='UTF-8')
    # data = pd.read_csv(INPUT_FILE)
    # data['time'] = data['time'].astype('datetime64[ns]')
    # print(df_param)
    # print(df_param.info())
    return df_param


def customize_data(df_param):
    """Changes data in the dataframe to our specifications

    Parameters:
    dataframe

    Returns:
    Modified dataframe

   """

    print("-In customize_data ...")
    # create a additional column in the dataframe that will contain the
    # corresponding day of the week
    df_param['day_of_week'] = df_param['time'].dt.dayofweek # Monday is 0 and Sunday is 6
    # remove records for weekend dates from the dataset
    df_param.drop(df_param[df_param['day_of_week'] == 5].index, inplace=True)
    df_param.drop(df_param[df_param['day_of_week'] == 6].index, inplace=True)

    # todo- need to also remove 25-dec and 01-jan data as holidays for all regions -   so wil need to probably define a holiday list
    # remove 26-dec for emea as boxing day ---
    # also there are other bank holidays that need removal from display for
    # EMEA

    # print(df_param)
    print(df_param.info())
    return df_param


def prepare_chart(df_param):
    '''
    uses the pandas dataframe that contains the data
    '''

    print('-In prepare_chart ...')
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
        trace = gobj.Scatter(x=df_for_this_proc['time'],
                             y=df_for_this_proc['max_indication_count'],
                             mode='lines',          # gives us a line chart
                             name=proc_name,        # legend name
                             marker=dict(color=color_palette_list),
                             text=proc_name)        # hover line name
        print('Appending trace to trace_list')
        if ('USA' in proc_name or 'Canada' in proc_name):
            print('---11--- ' + proc_name)
            traces_list_AMER.append(trace)
        elif 'Asia' in proc_name:
            print('---22--- ' + proc_name)
            traces_list_APAC.append(trace)
        elif 'Europe' in proc_name:
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
    output_file = OUTPUT_DIR + '/AMER_Max_Indication_Count.html'
    print('Plotting chart for AMER into file ' + output_file)
    fig = dict(data=traces_list_AMER, layout=layout)
    pl.offline.plot(fig, filename=output_file, auto_open=False)

    output_file = OUTPUT_DIR + '/APAC_Max_Indication_Count.html'
    print('Plotting chart for APAC into file ' + output_file)
    fig = dict(data=traces_list_APAC, layout=layout)
    pl.offline.plot(fig, filename=output_file, auto_open=False)

    output_file = OUTPUT_DIR + '/EMEA_Max_Indication_Count.html'
    print('Plotting chart for EMEA into file ' + output_file)
    # fig = dict(data=traces_list, layout=layout)
    fig = dict(data=traces_list_EMEA, layout=layout)
    # pl.offline.plot(fig)        # will display in browser
    # saves to a file and does not display to browser
    pl.offline.plot(fig, filename=output_file, auto_open=False)
    # todo - need to look at write_html
    # https://plotly.github.io/plotly.py-docs/generated/plotly.io.write_html.html


def main():
    '''
    the main function
    '''
    show_packages_version()
    df_csv = load_csv_file_into_dataframe()
    df_fmtd = customize_data(df_csv)
    prepare_chart(df_fmtd)


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
