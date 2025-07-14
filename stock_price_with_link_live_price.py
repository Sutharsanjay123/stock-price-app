import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import yfinance as yf

st.set_page_config(layout="wide")
st.title("📈 Stock Price Analysis & Comparison App")

uploaded_files = st.file_uploader("Upload CSV files of different stocks", type="csv", accept_multiple_files=True)

# Dictionary to map company/ticker to Yahoo Finance link
company_links = {
    "TCS": "https://finance.yahoo.com/quote/TCS.NS",
    "TATASTEEL": "https://finance.yahoo.com/quote/TATASTEEL.NS",
    "RELIANCE": "https://finance.yahoo.com/quote/RELIANCE.NS",
    "INFY": "https://finance.yahoo.com/quote/INFY.NS",
    "TECHM": "https://finance.yahoo.com/quote/TECHM.NS",
    "TITAN": "https://finance.yahoo.com/quote/TITAN.NS",
    "TATAMOTORS": "https://finance.yahoo.com/quote/TATAMOTORS.NS"
}

if uploaded_files:
    stock_data = {}
    all_columns = []

    for file in uploaded_files:
        ticker = file.name.replace(".csv", "").upper()
        try:
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip()
            if 'Date' not in df.columns:
                st.warning(f"No 'Date' column in {ticker}, skipping.")
                continue

            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df.dropna(subset=['Date'], inplace=True)
            df.sort_values('Date', inplace=True)

            # Fill missing 'Close' column
            if 'Close' not in df.columns:
                if 'Last' in df.columns:
                    df['Close'] = df['Last']
                elif 'Prev Close' in df.columns:
                    df['Close'] = df['Prev Close']
                else:
                    df['Close'] = df.select_dtypes(include='number').mean(axis=1)

            df.fillna(method='ffill', inplace=True)
            stock_data[ticker] = df
            all_columns.append(set(df.columns))

        except Exception as e:
            st.error(f"Error with {file.name}: {str(e)}")

    # Display live price and link to official stock page
    st.markdown("## 🔗 Live Stock Prices & Links")
    for ticker in stock_data.keys():
        try:
            live_data = yf.Ticker(f"{ticker}.NS").history(period="1d")
            current_price = live_data['Close'].iloc[-1] if not live_data.empty else "N/A"
            st.markdown(f"**{ticker}** - Current Price: ₹{current_price:.2f} &nbsp; | &nbsp; [View Live ↗]({company_links.get(ticker, 'https://www.google.com/search?q=' + ticker + '+stock')})")
        except:
            st.warning(f"Couldn't fetch live data for {ticker}")

    # Column selection and plotting
    if stock_data:
        common_cols = sorted(set.intersection(*all_columns)) if all_columns else []
        st.markdown("## 📊 Select Columns to Compare")
        selected_cols = st.multiselect("Choose columns:", common_cols, default=['Close'])

        for col in selected_cols:
            st.markdown(f"### 📌 {col} Comparison")
            fig, ax = plt.subplots(figsize=(12, 6))

            for ticker, df in stock_data.items():
                if col in df.columns:
                    ax.plot(df['Date'], df[col], label=ticker)
            ax.set_title(f"{col} Comparison")
            ax.set_xlabel("Date")
            ax.set_ylabel(col)
            ax.legend()
            st.pyplot(fig)

        st.markdown("---")
        st.markdown("## 🔍 Individual Stock Visuals")
        for ticker, df in stock_data.items():
            st.markdown(f"### {ticker}")
            for col in selected_cols:
                if col in df.columns:
                    st.subheader(f"{ticker} - {col}")
                    st.plotly_chart(px.line(df, x='Date', y=col, title=f"{ticker} - {col}"))

else:
    st.info("Upload one or more stock CSV files to begin.")
