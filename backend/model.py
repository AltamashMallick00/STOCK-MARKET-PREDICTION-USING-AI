import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn as nn

class LSTMModel(nn.Module):
    def __init__(self, input_size=1, hidden_layer_size=50, output_size=1):
        super(LSTMModel, self).__init__()
        self.hidden_layer_size = hidden_layer_size
        self.lstm = nn.LSTM(input_size, hidden_layer_size, batch_first=True)
        self.linear = nn.Linear(hidden_layer_size, output_size)

    def forward(self, input_seq):
        lstm_out, _ = self.lstm(input_seq)
        predictions = self.linear(lstm_out[:, -1, :])
        return predictions

class StockPredictor:
    def __init__(self):
        self.lr_model = LinearRegression()
        self.lstm_model = LSTMModel()
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.look_back = 60

    def prepare_data(self, data):
        # Using 'Close' prices for prediction
        prices = data['Close'].values.reshape(-1, 1)
        scaled_data = self.scaler.fit_transform(prices)
        
        X_lr, y_lr = [], []
        X_lstm, y_lstm = [], []
        
        for i in range(self.look_back, len(scaled_data)):
            # For Linear Regression (using previous close as feature)
            X_lr.append(scaled_data[i-1, 0])
            y_lr.append(scaled_data[i, 0])
            
            # For LSTM (using sequence of previous closes)
            X_lstm.append(scaled_data[i-self.look_back:i, 0])
            y_lstm.append(scaled_data[i, 0])
            
        return np.array(X_lr).reshape(-1, 1), np.array(y_lr), np.array(X_lstm), np.array(y_lstm)

    def train(self, data):
        X_lr, y_lr, X_lstm, y_lstm = self.prepare_data(data)
        
        # Train Linear Regression
        self.lr_model.fit(X_lr, y_lr)
        
        # Train LSTM
        X_lstm_tensor = torch.FloatTensor(X_lstm).unsqueeze(-1)
        y_lstm_tensor = torch.FloatTensor(y_lstm).unsqueeze(-1)
        
        optimizer = torch.optim.Adam(self.lstm_model.parameters(), lr=0.01)
        criterion = nn.MSELoss()
        
        self.lstm_model.train()
        for epoch in range(10): # Small number of epochs for quick demo
            optimizer.zero_grad()
            output = self.lstm_model(X_lstm_tensor)
            loss = criterion(output, y_lstm_tensor)
            loss.backward()
            optimizer.step()
            
    def predict(self, last_sequence):
        # last_sequence should be the last 'look_back' prices
        scaled_seq = self.scaler.transform(last_sequence.reshape(-1, 1))
        
        # LR Prediction
        lr_pred_scaled = self.lr_model.predict([[scaled_seq[-1, 0]]])[0]
        lr_pred = self.scaler.inverse_transform([[lr_pred_scaled]])[0][0]
        
        # LSTM Prediction
        self.lstm_model.eval()
        with torch.no_grad():
            lstm_input = torch.FloatTensor(scaled_seq).unsqueeze(0).unsqueeze(-1)
            lstm_pred_scaled = self.lstm_model(lstm_input).item()
            lstm_pred = self.scaler.inverse_transform([[lstm_pred_scaled]])[0][0]
            
        # Antigravity Engine: Weighted Ensemble
        antigravity_pred = (0.3 * lr_pred) + (0.7 * lstm_pred)
        
        return {
            "linear_regression": float(lr_pred),
            "lstm": float(lstm_pred),
            "antigravity": float(antigravity_pred)
        }

    def predict_long_term(self, last_sequence, years=10):
        # Predict one point per year for 'years' years
        # Using a simplified trend projection for such a long duration
        current_price = last_sequence[-1]
        
        # Get current growth trend from LR
        scaled_seq = self.scaler.transform(last_sequence.reshape(-1, 1))
        lr_pred_scaled = self.lr_model.predict([[scaled_seq[-1, 0]]])[0]
        lr_pred = self.scaler.inverse_transform([[lr_pred_scaled]])[0][0]
        
        daily_growth = (lr_pred - current_price) / current_price
        
        long_term = []
        for year in range(1, years + 1):
            # Compound the growth with some random variance
            growth_factor = (1 + daily_growth * 252) ** year # 252 trading days
            # Add some long-term AI "Antigravity" bias (positive drift)
            antigravity_drift = 1 + (0.02 * year) 
            predicted_price = current_price * growth_factor * antigravity_drift
            long_term.append({
                "year": 2026 + year,
                "price": float(predicted_price)
            })
            
        return long_term
