import pickle
import numpy as np
import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from config import DATABASE_URI, SECRET_KEY, WEATHER_API_KEY
from models import db, User, Prediction  # Import models from models.py

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = SECRET_KEY

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ----------------- Admin Configuration -----------------
class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class UserAdminView(SecureModelView):
    column_exclude_list = ['password']
    form_excluded_columns = ['password']

class PredictionAdminView(SecureModelView):
    column_default_sort = ('id', True)
    column_filters = ['airline', 'origin', 'destination']

admin = Admin(app, name='FlightDelayAI Admin', template_mode='bootstrap4')
admin.add_view(UserAdminView(User, db.session))
admin.add_view(PredictionAdminView(Prediction, db.session))


# ----------------- Load the ML Model -----------------
model = pickle.load(open("models/model.pkl", "rb"))

# ----------------- User Authentication Routes -----------------
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
        delay=float(prediction)
    )
    db.session.add(new_prediction)
    db.session.commit()
    
    return jsonify({'delay_prediction': float(prediction)})

@app.route('/recent_predictions', methods=['GET'])
def get_recent_predictions():
    """Fetches the 5 most recent predictions from the database."""
    predictions = Prediction.query.order_by(Prediction.id.desc()).limit(5).all()
    data = []
    for p in predictions:
        data.append({
            'airline': p.airline,
            'origin': p.origin,
            'destination': p.destination,
            'delay': round(p.delay, 1)
        })
    return jsonify(data)

@app.route('/')
def index():
    """Renders the home page."""
    return render_template('index.html')

# ----------------- Run the App -----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)
