import pickle
import numpy as np
import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from config import DATABASE_URI, SECRET_KEY, WEATHER_API_KEY
from models import db, User, Prediction  # ✅ Import models after moving them to models.py

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = SECRET_KEY

# Initialize extensions
db.init_app(app)  # ✅ Fix: Use db.init_app instead of creating a new instance
bcrypt = Bcrypt(app)

# ✅ Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect unauthorized users to login

# Import setup_admin AFTER db is initialized
from setup_admin import setup_admin_bp, init_admin

# Register Blueprint for setting up admin users
app.register_blueprint(setup_admin_bp, url_prefix="/admin")

# Initialize Admin Panel
init_admin(app)

# ----------------- Load the ML Model -----------------
model = pickle.load(open("models/model.pkl", "rb"))

# ----------------- User Authentication -----------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles login; on POST, checks credentials and logs in the user."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin.index'))
        else:
            return render_template('login.html', error="Invalid credentials.")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Logs out the current user."""
    logout_user()
    return redirect(url_for('login'))

# ----------------- Utility Functions -----------------
def fetch_weather(airport_code):
    """
    Fetch live weather data using OpenWeatherMap API.
    For simplicity, it treats the airport code as a city name.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={airport_code}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

# ----------------- API Routes -----------------
@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict flight delay using the trained ML model.
    Expects JSON input with keys:
    airline, origin, destination, flight_duration, congestion, aircraft_type
    """
    data = request.json

    # Fetch live weather data for the origin airport
    weather_json = fetch_weather(data['origin'])
    if "main" in weather_json:
        temp = weather_json["main"]["temp"]
        humidity = weather_json["main"]["humidity"]
    else:
        temp = 25    # default temperature
        humidity = 50  # default humidity

    # Prepare input features as a 4-element array:
    # flight_duration, congestion, temperature, humidity
    input_features = np.array([[data['flight_duration'], data['congestion'], temp, humidity]])
    
    # Predict delay using the model
    prediction = model.predict(input_features)[0]
    
    # Save the prediction to the database, converting numpy.float32 to a standard float
    new_prediction = Prediction(
        airline=data['airline'],
        origin=data['origin'],
        destination=data['destination'],
        flight_duration=data['flight_duration'],
        congestion=data['congestion'],
        aircraft_type=data['aircraft_type'],
        delay=float(prediction)  # Convert to native Python float
    )
    db.session.add(new_prediction)
    db.session.commit()
    
    return jsonify({'delay_prediction': float(prediction)})

@app.route('/')
def index():
    """Renders the home page."""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Renders the Flight Delay Analytics Dashboard with Plotly charts."""
    
    # Fetch the latest flight delay data (modify this based on your database structure)
    recent_predictions = Prediction.query.order_by(Prediction.id.desc()).limit(50).all()
    
    # Convert the query results into JSON format suitable for Plotly
    route_delay_data = []  # Replace with your actual query logic
    weather_impact_data = []  # Replace with actual weather impact data
    congestion_impact_data = []  # Replace with actual congestion data
    delay_trends_data = []  # Replace with historical delay trend data

    return render_template(
        'dashboard.html',
        route_delay_data=route_delay_data,
        weather_impact_data=weather_impact_data,
        congestion_impact_data=congestion_impact_data,
        delay_trends_data=delay_trends_data
    )


# ----------------- Run the App -----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)
