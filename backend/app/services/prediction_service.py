import pickle
import numpy as np
import pandas as pd
import requests
import sys
import os
import redis
import json

# Add root to sys.path to import ml modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from ml.pipeline.features import FeatureEngineer

from ..core.config import settings
from ..models.prediction import Prediction
from ..models.base import db

import xgboost as xgb
import shap

class PredictionService:
    def __init__(self):
        self.fe = FeatureEngineer()
        self.model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml/models/v1_model.json"))
        self.model = xgb.XGBRegressor()
        self.explainer = None
        try:
            self.model.load_model(self.model_path)
            self.explainer = shap.TreeExplainer(self.model)
        except Exception as e:
            print(f"Model/SHAP Explainer Load Error: {e}")
            self.model = None
            
        # Initialize Redis connection
        try:
            self.redis = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=0,
                decode_responses=True,
                socket_timeout=2
            )
            self.redis.ping()
            print("Successfully connected to Redis cache.")
        except Exception as e:
            print(f"Warning: Redis connection failed ({e}). Running without cache.")
            self.redis = None

    def fetch_weather(self, airport_code):
        airport_code = airport_code.upper().strip()
        
        # Check cache first
        if self.redis:
            cache_key = f"weather:{airport_code}"
            try:
                cached = self.redis.get(cache_key)
                if cached:
                    print(f"Redis Cache Hit for weather:{airport_code}")
                    return json.loads(cached)
            except Exception as e:
                print(f"Redis error fetching weather: {e}")
                
        # Cache miss - call OpenWeather API
        if not settings.WEATHER_API_KEY:
            return {"temp": 25, "humidity": 50}
            
        url = f"http://api.openweathermap.org/data/2.5/weather?q={airport_code}&appid={settings.WEATHER_API_KEY}&units=metric"
        weather_data = {"temp": 25, "humidity": 50}
        try:
            response = requests.get(url, timeout=5)
            weather_json = response.json()
            if "main" in weather_json:
                weather_data = {
                    "temp": float(weather_json["main"]["temp"]),
                    "humidity": float(weather_json["main"]["humidity"])
                }
                # Cache for 15 minutes (900 seconds)
                if self.redis:
                    try:
                        self.redis.setex(cache_key, 900, json.dumps(weather_data))
                        print(f"Cached weather for {airport_code} in Redis")
                    except Exception as e:
                        print(f"Redis error caching weather: {e}")
        except Exception as e:
            print(f"Weather API Error: {e}")
        return weather_data

    def get_prediction(self, data, user_id=None):
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
        
        # Compute SHAP explanation values for the features
        shap_contributions = {}
        if self.explainer:
            try:
                shap_vals = self.explainer.shap_values(features)[0]
                for col, val in zip(self.fe.feature_cols, shap_vals):
                    shap_contributions[col] = float(val)
            except Exception as e:
                print(f"SHAP explanation calculation error: {e}")

        # Save to DB
        new_pred = Prediction(
            airline=data['airline'],
            origin=data['origin'].upper().strip(),
            destination=data['destination'].upper().strip(),
            flight_duration=float(data['flight_duration']),
            congestion=float(data['congestion']),
            aircraft_type=data.get('aircraft_type'),
            delay=prediction_val,
            confidence_score=0.92,
            user_id=user_id
        )
        db.session.add(new_pred)
        db.session.commit()
        
        return {
            "id": new_pred.id,
            "airline": new_pred.airline,
            "origin": new_pred.origin,
            "destination": new_pred.destination,
            "flight_duration": new_pred.flight_duration,
            "congestion": new_pred.congestion,
            "aircraft_type": new_pred.aircraft_type,
            "delay": prediction_val,
            "weather": weather,
            "confidence": new_pred.confidence_score,
            "created_at": new_pred.created_at.isoformat(),
            "user_id": new_pred.user_id,
            "shap_contributions": shap_contributions
        }

    def get_history(self, limit, user_id=None):
        query = Prediction.query
        if user_id:
            query = query.filter_by(user_id=user_id)
        predictions = query.order_by(Prediction.created_at.desc()).limit(limit).all()
        return [p.to_dict() for p in predictions]

