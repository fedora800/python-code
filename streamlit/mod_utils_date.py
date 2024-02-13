from dateutil.relativedelta import relativedelta
from loguru import logger


def compute_date_difference(dt_older_date, dt_newer_date):

    # Check if dt_latest_rec_date is a weekend day (Saturday or Sunday)
    is_weekend = dt_older_date.weekday() in [5, 6]

    # Compute the difference in days using dateutil.relativedelta
    delta = relativedelta(dt_newer_date, dt_older_date)
    difference_in_days = delta.days
    print(f"Difference in days between today and {dt_older_date} = {difference_in_days}")

    # Print whether it's a weekend day
    print(f"Date input {dt_older_date} a weekend day!") if is_weekend else None

    logger.info("Argument date = {}, today's date = {}, returning difference in days = {}", dt_older_date, dt_newer_date, difference_in_days)
    # Return the difference in days
    return difference_in_days

