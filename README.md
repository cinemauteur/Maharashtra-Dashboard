# Maharashtra Export Dashboard

A trade analytics dashboard inspired by NIRYAT, built with Python (Flask) + Node.js (Express), visualizing Maharashtra's regional and district-level export data.

---

## 📁 Project Structure

```
maharashtra-dashboard/
├── backend/
│   ├── app.py              ← Python Flask REST API
│   ├── requirements.txt    ← Python dependencies
│   └── Sample.xlsx         ← Your data file (place here)
├── frontend/
│   ├── index.html          ← Main dashboard UI
│   ├── server.js           ← Node.js Express static server
│   └── package.json        ← Node.js dependencies
└── README.md
```

---

## 🚀 Quick Start (2 terminals in VS Code)

### Terminal 1 — Start Python API Backend

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate       # Mac/Linux
# OR: venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Run the API
python app.py
```
API will be available at: **http://localhost:5000**

---

### Terminal 2 — Start Node.js Frontend Server

```bash
cd frontend

# Install dependencies
npm install

# Run the server
npm start
```
Dashboard will be available at: **http://localhost:3000**

---

## 📊 Dashboard Features

| Feature | Description |
|---|---|
| **KPI Cards** | Total export, latest month, MoM growth, districts, products |
| **Monthly Trend** | Line chart — Apr to Dec 2025 |
| **Region Table** | All 7 regions with growth % and share |
| **District Table** | All 36 districts, sortable by region |
| **Product Rankings** | Top 10 commodities with horizontal bar chart |
| **Filters** | Filter by Region, District, or Product/Commodity |
| **Views** | Overview · Districts · Products tabs |

---

## 🔌 API Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/filters` | All filter options (regions, districts, products) |
| `GET /api/summary` | KPI summary metrics |
| `GET /api/monthly-trend` | Monthly values Apr–Dec |
| `GET /api/regions` | Region-wise aggregated data |
| `GET /api/districts` | District-wise aggregated data |
| `GET /api/products` | Top 10 products by export value |

All endpoints support query params: `?region=...&district=...&product=...`

---

## 🔧 Troubleshooting

**"Cannot connect to Python API"**
→ Make sure `python app.py` is running in Terminal 1 first.

**CORS errors in browser**
→ The Flask app already includes `flask-cors`. Ensure you installed all requirements.

**Port conflict**
→ Change `port=5000` in `app.py` or `PORT=3000` in `server.js`.
