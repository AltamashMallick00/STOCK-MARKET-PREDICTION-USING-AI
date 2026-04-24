# StockAI Antigravity Prediction Engine (MNC Edition)

Developed by **Altamsh Mallick** & **Anubha Shankar**.

## 🚀 Features
- **MNC Focused:** Pre-loaded with data for Apple, Microsoft, Google, Amazon, Tesla, Meta, and Netflix.
- **Dual-Horizon Forecasting:**
  - **Short Term:** Next 24h prediction using LR and LSTM.
  - **Long Term:** Next 10 years trend projection.
- **Premium UI/UX:**
  - **Smooth Transitions:** High-performance CSS animations.
  - **Theming:** Full Light and Dark mode support.
  - **Profile System:** Integrated developer avatars.
- **Antigravity Engine:** Enhanced ensemble model for superior accuracy.
- **Fully Local:** Dataset-based, no external API keys required.
- **GitHub Repository:** [AltamashMallick00/STOCK-MARKET-PREDICTION-USING-AI](https://github.com/AltamashMallick00/STOCK-MARKET-PREDICTION-USING-AI.git)

## 📂 Project Structure
```
/project
 ├── backend/
 │   ├── app.py          # FastAPI routes & frontend serving
 │   ├── model.py        # AI Model logic (LR & LSTM)
 │   ├── utils.py        # Data loading utilities
 │   └── data/           # Local CSV datasets
 ├── frontend/
 │   ├── index.html      # UI Structure
 │   ├── style.css       # Premium Styling
 │   └── script.js       # UI Logic & API interaction
 ├── Dockerfile          # Containerization
 ├── requirements.txt    # Python dependencies
 └── README.md           # Documentation
```

## 🛠️ Local Setup

### 1. Install Dependencies
Ensure you have Python 3.11+ installed.
```bash
pip install -r requirements.txt
```

### 2. Generate Sample Data
Run the included script to create a sample stock dataset:
```bash
python backend/generate_data.py
```

### 3. Run the Application
Start the FastAPI server:
```bash
python -m backend.app
```
Then open your browser at `http://localhost:8000`.

## 🐳 Docker Setup

### 1. Build Image
```bash
docker build -t stock-ai-antigravity .
```

### 2. Run Container
```bash
docker run -p 8000:8000 stock-ai-antigravity
```

## ☁️ Deployment on Render
1. Connect your GitHub repository to [Render](https://render.com).
2. Create a new **Web Service**.
3. Use the following settings:
   - **Runtime:** `Docker`
   - **Region:** Any
   - **Plan:** Free (or higher)
4. Render will automatically use the `Dockerfile` to build and deploy.

---
Developed by ✨ **Altamsh Mallick** & **Anubha Shankar**  
All Rights Reserved @TIU2026
