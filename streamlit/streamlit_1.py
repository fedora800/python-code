# https://plotly.com/python/candlestick-charts/

import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import streamlit as st

APP_NAME = "Stock App!"

# Page Configuration
st.set_page_config(
    page_title=APP_NAME,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add some markdown
st.sidebar.markdown("Made with love using [Streamlit](https://streamlit.io/).")
st.sidebar.markdown("# :chart_with_upwards_trend:")

# Add app title
st.sidebar.title(APP_NAME)

# Set start and end point to fetch data
#start_date = st.sidebar.date_input('Start date', datetime(2023, 1, 1))
#end_date = st.sidebar.date_input('End date', datetime.now().date())

# Read the csv prices file into dataframe
df = pd.read_csv('./../sp500_quotes_data.csv')
print(df)

# List of tickers
#TICKERS = ['NTRS', 'ORCL']
TICKERS = ['ENPH', 'GEN']

# Select ticker
ticker = st.sidebar.selectbox('Select ticker', sorted(TICKERS), index=0)
print("Ticker selected = ", ticker)

st.header(f'{ticker} Stock Price')
#df_symbol = df.loc[df['Symbol'] == ticker]
df_symbol = df[df['Symbol'] == ticker]
print("Symbol dataframe = ", df_symbol)

fig = go.Figure(data=[go.Candlestick(x=df_symbol['Date'],
                open=df_symbol['Open'],
                high=df_symbol['High'],
                low=df_symbol['Low'],
                close=df_symbol['Close'])])

fig.update_layout(xaxis_rangeslider_visible=False)
#fig.show()         # this will open another webpage as it's plotly trying to show the chart, which we dont want as streamlit should do it

# Render plot using plotly_chart
st.plotly_chart(fig)



# --- below worked when i ran on acloudguru aws VPS and was able to access via browser from my PC ---
#  sudo ufw allow 8000/tcp comment 'My Web Server Port'
#  streamlit run streamlit_1.py --server.port 8000
# but access can take time/be flaky. i saw that via IP:port it was not accessible during some times, but via fqdns and port it was ...




