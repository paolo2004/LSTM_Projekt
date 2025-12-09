import streamlit as st
import tensorflow as tf
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

# Load model
model = tf.keras.models.load_model("model/stock_model.h5")

#Background_color
st.markdown("""
    <style>
    .stApp {
        background-color: aliceBlue;
    }
    </style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="Stock Price Predictor", layout="centered")

st.title("📈 Stock Price Predictor ")

# USER INPUT
ticker = st.text_input("Enter Stock Ticker (e.g. AAPL, TSLA, GOOGL)")
lookback_days = st.slider("Lookback Days", 3, 30, 7)

# Fetch stock data
def fetch_latest_close(ticker):
    return yf.download(ticker, period='1d', interval='30m', auto_adjust=False)

# NEWS BUTTON
if st.button("Show News"):
    if ticker == "":
        st.warning("Please enter a stock ticker.")
    else:
        try:
            stock = yf.Ticker(ticker)
            news = stock.news

            if not news or len(news) == 0:
                st.error("No news data available.")
            else:
                st.subheader("News Data")
                for item in news:
                    st.write("### " + item.get("title", "No title"))
                    st.write(item.get("publisher", "Unknown source"))
                    st.write(item.get("link", ""))
                    st.write("---")

        except Exception as e:
            st.error(f"Error fetching news: {e}")



# PREDICTION BUTTON
if st.button("Predict Price"):
    if ticker == "":
        st.warning("Please enter a stock ticker.")
    else:
        data = fetch_latest_close(ticker)

        if data.empty:
            st.error("No data found for this ticker.")
        else:
            latest_close = data["Close"].iloc[-1]

            # Model expects 3D shape for LSTM
            x = np.array([[latest_close]]).reshape((1, 1, 1))

            # Predict
            prediction = model.predict(x)[0][0]

            # OUTPUT
            st.subheader("Results")
            st.write(f"**Ticker:** {ticker.upper()}")
            st.write(f"**Latest Close Price:** ${float(latest_close):.2f}")
            st.write(f"**Predicted Price:** ${float(prediction):.2f}")

            signal = "📈 BUY" if prediction > latest_close else "📉 SELL"
            st.write(f"**Signal:** {signal}")

            # Show recent data
            st.subheader("Recent Price Data")
            st.dataframe(data.tail())
