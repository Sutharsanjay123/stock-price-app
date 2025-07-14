# 📈 Stock Price Analysis, Comparison & Live Info App

A visually rich and interactive **Streamlit web app** for analyzing, comparing, and visualizing stock prices from uploaded CSV files. Includes **live TradingView charts**, **custom theming**, and **multi-stock comparison tools**.

---

## 🚀 Features

- 📤 Upload multiple stock CSV files (custom or from NSE/BSE/NASDAQ)
- 📊 Compare metrics like `Close`, `Last`, `Prev Close` across stocks
- 📈 Plot interactive graphs using `Plotly` and `Matplotlib`
- 🌐 Embedded **live charts** from [TradingView](https://tradingview.com)
- 🎨 Dark mode UI with elegant background and fonts
- 🔍 Manual TradingView input for any global stock symbol

---

## 📦 Tech Stack

- [Streamlit](https://streamlit.io/) – Web UI
- [Pandas](https://pandas.pydata.org/) – Data Processing
- [Plotly](https://plotly.com/python/) – Interactive Graphs
- [Matplotlib](https://matplotlib.org/) – Static Comparison Charts
- [TradingView](https://tradingview.com/) – Real-Time Charts (Embedded)

---

## 📁 How to Use

 1. Clone the Repository
git clone https://github.com/Sutharsanjay123/stock-price-app.git
cd stock-price-app
2. Install Requirements
pip install -r requirements.txt
If requirements.txt is missing, install manually:
pip install streamlit pandas plotly matplotlib
3. Run the App
streamlit run stock_stream_app.py

---
## 📂 CSV Format Expected
Each CSV should contain at least the following:
Date (YYYY-MM-DD or similar)
One of: Close, Last, or Prev Close
Optional: Open, High, Low, Volume
---

## 🌐 Live Chart Examples
You can enter these symbols to test live TradingView charts:
NSE:TCS
NASDAQ:AAPL
BSE:RELIANCE
NYSE:TSLA
---
## 📸 UI Preview
<img width="1897" height="586" alt="Screenshot 2025-07-14 234602" src="https://github.com/user-attachments/assets/750ad207-c2d3-403a-9132-386a1841c7fe" />

---
## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first.
---
## 🙋‍♂️ Author
Suthar Sanjay
📧 sutharsanjay123@example.com
🔗 GitHub

