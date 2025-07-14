import streamlit as st
import pandas as pd
import plotly.express as px
from prophet import Prophet
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Stock Price Analysis & Prediction")

# 1. Upload CSVs
uploaded_files = st.file_uploader("Upload multiple stock CSVs", type="csv", accept_multiple_files=True)

if uploaded_files:
    best_stock = None
    best_stock_return = -np.inf
    best_stock_ticker = ""

    all_stocks_df = []
    stock_prices = []
    stock_returns = []

    for file in uploaded_files:
        st.markdown("---")
        ticker = file.name.replace(".csv", "")
        st.header(f"Stock: {ticker}")

        try:
            # Read the file into a DataFrame
            df = pd.read_csv(file)

            # If the DataFrame is empty, skip it and show a message
            if df.empty:
                st.error(f"The file {file.name} is empty. Please upload a valid file.")
                continue

            # Clean column names (remove extra spaces or characters)
            df.columns = df.columns.str.strip()

            # If the 'Date' column is missing, assume the index as date
            if 'Date' not in df.columns:
                st.warning(f"Missing 'Date' column in {file.name}. Using index as 'Date'.")
                df['Date'] = pd.to_datetime(df.index)  # Assuming index as a date if 'Date' is missing
            else:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

            # If the 'Close' column is missing, assume 'Last' or fill with mean value
            if 'Close' not in df.columns:
                st.warning(f"Missing 'Close' column in {file.name}. Using 'Last' column instead.")
                if 'Last' in df.columns:
                    df['Close'] = df['Last']
                else:
                    # Fill missing Close column with the mean value
                    df['Close'] = df['Close'].fillna(df['Close'].mean())
            else:
                df['Close'] = df['Close'].fillna(df['Close'].mean())  # Fill missing Close with mean

            # Sort by Date
            df.sort_values('Date', inplace=True)

            # 2. Plot raw closing prices
            st.subheader("Closing Price Over Time")
            st.plotly_chart(px.line(df, x='Date', y='Close', title=f"{ticker} Close Price"))

            # 3. Returns and Volatility
            df['Returns'] = df['Close'].pct_change()
            df['Volatility'] = df['Close'].rolling(window=20).std()

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Returns")
                st.plotly_chart(px.line(df, x='Date', y='Returns'))

            with col2:
                st.subheader("Volatility (20-day)")
                st.plotly_chart(px.line(df, x='Date', y='Volatility'))

            # Calculate the average return
            stock_return = df['Returns'].mean()
            stock_prices.append(df['Close'].iloc[-1])  # Latest closing price
            stock_returns.append(stock_return)

            # Determine the best stock based on returns and price
            if stock_return > best_stock_return:
                best_stock_return = stock_return
                best_stock_ticker = ticker
                best_stock = df

            # Append to a list of all stocks for comparison
            all_stocks_df.append(df)

        except pd.errors.EmptyDataError:
            st.error(f"The file {file.name} is empty. Please upload a valid file.")
        except Exception as e:
            st.error(f"An error occurred while processing {file.name}: {str(e)}")

    # 4. Price Forecasting using Prophet for the best stock
    if best_stock is not None:
        st.subheader(f"Price Prediction (Prophet) for Best Stock: {best_stock_ticker}")
        prophet_df = best_stock[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
        model = Prophet()
        model.fit(prophet_df)
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)
        fig1 = model.plot(forecast)
        st.plotly_chart(fig1)

    # 5. Compare All Stocks based on Price and Returns
    st.markdown("## Comparison of All Uploaded Stocks Based on Price and Returns")

    # Plot the latest price of each stock
    st.subheader("Latest Stock Prices")
    price_df = pd.DataFrame({
        "Stock": [file.name.replace('.csv', '') for file in uploaded_files],
        "Price": stock_prices
    })
    st.bar_chart(price_df.set_index('Stock'))

    # Plot the average returns of each stock
    st.subheader("Average Returns of Each Stock")
    returns_df = pd.DataFrame({
        "Stock": [file.name.replace('.csv', '') for file in uploaded_files],
        "Average Return": stock_returns
    })
    st.bar_chart(returns_df.set_index('Stock'))

    # Final comparison graph based on price and return
    st.subheader("Price vs Returns Comparison")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(price_df['Price'], returns_df['Average Return'], color='blue')

    for i, txt in enumerate(price_df['Stock']):
        ax.annotate(txt, (price_df['Price'][i], returns_df['Average Return'][i]))

    ax.set_xlabel('Stock Price')
    ax.set_ylabel('Average Return')
    ax.set_title('Stock Price vs Average Return')
    st.pyplot(fig)

    # 6. Column Selection for Dynamic Graphs
    st.markdown("## Select Columns to Display in the Graph")
    column_options = ['Closing Price', 'Returns', 'Volatility']
    selected_columns = st.multiselect("Select the data to compare:", column_options)

    for file in uploaded_files:
        ticker = file.name.replace(".csv", "")
        st.markdown(f"### {ticker}")

        df = pd.read_csv(file)

        # If the DataFrame is empty, skip it and show a message
        if df.empty:
            st.error(f"The file {file.name} is empty. Please upload a valid file.")
            continue

        # Clean column names (remove extra spaces or characters)
        df.columns = df.columns.str.strip()

        # If the 'Date' column is missing, assume the index as date
        if 'Date' not in df.columns:
            df['Date'] = pd.to_datetime(df.index)
        else:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Fill missing data (if any) for columns like 'Close', 'Returns', 'Volatility'
        if 'Close' not in df.columns:
            df['Close'] = df['Last']
        df['Returns'] = df['Close'].pct_change()
        df['Volatility'] = df['Close'].rolling(window=20).std()

        # Filter and show selected columns
        if 'Closing Price' in selected_columns:
            st.subheader(f"{ticker} - Closing Price")
            st.plotly_chart(px.line(df, x='Date', y='Close', title=f"{ticker} Close Price"))
        if 'Returns' in selected_columns:
            st.subheader(f"{ticker} - Returns")
            st.plotly_chart(px.line(df, x='Date', y='Returns', title=f"{ticker} Returns"))
        if 'Volatility' in selected_columns:
            st.subheader(f"{ticker} - Volatility")
            st.plotly_chart(px.line(df, x='Date', y='Volatility', title=f"{ticker} Volatility"))
