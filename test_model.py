import pandas as pd
import tensorflow as tf
import yfinance as yf

tickers = 'TSLA'

start_date = "2023-01-01"
end_date = "2025-11-30"

test_data = yf.download(tickers, start=start_date, end=end_date,  auto_adjust=False)
#print(test_data.head())

data_processed = test_data.iloc[:, 1:2].values
print(data_processed.shape)

model = tf.keras.models.load_model("model/stock_model.h5")

predicted_price = model.predict(data_processed)
print(predicted_price)