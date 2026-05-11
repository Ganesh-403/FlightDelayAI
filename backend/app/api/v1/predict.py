# backend/app/api/v1/predict.py
from flask import Blueprint, request, jsonify
from flask_login import login_required
from ...services.prediction_service import PredictionService

predict_bp = Blueprint("predict", __name__)
prediction_service = PredictionService()

@predict_bp.route("/", methods=["POST"])
def predict_delay():
    data = request.get_json()
    # In a real enterprise app, we'd use Pydantic for validation here
    try:
        result = prediction_service.get_prediction(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@predict_bp.route("/history", methods=["GET"])
def get_history():
    limit = request.args.get("limit", 10, type=int)
    history = prediction_service.get_history(limit)
    return jsonify(history), 200
