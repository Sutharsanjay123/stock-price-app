import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Set wide layout and title
st.set_page_config(layout="wide")
st.title("📈 Stock Analysis, Comparison & Live Info")

# Custom dark CSS and background image
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #000000;
        color: #ffffff;
    }

    .stApp {
        background-image: url("https://wallpaperaccess.com/full/1393765.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    .stFileUploader {
        background: rgba(0, 0, 0, 0.6);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.6);
        color: white;
        text-align: center;
    }

    .stFileUploader label {
        color: #00ffff !important;
        font-weight: bold;
    }

    .big-font {
        font-size: 40px !important;
        text-align: center;
        font-weight: bold;
        color: #ffffff;
    }

    a {
        color: #00ffff !important;
    }

    .block-container {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 2rem;
        border-radius: 12px;
    }
    .st-emotion-cache-7czcpc > img {
    max-width: 100%;
    width: 63rem;
    height: 33rem;
    font-size: 2px;
    border-radius: 0.5rem;
}
    </style>
""", unsafe_allow_html=True)

# File uploader
uploaded_files = st.file_uploader("📤 Upload CSV files of different stocks", type="csv", accept_multiple_files=True)

def generate_website_url(symbol):
    return f"https://www.{symbol.lower().replace(' ', '')}.com"

if uploaded_files:
    stock_data = {}
    all_columns = []

    for file in uploaded_files:
        symbol = file.name.replace(".csv", "").strip().upper()
        try:
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip()

            # Check and handle possible date columns
            date_column = None
            for col in df.columns:
                if 'date' in col.lower():
                    date_column = col
                    break

            if date_column is None:
                st.warning(f"⚠️ No date column found in {symbol}, skipping.")
                continue

            df['Date'] = pd.to_datetime(df[date_column], errors='coerce')
            df.dropna(subset=['Date'], inplace=True)
            df.sort_values('Date', inplace=True)

            # Check for stock price column (Close, Last, or Prev Close)
            if 'Close' not in df.columns:
                if 'Last' in df.columns:
                    df['Close'] = df['Last']
                elif 'Prev Close' in df.columns:
                    df['Close'] = df['Prev Close']
                else:
                    df['Close'] = df.select_dtypes(include='number').mean(axis=1)

            df.fillna(method='ffill', inplace=True)
            df.fillna(method='bfill', inplace=True)

            stock_data[symbol] = df
            all_columns.append(set(df.columns))

        except Exception as e:
            st.error(f"❌ Error processing {symbol}: {e}")

    # 📊 Comparison Section
    if stock_data:
        common_cols = sorted(set.intersection(*all_columns)) if all_columns else []
        selected_cols = st.multiselect("📊 Select columns to compare:", common_cols, default=['Close'])

        # Dropdown for selecting the type of graph
        chart_type = st.selectbox("🔳 Select Graph Type", ["Line", "Bar", "Scatter", "Area", "Candlestick"])

        for col in selected_cols:
            st.markdown(f"---\n### 🔍 {col} Comparison Across Stocks")

            # Reduced graph size and adjusted font sizes
            fig, ax = plt.subplots(figsize=(8, 4), facecolor='#000000')  # Smaller size
            ax.set_facecolor('#111111')

            for symbol, df in stock_data.items():
                if col in df.columns:
                    if chart_type == "Line":
                        ax.plot(df['Date'], df[col], label=symbol)
                    elif chart_type == "Bar":
                        ax.bar(df['Date'], df[col], label=symbol)
                    elif chart_type == "Scatter":
                        ax.scatter(df['Date'], df[col], label=symbol)
                    elif chart_type == "Area":
                        ax.fill_between(df['Date'], df[col], label=symbol, alpha=0.5)

            # Adjust title, labels, and font sizes
            ax.set_title(f"{col} Over Time", color='cyan', fontsize=14)
            ax.set_xlabel("Date", color='white', fontsize=10)
            ax.set_ylabel(col, color='white', fontsize=10)
            ax.tick_params(axis='both', colors='white', labelsize=8)
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white') 
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.legend(facecolor='#222222', edgecolor='white', labelcolor='white', fontsize=8)

            st.pyplot(fig)

        # 🧾 Individual Stock Sections
        for symbol, df in stock_data.items():
            st.markdown(f"---\n## 🧾 {symbol} Overview")
            website = generate_website_url(symbol)
            st.markdown(f"🌐 [Visit {symbol} Website]({website})")

            for col in selected_cols:
                if col in df.columns:
                    if chart_type == "Line":
                        fig = px.line(df, x='Date', y=col, title=f"{symbol} - {col} Over Time", template="plotly_dark")
                    elif chart_type == "Bar":
                        fig = px.bar(df, x='Date', y=col, title=f"{symbol} - {col} Over Time", template="plotly_dark")
                    elif chart_type == "Scatter":
                        fig = px.scatter(df, x='Date', y=col, title=f"{symbol} - {col} Over Time", template="plotly_dark")
                    elif chart_type == "Area":
                        fig = px.area(df, x='Date', y=col, title=f"{symbol} - {col} Over Time", template="plotly_dark")
                    elif chart_type == "Candlestick":
                        fig = px.candlestick(df, x='Date', open='Open', high='High', low='Low', close='Close', title=f"{symbol} - {col} Over Time", template="plotly_dark")

                    st.plotly_chart(fig)

            # TradingView Live Chart (dark themed)
            st.markdown("### 📈 Live TradingView Chart")
            st.markdown(f"""
                <iframe 
                    src="https://s.tradingview.com/widgetembed/?symbol={symbol}&interval=D&hidesidetoolbar=1&theme=dark"
                    width="100%" height="500" frameborder="0" allowtransparency="true" scrolling="no">
                </iframe>
            """, unsafe_allow_html=True)

    # 🔍 Manual TradingView Symbol
    st.markdown("---\n### 🔍 Live Chart for Any Company")
    manual_symbol = st.text_input("Enter TradingView symbol (e.g., NSE:TCS, NASDAQ:GOOGL):")

    if manual_symbol:
        symbol = manual_symbol.strip().upper()
        website = generate_website_url(symbol)  # Generate website link for manual symbol
        st.markdown(f"### 📊 Live Chart for `{symbol}`")
        st.markdown(f"🌐 [Visit {symbol} Website]({website})")  # Display company website link
        st.markdown(f"""
        <iframe 
            src="https://s.tradingview.com/widgetembed/?symbol={symbol}&interval=D&hidesidetoolbar=1&theme=dark"
            width="100%" height="500" frameborder="0" allowtransparency="true" scrolling="no">
        </iframe>
        """, unsafe_allow_html=True)

else:
    st.info("📤 Please upload one or more stock CSV files to begin.")
