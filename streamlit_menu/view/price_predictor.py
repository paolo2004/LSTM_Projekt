import yfinance as yf
import streamlit as st
import tensorflow as tf
import numpy as np

# Load model
model = tf.keras.models.load_model("model/stock_model.h5")

#st.title("Stock Price Predictor")

st.set_page_config(page_title="Stock Price Predictor", layout="centered")

st.title("📈 Stock Price Predictor ")

# USER INPUT
ticker = st.text_input("Enter Stock Ticker (e.g. AAPL, TSLA, GOOGL)")
lookback_days = st.slider("Lookback Days", 3, 30, 7)

# Fetch stock data
def fetch_latest_close(ticker):
    return yf.download(ticker, period='1d', interval='30m', auto_adjust=False)

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
