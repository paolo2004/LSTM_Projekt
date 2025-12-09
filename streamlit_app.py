import streamlit as st
import tensorflow as tf
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

# Load model
model = tf.keras.models.load_model("model/stock_model.h5")

#Background_image
def set_bg_from_url():
    st.markdown(
        f""""
       <style>
       .stApp{{
       background:
       url("https://www.bing.com/images/search?view=detailV2&ccid=AgtIrwe9&id=EB4CF5FF9B3F527D7750B3DC527D4873265DDAD1&thid=OIP.AgtIrwe9HwqjbKdOY8Z4eAHaE8&mediaurl=https%3a%2f%2fmedia.gettyimages.com%2fid%2f1317587887%2fphoto%2ftrading-charts-on-a-display.jpg%3fs%3d612x612%26w%3dgi%26k%3d20%26c%3d-1OWpoM21zE_Rn0c-MZpnyZTJt-C6Y489wefF1jh_Vw%3d&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.020b48af07bd1f0aa36ca74e63c67878%3frik%3d0dpdJnNIfVLcsw%26pid%3dImgRaw%26r%3d0&exph=408&expw=612&q=trading+images&FORM=IRPRST&ck=577545C822EEE3C6BC208F970835FBB4&selectedIndex=4&itb=0");
       background-size: cover;
       }}
       </style>
       """,
        unsafe_allow_html=True,
    )
set_bg_from_url()

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
        stock = yf.Ticker(ticker)
        new = stock.news
        if new.empty:
            st.error("No news data available.")
        else:
            #Output
            st.subheader("News Data")
            print(new)
            st.write(new)

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
