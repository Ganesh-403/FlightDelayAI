# models/train_model.py
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pickle

# Load the historical dataset with weather features
df = pd.read_csv("data/flight_data.csv")

# For richer input, we now use 4 features:
# flight_duration, congestion, temperature, and humidity.
X = df[['flight_duration', 'congestion', 'temperature', 'humidity']]
y = df['delay']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the XGBoost model
model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))

# Save the trained model
pickle.dump(model, open("models/model.pkl", "wb"))
