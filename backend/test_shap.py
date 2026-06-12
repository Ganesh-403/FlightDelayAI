import xgboost as xgb
import shap
import numpy as np

try:
    model = xgb.XGBRegressor()
    model.load_model("ml/models/v1_model.json")
    explainer = shap.TreeExplainer(model)
    X = np.array([[120.0, 5.0, 25.0, 50.0]])
    shap_values = explainer.shap_values(X)
    print("SHAP values computed successfully:", shap_values)
except Exception as e:
    print("Error during SHAP test:", e)
