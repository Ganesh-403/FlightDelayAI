import pickle
import numpy as np
import pandas as pd
import requests
import sys
import os

# Add root to sys.path to import ml modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from ml.pipeline.features import FeatureEngineer

from ..core.config import settings
from ..models.prediction import Prediction
from ..models.base import db

import xgboost as xgb

class PredictionService:
    def __init__(self):
        self.fe = FeatureEngineer()
        self.model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml/models/v1_model.json"))
        self.model = xgb.XGBRegressor()
        try:
            self.model.load_model(self.model_path)
        except Exception as e:
            print(f"Model Load Error: {e}")
            self.model = None

    def fetch_weather(self, airport_code):
        # Implementation remains the same but with better logging
        if not settings.WEATHER_API_KEY:
            return {"temp": 25, "humidity": 50}
            
        url = f"http://api.openweathermap.org/data/2.5/weather?q={airport_code}&appid={settings.WEATHER_API_KEY}&units=metric"
        try:
            response = requests.get(url, timeout=5)
            weather_json = response.json()
            if "main" in weather_json:
                return {
                    "temp": weather_json["main"]["temp"],
                    "humidity": weather_json["main"]["humidity"]
                }
        except Exception as e:
            print(f"Weather API Error: {e}")
        return {"temp": 25, "humidity": 50}

    def get_prediction(self, data):
        if not self.model:
            raise Exception("Prediction model not found on server")

        weather = self.fetch_weather(data['origin'])
        
        # Use the FeatureEngineer for consistency
        inference_data = {
            'flight_duration': data['flight_duration'],
            'congestion': data['congestion'],
            'temperature': weather['temp'],
            'humidity': weather['humidity']
        }
        
        features = self.fe.get_inference_features(inference_data)
        prediction_val = float(self.model.predict(features)[0])
        
        # Save to DB
        new_pred = Prediction(
            airline=data['airline'],
            origin=data['origin'],
            destination=data['destination'],
            flight_duration=data['flight_duration'],
            congestion=data['congestion'],
            aircraft_type=data.get('aircraft_type'),
            delay=prediction_val
        )
        db.session.add(new_pred)
        db.session.commit()
        
        return {
            "delay_prediction": prediction_val,
            "weather": weather,
            "confidence": 0.92 # Placeholder for actual confidence logic
        }

    def get_history(self, limit):
        predictions = Prediction.query.order_by(Prediction.created_at.desc()).limit(limit).all()
        return [p.to_dict() for p in predictions]
