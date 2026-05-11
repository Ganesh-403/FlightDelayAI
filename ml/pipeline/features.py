# ml/pipeline/features.py
import pandas as pd
import numpy as np

class FeatureEngineer:
    def __init__(self):
        self.feature_cols = ['flight_duration', 'congestion', 'temperature', 'humidity']

    def preprocess(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Implements reproducible preprocessing steps.
        In a real app, this would handle categorical encoding, scaling, etc.
        """
        df = data.copy()
        
        # Ensure numeric types
        for col in self.feature_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Simple imputation
        df = df.fillna(df.median(numeric_only=True))
        
        return df[self.feature_cols]

    def get_inference_features(self, data_dict: dict) -> np.ndarray:
        """
        Converts a single request dictionary into the format expected by the model.
        """
        df = pd.DataFrame([data_dict])
        processed = self.preprocess(df)
        return processed.values
