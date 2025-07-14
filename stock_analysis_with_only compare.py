import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt

# Set page layout to wide
st.set_page_config(layout="wide")
st.title("Stock Price Analysis & Prediction")

# 1. Upload CSVs
uploaded_files = st.file_uploader("Upload multiple stock CSVs", type="csv", accept_multiple_files=True)

if uploaded_files:
    all_stocks_df = []

    # Store tickers for easy reference
    tickers = []

    # Iterate through the uploaded files
    for file in uploaded_files:
        st.markdown("---")
        ticker = file.name.replace(".csv", "")
        tickers.append(ticker)
        st.header(f"Stock: {ticker}")

        try:
            # Read the file into a DataFrame
            df = pd.read_csv(file)

            # Clean column names (remove extra spaces or characters)
            df.columns = df.columns.str.strip()

            # If the 'Date' column is missing, assume the index as date
            if 'Date' not in df.columns:
                st.warning(f"Missing 'Date' column in {file.name}. Using index as 'Date'.")
                df['Date'] = pd.to_datetime(df.index)  # Assuming index as date if 'Date' is missing
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

            # Append to a list of all stocks for comparison
            all_stocks_df.append(df)

        except pd.errors.EmptyDataError:
            st.error(f"The file {file.name} is empty. Please upload a valid file.")
        except Exception as e:
            st.error(f"An error occurred while processing {file.name}: {str(e)}")

    # 2. Select columns for comparison
    column_options = ['Prev Close', 'Open', 'High', 'Low', 'Last', 'Close', 'VWAP', 'Volume', 'Turnover', 'Trades', 'Deliverable Volume', '%Deliverble']
    selected_columns = st.multiselect("Select the data to compare:", column_options, default=['Close', 'Volume'])

    # 3. Plot selected columns for each stock
    for i, df in enumerate(all_stocks_df):
        ticker = tickers[i]
        st.markdown(f"### {ticker} - Selected Data")

        # Filter and show selected columns
        for col in selected_columns:
            if col in df.columns:
                st.subheader(f"{ticker} - {col}")
                st.plotly_chart(px.line(df, x='Date', y=col, title=f"{ticker} {col}"))
            else:
                st.warning(f"Column '{col}' not found in {ticker}. Skipping.")

    # 4. Compare All Stocks Based on Selected Columns
    st.markdown("## Comparison of All Uploaded Stocks Based on Selected Columns")

    for col in selected_columns:
        st.subheader(f"Comparison of {col} for All Stocks")
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for i, df in enumerate(all_stocks_df):
            ticker = tickers[i]
            if col in df.columns:
                ax.plot(df['Date'], df[col], label=ticker)
        
        ax.set_xlabel('Date')
        ax.set_ylabel(col)
        ax.set_title(f"Comparison of {col} Across All Stocks")
        ax.legend()
        st.pyplot(fig)
