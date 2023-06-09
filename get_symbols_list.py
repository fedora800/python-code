import bs4 as bs
# better was to read table from html could be using pandas - https://techiejackieblogs.com/how-to-get-the-list-of-sp-500-companies-stocks/
# https://tcoil.info/
import requests
import yfinance as yf
import datetime

symbol_file = "sp500_constituents.csv"
quotes_file = "sp500_quotes_data.csv"

# below is causing problems, likely because wikipedia is not liking it, so saving html output to file via browser and then using file
#resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

with open('./wikipedia_sp500_page.html', 'r', encoding='utf-8') as f:
    soup = bs.BeautifulSoup(f, 'html.parser')

# required data in this html block  <table class="wikitable sortable" id="constituents">
table = soup.find('table', {'class': 'wikitable sortable'})

list_symbols = []
for row in table.findAll('tr')[1:]:
    ticker = row.findAll('td')[0].text
    list_symbols.append(ticker)
#print(tickers)
list_symbols = [s.replace('\n', '') for s in list_symbols]
list_symbols.sort()


with open(symbol_file, "w") as f:
    for symbol in list_symbols:
        f.write(symbol + '\n')
print('Created symbol list file = ', symbol_file)

# temporary, to reduce symbols and data lookups for testing
my_temp_filtered_stock_list =  [ symbol for symbol in list_symbols if "RS" in symbol ]

start = datetime.datetime(2023, 1, 1)
end = datetime.datetime(2023, 6, 8)
data = yf.download(my_temp_filtered_stock_list, start=start, end=end)

df = data.stack().reset_index().rename(index=str, columns={"level_1": "Symbol"}).sort_values(['Symbol','Date'])
df.set_index('Date', inplace=True)

df.to_csv(quotes_file)
print('Created quotes data file = ', quotes_file)