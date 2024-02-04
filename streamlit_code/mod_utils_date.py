from datetime import datetime, time, timedelta
from dateutil.relativedelta import relativedelta
from loguru import logger


def compute_date_difference(dt_older_date, dt_newer_date, type_of_days="CALENDAR"):
  """_summary_
  valid values are WORKING or CALENDAR

  Args:
      dt_older_date (_type_): _description_
      dt_newer_date (_type_): _description_
      type_of_days (str, optional): _description_. Defaults to "calendar".

  Returns:
      _type_: _description_
  """

  logger.debug("Received arguments : dt_older_date={} dt_newer_date={} type_of_days={}", dt_older_date, dt_newer_date, type_of_days)
  
  # Compute the difference in calendar days
  delta = relativedelta(dt_newer_date, dt_older_date)
  difference_in_days_cal = delta.days
  logger.debug("Difference in calendar days between {} and {} = {}", dt_older_date, dt_newer_date, difference_in_days_cal)

  # Calculate the difference in working days
  if type_of_days == "WORKING":
    working_days = 0
    current_date = dt_older_date
    while current_date < dt_newer_date:
        if current_date.weekday() not in [5, 6]:  # Exclude Saturday and Sunday from the days count
            working_days += 1
        current_date += timedelta(days=1)
    difference_in_days_wrk = working_days
    logger.debug("Difference in working days between {} and {} = {}", dt_older_date, dt_newer_date, difference_in_days_wrk)

  # Return the difference in days
  if type_of_days == "WORKING":
    return difference_in_days_wrk
  else:
    return difference_in_days_cal



def get_date_with_zero_time(dt_datetime):
  """
  Clear out the time component of any time and just return the datetime object with only the date.
  Time component will be there but will be 00:00:00
  """

  dt_date = datetime.combine(dt_datetime, time())
  return dt_date


def get_info_about_date(dt_date):

  # Check if dt_latest_rec_date is a weekend day (Saturday or Sunday)
  is_weekend = dt_date.weekday() in [5, 6]
  # Print whether it's a weekend day
  print(f"Date input {dt_date} a weekend day!") if is_weekend else None
