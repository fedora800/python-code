import pandas as pd
# https://github.com/dataprofessor/code/blob/master/streamlit/part10/sp500-app.py

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

html = pd.read_html(url, header = 0)
df = html[0]
print(df)
#     Symbol              Security             GICS Sector                   GICS Sub-Industry    Headquarters Location  Date added      CIK      Founded

sector_unique = sorted(df['GICS Sector'].unique())
print(sector_unique)
# ['Communication Services', 'Consumer Discretionary', 'Consumer Staples', 'Energy', 'Financials', 'Health Care', 'Industrials', 'Information Technology', 'Materials', 'Real Estate', 'Utilities']

selected_sectors = [ 'Financials', 'Information Technology' ]
df_selected_sectors = df[ (df['GICS Sector'].isin(selected_sectors)) ]
print(df_selected_sectors)

# that git code also contains code to download data

