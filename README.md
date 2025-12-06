# LSTM webhook API (FastAPI + Render)

This projekt deploys a FastAPI server that:
- loads a LSTM model ('stock_model.h5')
- Accepts webhook alerts via POST /webhook
- Returns predictions and trading signals
- Runs on Render's FREE plan with HTPPS support

## Deployment (Render)

1. Push this projekt to Github repository
2. Go to https://render.com
3. Click **New -> web services**
4. Connect your Github repo
5. Render detects 'render.yaml' automatically
6. Wait for deployment

Your final webhook URL will be:
https://<your-app-name>.onrender.com/webhook
