from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # New field for admin status

class Prediction(db.Model):
    __tablename__ = 'prediction'
    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(50))
    origin = db.Column(db.String(10))
    destination = db.Column(db.String(10))
    flight_duration = db.Column(db.Float)
    congestion = db.Column(db.Float)
    aircraft_type = db.Column(db.String(50))
    delay = db.Column(db.Float)
