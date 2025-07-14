import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📈 Stock Price Analysis & Comparison App")

uploaded_files = st.file_uploader("Upload CSV files of different stocks", type="csv", accept_multiple_files=True)

if uploaded_files:
    stock_data = {}
    all_columns = []

    # Load data
    for file in uploaded_files:
        ticker = file.name.replace(".csv", "")
        try:
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip()  # Clean column names
            if 'Date' not in df.columns:
                st.warning(f"No 'Date' column in {ticker}, skipping this file.")
                continue

            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df.dropna(subset=['Date'], inplace=True)
            df.sort_values('Date', inplace=True)

            # Fill missing Close using fallback or mean
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

    # Get common columns across all uploaded files
    if stock_data:
        common_cols = sorted(set.intersection(*all_columns)) if all_columns else []
        st.markdown("### 📊 Select columns to compare")
        selected_cols = st.multiselect("Choose columns to display:", common_cols, default=['Close'])

        for col in selected_cols:
            st.markdown(f"## 📌 {col} Comparison")
            fig, ax = plt.subplots(figsize=(12, 6))

            for ticker, df in stock_data.items():
                if col in df.columns:
                    ax.plot(df['Date'], df[col], label=ticker)
            
            ax.set_title(f"Comparison of {col}")
            ax.set_xlabel("Date")
            ax.set_ylabel(col)
            ax.legend()
            st.pyplot(fig)

        st.markdown("---")
        st.markdown("### 🔍 Individual Stock Visuals")
        for ticker, df in stock_data.items():
            st.markdown(f"## {ticker}")
            for col in selected_cols:
                if col in df.columns:
                    st.subheader(f"{ticker} - {col}")
                    st.plotly_chart(px.line(df, x='Date', y=col, title=f"{ticker} - {col}"))

else:
    st.info("Please upload one or more CSV files to begin.")
