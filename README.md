# ✈️ FlightDelayAI – Premium Flight Delay Analytics & Prediction 🚀

FlightDelayAI is a **state-of-the-art, full-stack machine learning application** designed to predict flight delays with precision. Featuring a high-end "Glassmorphism" UI and a comprehensive analytics dashboard, it provides real-time insights into the factors causing flight disruptions.

---

## 🎨 Premium Features

✅ **AI-Powered Predictions** – Real-time XGBoost model analysis.  
✅ **Interactive Analytics** – Dash-powered dashboard with dark-themed visualizations.  
✅ **Glassmorphism UI** – Modern, immersive frontend with smooth animations.  
✅ **Live History Sidebar** – Dynamically updates as new predictions are made.  
✅ **Secure Admin Panel** – Manage users and records via a protected Flask-Admin interface.  
✅ **Weather Integration** – Real-time weather data via OpenWeatherMap API.  

---

## 🛠 Tech Stack

- **Backend:** Flask, SQLAlchemy ORM, Flask-Login, Flask-Bcrypt
- **Frontend:** Glassmorphism CSS, Jinja2, Inter Typography
- **Analytics:** Dash, Plotly Express, Dash Bootstrap Components
- **ML Engine:** XGBoost, Scikit-Learn, Pandas, NumPy
- **Database:** PostgreSQL

---

## 🚀 Getting Started

### 1️⃣ Environment Setup
Create and activate a fresh virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2️⃣ Configure `config.py`
Update your PostgreSQL credentials and API key:
```python
DATABASE_URI = "postgresql://postgres:your_password@localhost:5432/flight_delay_db"
SECRET_KEY = "your_secret_key"
WEATHER_API_KEY = "your_openweathermap_key"
```

### 3️⃣ Initialize Database & Admin
Run the seeding script to create the database tables and the initial admin user:
```powershell
python create_admin.py
```
*Default Credentials: **admin** / **admin123***

### 4️⃣ Train the AI Model
```powershell
python models/train_model.py
```

---

## 🚦 Running the Application

FlightDelayAI uses a dual-server architecture. You must run both commands in separate terminals:

### ➤ Main Prediction App (Flask)
```powershell
python app.py
```
📍 **Access at:** [http://127.0.0.1:5000](http://127.0.0.1:5000)

### ➤ Analytics Dashboard (Dash)
```powershell
python dashboard.py
```
📍 **Access at:** [http://127.0.0.1:8050](http://127.0.0.1:8050)

---

## 🔧 Project Structure

- `app.py`: Main Flask server and API endpoints.
- `dashboard.py`: Interactive Dash analytics application.
- `models.py`: Database schema for Users and Predictions.
- `config.py`: Environment and API configurations.
- `templates/`: HTML templates (Home, Login).
- `static/`: Premium CSS styling and assets.
- `models/`: Machine learning training scripts and serialized model.

---

## 🙌 Support
⭐ **Star this repo** if you found it helpful!
