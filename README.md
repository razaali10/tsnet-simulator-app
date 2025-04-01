
# TSNET Transient Simulator App

This is a full-stack hydraulic simulation tool for transient analysis in water distribution networks using the **TSNET** Python library and EPANET `.inp` files.

## 🔧 Features

- Simulates hydraulic transients (e.g., valve closures, pump shutdowns, surge tanks, air chambers, PRVs)
- Flask API backend to handle simulation logic and return time-series results
- Streamlit GUI for interactive parameter input, visualization, and CSV downloads
- Compatible with OpenAI Custom GPT via Action Tool (`openapi.yaml` included)

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/tsnet-simulator-app.git
cd tsnet-simulator-app
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Flask API (Backend)

```bash
python app.py
```

API runs on: `http://localhost:5000/run-simulation`

### 4. Run Streamlit GUI (Frontend)

```bash
streamlit run streamlit_app.py
```

---

## 🌐 Deployment

### Deploy Flask API to Render
1. Push code to GitHub
2. Go to [Render](https://render.com), create a new Web Service
3. Set:
   - **Start command**: `python app.py`
   - **Build command**: `pip install -r requirements.txt`
4. Use the Render HTTPS URL in the `streamlit_app.py` and `openapi.yaml`

### Deploy Streamlit to Streamlit Cloud
1. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Link your repo and select `streamlit_app.py`
3. Set API URL correctly in your script

---

## 🧠 Example Transient Parameters (`transient_params.json`)

```json
{
  "event_type": "valve_closure",
  "pipe_id": "P23",
  "start_time": 10,
  "closure_time": 2,
  "tf": 60.0,
  "dt": 0.01,
  "monitor_nodes": ["N1", "N2"],
  "monitor_pipes": ["P10"]
}
```

---

## 🤖 GPT Integration

- `openapi.yaml` is included and points to `/run-simulation`
- Upload it to your Custom GPT's "Actions" section in the GPT Editor
- GPT will accept a `.inp` file and user parameters, trigger simulation, and return formatted results

---

## 📄 License

MIT License
