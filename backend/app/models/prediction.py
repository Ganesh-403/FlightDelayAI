# backend/app/models/prediction.py
from datetime import datetime
from .base import db

class Prediction(db.Model):
    __tablename__ = 'predictions'
    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(50), nullable=False)
    origin = db.Column(db.String(10), nullable=False, index=True)
    destination = db.Column(db.String(10), nullable=False, index=True)
    flight_duration = db.Column(db.Float, nullable=False)
    congestion = db.Column(db.Float, nullable=False)
    aircraft_type = db.Column(db.String(50))
    delay = db.Column(db.Float, nullable=False)
    confidence_score = db.Column(db.Float, default=1.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "airline": self.airline,
            "origin": self.origin,
            "destination": self.destination,
            "delay": self.delay,
            "created_at": self.created_at.isoformat()
        }
