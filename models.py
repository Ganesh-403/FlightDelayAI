from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for admin authentication."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Prediction(db.Model):
    """Prediction model to store flight delay predictions."""
    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(50))
    origin = db.Column(db.String(10))
    destination = db.Column(db.String(10))
    flight_duration = db.Column(db.Float)
    congestion = db.Column(db.Float)
    aircraft_type = db.Column(db.String(50))
    delay = db.Column(db.Float)
