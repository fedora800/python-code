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

# List of tickers
TICKERS = ['NTRS', 'ORCL']

# Select ticker
ticker = st.sidebar.selectbox('Select ticker', sorted(TICKERS), index=0)

st.header(f'{ticker} Stock Price')

df = pd.read_csv('./sp500_quotes_data.csv')
print(df)

fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

fig.update_layout(xaxis_rangeslider_visible=False)
#fig.show()         # this will open another webpage as it's plotly trying to show the chart, which we dont want as streamlit should do it

# Render plot using plotly_chart
st.plotly_chart(fig)
