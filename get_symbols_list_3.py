import pandas as pd
import ssl

# https://github.com/dataprofessor/code/blob/master/streamlit/part10/sp500-app.py

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

try:
  html = pd.read_html(url, header = 0)
  df = html[0]
  print(df.head())
  df.to_csv("sp500_companies_list.csv", index=False, encoding="utf-8")    # Save to CSV
  print("Data saved to sp500_companies_list.csv")
except Exception as e:
  print(f"Error occurred: {e}")
  df = pd.DataFrame()  # create an empty DataFrame if there's an error

print(df)
#     Symbol              Security             GICS Sector                   GICS Sub-Industry    Headquarters Location  Date added      CIK      Founded

sector_unique = sorted(df['GICS Sector'].unique())
print(sector_unique)
# ['Communication Services', 'Consumer Discretionary', 'Consumer Staples', 'Energy', 'Financials', 'Health Care', 'Industrials', 'Information Technology', 'Materials', 'Real Estate', 'Utilities']

selected_sectors = [ 'Financials', 'Information Technology' ]
df_selected_sectors = df[ (df['GICS Sector'].isin(selected_sectors)) ]
print(df_selected_sectors)

# that git code also contains code to download data
