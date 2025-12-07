from fastapi import FastAPI, Request
import uvicorn
import json
#from model_loader import model
import tensorflow as tf
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

app = FastAPI()

# Load Model
model = tf.keras.models.load_model("model/stock_model.h5")

# Globals to store latest price and prediction
latest_close = None
latest_prediction = None

#Prediction function
def predict_price(price):
    x = np.array([[price]]).reshape((1, 1, 1))  # 3D input for LSTM
    prediction = model.predict(x)[0][0]
    return prediction


# Function to fetch latest close from yfinance
def fetch_latest_close(ticker="AAPL"):
    global latest_close, latest_prediction
    end_date = datetime.today()
    start_date = end_date - timedelta(days=7)  # buffer for weekends/holidays

    data = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    if data.empty:
        print("No data fetched.")
        return

    latest_close = data['Close'].iloc[-1]
    latest_prediction = predict_price(latest_close)
    print(f"[{datetime.now()}] Latest close: {latest_close}, Prediction: {latest_prediction}")

@app.get("/")
def home():
    return {"status": "OK", "message": "LSTM Webhook API is running"}

# Endpoint to get latest prediction
@app.get("/latest")
def get_latest():
    if latest_close is None:
        return {"error": "Data not available yet"}
    return {
        "latest_close": float(latest_close),
        "model_prediction": float(latest_prediction),
        "signal": "BUY" if latest_prediction > latest_close else "SELL"
    }

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    print("Received Webhook Data:", data)

    # Example: expecting price in JSON: {"price": 123.45}
    price = float(data.get("price", 0))

    # Model expects 3D input: (batch, timesteps, features)
    x = np.array([[price]]).reshape((1, 1, 1))
    prediction = model.predict(x)[0][0]

    print("Model prediction:", prediction)

    return {
        "received": data,
        "model_prediction": float(prediction),
        "signal": "BUY" if prediction > price else "SELL"
    }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)


