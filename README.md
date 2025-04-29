# ✈ FlightDelayAI – Predict Flight Delays with Machine Learning 🚀

FlightDelayAI is a **machine learning-powered web application** that predicts flight delays based on factors like **weather conditions, airport congestion, flight duration, and aircraft type**. It uses **Flask** for the backend, **PostgreSQL** for data storage, and **Dash/Plotly Express** for an interactive dashboard.

---

## 🔹 Features

✅ **ML-Powered Predictions** – Predict delays based on trained data  
✅ **Live Weather Integration** – Real-time weather from OpenWeatherMap  
✅ **Admin Dashboard** – View predictions using Flask-Admin  
✅ **Secure Login** – Passwords hashed using Flask-Bcrypt  
✅ **Interactive Dashboard** – Built with Dash and Plotly Express  
✅ **REST API** – JSON-based prediction endpoint  

---

## 🛠 Tech Stack

- **Backend:** Flask, Flask-Login, Flask-Admin, Flask-Bcrypt  
- **ML:** XGBoost, NumPy, Pandas  
- **Database:** PostgreSQL, SQLAlchemy ORM  
- **Visualization:** Dash, Plotly Express  
- **Other:** OpenWeatherMap API  

---

## 🚀 Getting Started

### 1️⃣ Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/FlightDelayAI.git
cd FlightDelayAI
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set up PostgreSQL & configure `config.py`

- Create a PostgreSQL database:

```sql
CREATE DATABASE flight_delay_db;
```

- Update `config.py` with your details:

```python
DATABASE_URI = "postgresql://your_username:your_password@localhost/flight_delay_db"
SECRET_KEY = "your_secret_key"
WEATHER_API_KEY = "your_openweathermap_api_key"
```

📝 *Tip: Rename `config.py` to `config_template.py` before pushing to GitHub, and ignore `config.py` via `.gitignore`.*

### 4️⃣ Train the ML Model

```bash
python models/train_model.py
```

➡️ This will generate `model.pkl` inside the `models/` folder.

### 5️⃣ Run the Flask App

```bash
python app.py
```

📍 Opens at: `http://127.0.0.1:5000/`  
This includes:
- Prediction form
- Admin login & dashboard
- REST API endpoint `/predict`

### 6️⃣ Run the Dash Dashboard

In a **new terminal**, run:

```bash
python dashboard.py
```

📍 Opens at: `http://127.0.0.1:8050/`  
Visualizes:
- Weather impact on delays
- Congestion patterns
- Route-based averages
- Time series trends

---

## 📊 Dashboard Preview

![Dashboard 1](assets/dashboard1.jpg)  
![Dashboard 2](assets/dashboard2.jpg)  
![Prediction Page](assets/predictionpage.jpg)

---

## 🔧 API Endpoint

### ➤ Predict Flight Delay

- **Endpoint:** `/predict`
- **Method:** `POST`
- **Content-Type:** `application/json`

**Request Example:**

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

## 🙌 Contribute & Support

💡 Found a bug or have a suggestion?  
Create an issue or submit a pull request.

⭐ **Star this repo** if you found it helpful!

---

## 📄 License

This project is licensed under the MIT License.
