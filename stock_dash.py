!pip install yfinance
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import requests
from PIL import Image
from io import BytesIO

# Function to get stock data
def get_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    return stock.history(start=start_date, end=end_date)

# Function to plot stock data with moving averages
def plot_stock_data(df, ticker):
    plt.figure(figsize=(10, 6))
    plt.plot(df['Close'], label=f'{ticker} Close Price')
    plt.plot(df['Close'].rolling(window=50).mean(), label='50-Day MA')
    plt.plot(df['Close'].rolling(window=200).mean(), label='200-Day MA')
    plt.title(f'Stock Price and Moving Averages: {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# Function to fetch financial ratios
def fetch_financial_ratios(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    ratios = {
        "P/E Ratio": info.get('trailingPE', 'N/A'),
        "Dividend Yield": info.get('dividendYield', 'N/A') * 100 if info.get('dividendYield') else 'N/A',
        "EPS": info.get('trailingEps', 'N/A'),
        "P/B Ratio": info.get('priceToBook', 'N/A'),
        "P/S Ratio": info.get('priceToSalesTrailing12Months', 'N/A'),
        "ROE": info.get('returnOnEquity', 'N/A'),
        "Debt-to-Equity Ratio": info.get('debtToEquity', 'N/A'),
        "Market Cap": info.get('marketCap', 'N/A'),
        "Beta": info.get('beta', 'N/A')
    }
    return ratios

# Function to fetch and display the company logo
# def display_company_logo(ticker):
#     stock = yf.Ticker(ticker)
#     logo_url = stock.info.get('logo_url')
#     if logo_url:
#         response = requests.get(logo_url)
#         img = Image.open(BytesIO(response.content))
#         st.image(img, width=50)

st.title('Interactive Stock Dashboard')

# User input for selecting stocks and date ranges
tickers = st.text_input('Enter stock ticker symbols (comma separated)', 'AAPL, MSFT')
start_date = st.date_input('Start Date', value=pd.to_datetime('2020-01-01'))
end_date = st.date_input('End Date', value=pd.to_datetime('today'))

if st.button('Show Data'):
    ticker_list = [ticker.strip().upper() for ticker in tickers.split(',')]

    # Create a DataFrame to store financial ratios
    ratios_df = pd.DataFrame()

    for ticker in ticker_list:
        st.write(f'## {ticker} Stock Data')
        #display_company_logo(ticker)  # Display the company logo
        df = get_stock_data(ticker, start_date, end_date)
        st.line_chart(df['Close'])
        plot_stock_data(df, ticker)

        # st.write(f'## {ticker} Financial Ratios')
        ratios = fetch_financial_ratios(ticker)
        ratios_df[ticker] = pd.Series(ratios)

    # Display the financial ratios comparison table
    st.write('## Financial Ratios Comparison')
    st.dataframe(ratios_df)

    if len(ticker_list) > 1:
        st.write('## Compare Stocks')
        for ticker in ticker_list:
            df = get_stock_data(ticker, start_date, end_date)
            st.line_chart(df['Close'], width=0, height=0, use_container_width=True)
