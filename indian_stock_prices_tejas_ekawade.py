# https://medium.com/@TejasEkawade/getting-indian-stock-prices-using-python-19f8c83d2015

import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from jugaad_data.nse import index_raw

n_years = 3 # Parameter for historical years

def convert_to_date(date_str):
    date_obj = datetime.datetime.strptime(date_str, '%d %b %Y')
    return date_obj

# Get from and to dates
to_date = datetime.date.today()
from_date = to_date - relativedelta(years=n_years)
print(from_date, to_date)

# Fetch the index data 
raw_index_data = index_raw(symbol="NIFTY 50", from_date=from_date, to_date=to_date)

# Converting into dataframe and processing the data
nifty_historical_df = (pd.DataFrame(raw_index_data)\
                            .assign(HistoricalDate=lambda x: x['HistoricalDate'].apply(convert_to_date))\
                            .sort_values('HistoricalDate')\
                            .drop_duplicates()\
                            .loc[lambda x: x['Index Name'] == 'Nifty 50']\
                            .reset_index(drop=True))
nifty_historical_df



