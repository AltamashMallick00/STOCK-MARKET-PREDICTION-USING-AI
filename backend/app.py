from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from fastapi.staticfiles import StaticFiles
from .model import StockPredictor
from .utils import load_stock_data, get_available_stocks
import uvicorn
import os

app = FastAPI(title="Stock Prediction AI - Antigravity Engine")

# Mount frontend
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = StockPredictor()

class PredictionRequest(BaseModel):
    symbol: str

@app.get("/stocks")
async def list_stocks():
    return {"stocks": get_available_stocks()}

@app.post("/predict")
async def predict_stock(request: PredictionRequest):
    data = load_stock_data(request.symbol)
    if data is None:
        raise HTTPException(status_code=404, detail="Stock data not found")
    
    # Train model on current data
    predictor.train(data)
    
    # Get predictions
    last_sequence = data['Close'].values[-60:]
    predictions = predictor.predict(last_sequence)
    long_term = predictor.predict_long_term(last_sequence)
    
    # Prepare chart data (last 30 days + prediction)
    history = data.tail(30)[['Date', 'Close']].to_dict(orient='records')
    
    return {
        "symbol": request.symbol,
        "history": history,
        "predictions": predictions,
        "long_term": long_term
    }

# Mount frontend (MUST be after API routes)
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
