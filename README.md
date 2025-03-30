# ✈ FlightDelayAI – Predict Flight Delays with Machine Learning 🚀  

FlightDelayAI is a **machine learning-powered web application** that predicts flight delays based on various factors like **weather conditions, airport congestion, flight duration, and aircraft type**. The system leverages **Flask**, **PostgreSQL**, and **Plotly.js** to provide an interactive dashboard and REST API for real-time predictions.  

---

## 🔹 Features  
✅ **ML-Powered Predictions** – Uses a trained model to estimate flight delays  
✅ **Live Weather Data** – Fetches real-time weather for accurate forecasting  
✅ **Admin Dashboard** – Manage predictions with Flask-Admin  
✅ **Secure Authentication** – Login system with hashed passwords  
✅ **Interactive Analytics** – Visualize delays, congestion, and weather impact with Plotly  
✅ **Database Storage** – Stores predictions in a PostgreSQL database  

---

## 🛠 Tech Stack  
- **Backend:** Flask, Flask-Login, Flask-Admin, Flask-Bcrypt  
- **Database:** PostgreSQL with SQLAlchemy ORM  
- **Machine Learning:** Scikit-Learn, NumPy, Pickle  
- **Frontend:** HTML, CSS, JavaScript, Plotly.js  
- **API Integration:** OpenWeatherMap API  

---

## 🚀 Getting Started  

### 1️⃣ Clone the repo  
```sh
git clone https://github.com/YOUR-USERNAME/FlightDelayAI.git
cd FlightDelayAI
```

### 2️⃣ Install dependencies  
```sh
pip install -r requirements.txt
```

### 3️⃣ Set up PostgreSQL & configure `config.py`  
- Create a PostgreSQL database:  
  ```sql
  CREATE DATABASE flight_delay_db;
  ```
- Update `DATABASE_URI` in `config.py`:  
  ```py
  DATABASE_URI = "postgresql://your_username:your_password@localhost/flight_delay_db"
  ```

### 4️⃣ Run the app  
```sh
python app.py
```
The application will be available at `http://127.0.0.1:5000/`  

---

## 📊 Dashboard Preview  
[Insert an image of your dashboard here]  

---

## 🔧 API Endpoints  

### ➤ **Predict Flight Delay**  
**Endpoint:** `/predict`  
**Method:** `POST`  
**Request JSON:**  
```json
{
    "airline": "American Airlines",
    "origin": "JFK",
    "destination": "LAX",
    "flight_duration": 5.5,
    "congestion": 3.2,
    "aircraft_type": "Boeing 737"
}
```
**Response:**  
```json
{
    "delay_prediction": 12.5
}
```

---

## ⭐ Contribute & Support  
💡 Found a bug? Have an idea? Open an issue or submit a pull request!  

**🚀 Star this repo if you find it useful!** 🌟  

---
