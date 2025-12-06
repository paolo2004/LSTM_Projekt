from fastapi import FastAPI, Request
import uvicorn
import json
#from model_loader import model
import tensorflow as tf
import numpy as np

app = FastAPI()

# Load Model
model = tf.keras.models.load_model("model/stock_model.h5")

@app.get("/")
def home():
    return {"status": "OK", "message": "LSTM Webhook API is running"}

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


