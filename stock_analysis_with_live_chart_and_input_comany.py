import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import requests

st.set_page_config(layout="wide")
st.title("📈 Stock Analysis, Comparison & Live Info")

uploaded_files = st.file_uploader("Upload CSV files of different stocks", type="csv", accept_multiple_files=True)

def generate_website_url(symbol):
    company = symbol.lower().replace(" ", "")
    return f"https://www.{company}.com"

# List to store company names for selecting from uploaded files
company_names = []

if uploaded_files:
    stock_data = {}
    all_columns = []

    for file in uploaded_files:
        # Use file name as symbol (e.g., TCS.csv → TCS)
        symbol = file.name.replace(".csv", "").strip().upper()
        company_names.append(symbol)  # Add company to the list for selection
        try:
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip()

            if 'Date' not in df.columns:
                st.warning(f"No 'Date' column in {symbol}, skipping.")
                continue

            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df.dropna(subset=['Date'], inplace=True)
            df.sort_values('Date', inplace=True)

            # Handle missing 'Close' column
            if 'Close' not in df.columns:
                if 'Last' in df.columns:
                    df['Close'] = df['Last']
                elif 'Prev Close' in df.columns:
                    df['Close'] = df['Prev Close']
                else:
                    df['Close'] = df.select_dtypes(include='number').mean(axis=1)

            df.fillna(method='ffill', inplace=True)
            stock_data[symbol] = df
            all_columns.append(set(df.columns))

        except Exception as e:
            st.error(f"Error processing {symbol}: {e}")

    # 📊 Comparison section
    if stock_data:
        common_cols = sorted(set.intersection(*all_columns)) if all_columns else []
        selected_cols = st.multiselect("📊 Select columns to compare:", common_cols, default=['Close'])

        for col in selected_cols:
            st.markdown(f"## 📌 {col} Comparison")
            fig, ax = plt.subplots(figsize=(12, 6))
            for symbol, df in stock_data.items():
                if col in df.columns:
                    ax.plot(df['Date'], df[col], label=symbol)
            ax.set_title(f"{col} Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel(col)
            ax.legend()
            st.pyplot(fig)

        # 🧾 Individual stock view + Website + TradingView embed
        for symbol, df in stock_data.items():
            st.markdown(f"---\n## 🧾 {symbol} Overview")

            # 🔗 Company Website Link
            website = generate_website_url(symbol)
            st.markdown(f"🌐 [Visit {symbol} Website]({website})")

            # 📊 Plot selected columns
            for col in selected_cols:
                if col in df.columns:
                    st.plotly_chart(px.line(df, x='Date', y=col, title=f"{symbol} - {col}"))

            # 📈 Embed TradingView Live Chart using symbol
            st.markdown("### 📈 Live TradingView Chart")
            st.markdown(f"""
                <iframe 
                    src="https://s.tradingview.com/widgetembed/?symbol={symbol}&interval=D&hidesidetoolbar=1&theme=light"
                    width="100%" height="500" frameborder="0" allowtransparency="true" scrolling="no">
                </iframe>
            """, unsafe_allow_html=True)

    # 🔍 Add input for manually entering a TradingView symbol
    st.markdown("### 🔍 Find Live Chart of any Company")
    manual_symbol = st.text_input("Enter TradingView symbol (e.g., NSE:TCS, NSE:SBIN):")

    if manual_symbol:
        symbol = manual_symbol.strip().upper()

        # Try embedding the chart for the entered symbol
        st.markdown("### 📊 Live Chart for Custom Symbol")
        st.markdown(f"""
        <iframe 
            src="https://s.tradingview.com/widgetembed/?symbol={symbol}&interval=D&hidesidetoolbar=1&theme=light"
            width="100%" height="500" frameborder="0" allowtransparency="true" scrolling="no">
        </iframe>
        """, unsafe_allow_html=True)

else:
    st.info("📤 Please upload one or more stock CSV files to begin.")
