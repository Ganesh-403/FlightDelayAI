# backend/app/api/v1/predict.py
from flask import Blueprint, request, jsonify
from flask_login import current_user
from pydantic import BaseModel, Field, field_validator, ValidationError
from ...services.prediction_service import PredictionService
from ... import socketio

predict_bp = Blueprint("predict", __name__)
prediction_service = PredictionService()

class PredictionRequest(BaseModel):
    airline: str = Field(..., min_length=1)
    origin: str = Field(..., min_length=3, max_length=3)
    destination: str = Field(..., min_length=3, max_length=3)
    flight_duration: float = Field(..., gt=0)
    congestion: float = Field(..., ge=1, le=10)
    aircraft_type: str = Field(None)
    
    @field_validator('origin', 'destination')
    @classmethod
    def validate_iata(cls, v: str) -> str:
        if not v.isalpha():
            raise ValueError("IATA airport code must contain only letters")
        return v.upper().strip()

@predict_bp.route("/", methods=["POST"])
def predict_delay():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON request body"}), 400
        
    try:
        validated = PredictionRequest(**data)
    except ValidationError as e:
        errors = {err['loc'][0]: err['msg'] for err in e.errors()}
        return jsonify({"error": "Validation failed", "details": errors}), 400
        
    try:
        user_id = current_user.id if current_user.is_authenticated else None
        result = prediction_service.get_prediction(validated.model_dump(), user_id=user_id)
        
        # Emit real-time WebSocket event
        socketio.emit("new_prediction", result)
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@predict_bp.route("/history", methods=["GET"])
def get_history():
    limit = request.args.get("limit", 10, type=int)
    # Filter by user if logged in, otherwise return recent predictions
    user_id = current_user.id if current_user.is_authenticated else None
    history = prediction_service.get_history(limit, user_id=user_id)
    return jsonify(history), 200

