# version 20220308
from datetime import datetime
from numpy import uint32
from tzlocal import get_localzone
import pytz
from pytz import timezone, all_timezones
# http://pytz.sourceforge.net/
# https://medium.com/@eleroy/10-things-you-need-to-know-about-date-and-time-in-python-with-datetime-pytz-dateutil-timedelta-309bfbafb3f7
# https://www.saltycrane.com/blog/2009/05/converting-time-zones-datetime-objects-python/
# https://pypi.org/project/pytz/

DT_OUTPUT_FMT = "%Y-%m-%d %H:%M:%S.%f %Z%z"


def get_all_timezones():
    '''
    lists all the timezones available in all_timezones list in pyzt module
    '''
    print('Total number of timezones in all_timezones = ', len(all_timezones))
    for zone in all_timezones:
        #if 'US' in zone:
        #if 'Europe' in zone:
        if 'Asia/Ko' in zone:
            print(zone)


def get_current_local_timezone():
    '''
    gets the current local timezone using tzlocal module
    '''
    # get local timezone and local time
    local_tz = get_localzone()
    dt_now_local = datetime.now()
    print('My local timezone=', local_tz)
    print('Current local datetime (naive; no tz) =', dt_now_local.strftime(DT_OUTPUT_FMT))
    print('Current local datetime in local timezone =', dt_now_local.astimezone(local_tz), '\t', dt_now_local.astimezone(local_tz).strftime(DT_OUTPUT_FMT))


def get_country_from_timezones():
    '''
    Print the country name with country code in each line
    using for loop
    '''
    print('pytz.country_names = ')
    for key, val in pytz.country_names.items():
        if 'In' in val:
            print(val, key)

    # Print the country name of the particular country code
    print('\nCountry name based on country code(JP):', pytz.country_names['JP'])


def get_current_time_in_utc():
    '''
    Gets current time on the host in UTC timezone
    '''
    dt_now_utc = datetime.now(timezone('UTC'))
    print('current utc time=', dt_now_utc.strftime(DT_OUTPUT_FMT))


def convert_datetime_to_diff_timezone():
    '''
    Change datetime to the required timezones
    '''
    dt_now_utc = datetime.now(timezone('UTC'))
    print('current utc time=', dt_now_utc.strftime(DT_OUTPUT_FMT))
    # Convert to US/Pacific time zone
    dt_now_pacific = dt_now_utc.astimezone(timezone('US/Pacific'))
    print('converted utc date into PST date=', dt_now_pacific.strftime(DT_OUTPUT_FMT))
    # Convert to Europe/Berlin time zone
    dt_now_berlin = dt_now_pacific.astimezone(timezone('Europe/Berlin'))
    print('converted utc date into CET date=', dt_now_berlin.strftime(DT_OUTPUT_FMT))
    # Convert to India time zone
    dt_now_kolkata = dt_now_pacific.astimezone(timezone('Asia/Kolkata'))
    print('converted utc date into IST date=', dt_now_kolkata.strftime(DT_OUTPUT_FMT))


def convert_datetime_to_diff_timezone_using_pytz_timezone():
    '''
    Change datetime to the required timezones using the pytz objects and functions - timezone, localize(), astimezone()
    '''
    # Retrieve the current date
    dt_now = datetime.now()
    # Print the current data and time
    print('dt_now (NO timezone info) = ', dt_now)

    # Create a timezone variable and set it to US/Eastern
    pytz_current = pytz.timezone('US/Eastern')
    print('Timezone variable to be applied to dt_now : ', pytz_current)
    # localize() method is used to localize a naive datetime (ie datetime with no timezone information)
    # Apply our pre-defined timezone to the naive datetime variable so that it now has a timezone component.
    dt_now_with_new_tz = pytz_current.localize(dt_now)
    print('dt_now with the applied timezone = ', dt_now_with_new_tz, '\t\t', dt_now_with_new_tz.strftime(DT_OUTPUT_FMT))

    # Create another timezone variable and set it to Asia/Hong_Kong
    pytz_new = pytz.timezone('Asia/Hong_Kong')
    print('A new timezone variable to override exisiting timezone on dt_now : ', pytz_new)
    # Use the astimezone() method to convert an existing localized time to the one we specify
    # Apply our new timezone to the localized datetime variable so that it gets set with a different timezone component.
    dt_now_with_new_tz_2 = dt_now.astimezone(pytz_new)
    print('dt_now with the new changed timezone : ', dt_now_with_new_tz_2, '\t\t', dt_now_with_new_tz_2.strftime(DT_OUTPUT_FMT))

    # Read the datetime of the specified timezone
    print('Current datetime using the EST timezone variable : ', datetime.now(tz=pytz_current))
    print('Current datetime using the HKT timezone variable : ', datetime.now(tz=pytz_new))


def convert_epoch_to_datetime():
    '''
    Converts different formats of epoch / posix unix times to datetimestamp objects
    Epoch time - the number of SECONDS that have elapsed since the Unix epoch, excluding leap seconds. The Unix epoch is 00:00:00 UTC on 1 January 1970.
    Standard format is 10 chars - eg. 1612345678 which is February 3, 2021 9:47:58 UTC
    Milliseconds format is 13 chars - eg 1612345678012 which February 3, 2021 9:47:58.012 UTC
    '''

    epoch_fmt_1 = '1612345678'
    epoch_fmt_2 = '1612345678012'
    # seen below from redline, here we can just take the 1st 13 chars which is millisecond granularity, 
    # following 6 chars looks like the same milliseconds in human-readable format
    epoch_fmt_3 = '1612345678012012000' 

    dt_1 = datetime.fromtimestamp(int(epoch_fmt_1))
    print(epoch_fmt_1, ' converts to ', dt_1.strftime(DT_OUTPUT_FMT))
    dt_2 = datetime.fromtimestamp(float(int(epoch_fmt_2) / 1000.0))
    print(epoch_fmt_2, ' converts to ', dt_2.strftime(DT_OUTPUT_FMT))
    dt_3 = datetime.fromtimestamp(float(epoch_fmt_3[0:10] + '.' + epoch_fmt_3[13:]))    # 1612345678012012000 becomes 1612345678.012000 which is a timestamp object format
    print(epoch_fmt_3, ' converts to ', dt_3.strftime(DT_OUTPUT_FMT))


def convert_datetime_to_epoch():

    timestamp = datetime.now().timestamp()          # eg format = 1646742802.432567
    print("current epoch as a timestamp object :", timestamp)
    print("current epoch in millisecond format :",round(timestamp*1000))


def convert_string_to_datetime():
    '''
    Converts user input string to a datetime or timestamp object
    '''

    inp_date_str = '2021-02-03 09:47:58.123'
    inp_date_str_2 = '2012-10-12T19:30:00'

    inp_date_dt = datetime.strptime(inp_date_str, '%Y-%m-%d %H:%M:%S.%f')
    print('Datetimestamp obj from inp_date_str =', inp_date_dt, ' dt-timestamp=', inp_date_dt.timestamp(), ' dt-tz=', inp_date_dt.tzname())

    hk_tz = timezone('Asia/Hong_Kong')
    hk_dt = inp_date_dt.astimezone(hk_tz)
    print('Mapped to Hong Kong TZ, it becomes', hk_dt, ' hk-timestamp=', hk_dt.timestamp(), ' hk-tz=', hk_dt.tzname(), ' hk-offset=', hk_dt.tzinfo.utcoffset(hk_dt))

    
    inp_date_dt_2 = datetime.strptime(inp_date_str_2, '%Y-%m-%dT%H:%M:%S').astimezone(timezone('Europe/London'))
    print('\nDatetimestamp obj from inp_date_str_2 =', inp_date_dt_2, ' dt-timestamp=', inp_date_dt_2.timestamp(), ' dt-tz=', inp_date_dt_2.tzname())
    print('inp_date_str_2 but in different format = ', inp_date_dt_2.strftime(DT_OUTPUT_FMT))
    print('UTC conversion of inp_date_str_2 = ', inp_date_dt_2.astimezone(timezone('UTC')))
    tmp_dt = inp_date_dt_2.astimezone(timezone('Europe/Madrid'))
    print('inp_date_str_2 in Europe/Madrid timezone = ', tmp_dt)


def main():
    '''
    the main function
    '''
    #get_all_timezones()
    #get_current_local_timezone()
    #get_country_from_timezones()
    #get_current_time_in_utc()
    #convert_datetime_to_diff_timezone()
    #convert_datetime_to_diff_timezone_using_pytz_timezone()
    #convert_epoch_to_datetime()
    #convert_datetime_to_epoch()
    convert_string_to_datetime()

if __name__ == '__main__':
    main()