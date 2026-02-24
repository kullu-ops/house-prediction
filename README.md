# EstateIQ — House Price Prediction App

## 📁 Project Structure
```
house-prediction/
├── backend/
│   ├── server.js       ← Node.js / Express API
│   ├── predict.py      ← Python ML prediction script
│   ├── Housing.csv     ← ⚠️ YOU MUST ADD THIS FILE
│   └── package.json
└── frontend/
    └── index.html      ← Standalone HTML app
```

---

## 🚀 Setup Steps

### Step 1 — Prerequisites
Make sure you have installed:
- **Node.js** (v18+) → https://nodejs.org
- **Python 3** (v3.8+) → https://python.org
- **pip packages**: `pip install scikit-learn numpy pandas`

---

### Step 2 — Add your dataset
Copy your `Housing.csv` file into the `backend/` folder:
```
house-prediction/backend/Housing.csv
```
This is the same CSV used during training in your notebook.

---

### Step 3 — Install Node dependencies
```bash
cd house-prediction/backend
npm install
```

---

### Step 4 — Start the backend server
```bash
node server.js
```
You should see:
```
🏠 House Prediction API running on http://localhost:3000
```

---

### Step 5 — Open the app
Visit in your browser:
```
http://localhost:3000
```

---

## ⚙️ How It Works

1. You fill in property details in the beautiful UI
2. The frontend sends a POST request to `/api/predict`
3. The Node.js backend calls `predict.py` with the features
4. Python trains the pipeline (first time only, then caches `model.pkl`)
5. The predicted price is returned and displayed

**The model matches your notebook exactly:**
- Log-transforms price before training
- Combines bedrooms + bathrooms → `total_room`
- One-hot encodes `furnishingstatus` and `stories`
- Uses `StandardScaler + LinearRegression` pipeline
- Applies `np.exp()` to reverse the log transform on output

---

## 🔁 Model Caching
On first run, `predict.py` trains the model and saves it as `backend/model.pkl`.
All future predictions load from this file (fast). If you update `Housing.csv`, delete `model.pkl` to retrain.

---

## 🛠️ Troubleshooting

| Issue | Fix |
|---|---|
| `Housing.csv not found` | Copy it to `backend/` folder |
| `Cannot connect to server` | Run `node server.js` first |
| `python3 not found` | Install Python or change `python3` → `python` in server.js |
| `ModuleNotFoundError` | Run `pip install scikit-learn numpy pandas` |
