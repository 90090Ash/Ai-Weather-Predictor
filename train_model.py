import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

# Load dataset
data = pd.read_csv("data/weather.csv")

# Input features (3 only)
X = data[['humidity', 'wind_speed', 'meanpressure']]
y = data['meantemp']   # temperature to predict

# Split into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train the Random Forest
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
os.makedirs("model", exist_ok=True)
pickle.dump(model, open("model/weather_model.pkl", "wb"))

print("✅ Model trained successfully with 3 features")

