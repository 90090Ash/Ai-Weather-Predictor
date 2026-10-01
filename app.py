# pyrefly: ignore [missing-import]
from flask import Flask, request, jsonify
import pickle
# pyrefly: ignore [missing-import]
import numpy as np

app = Flask(__name__)

model = pickle.load(open("model/weather_model.pkl", "rb"))

@app.route("/")
def home():
    return "AI Weather Forecast API is running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    humidity = data["humidity"]
    wind_speed = data["wind_speed"]
    meanpressure = data["meanpressure"]

    features = np.array([[humidity, wind_speed, meanpressure]])
    prediction = model.predict(features)

    return jsonify({
        "predicted_temperature": round(float(prediction[0]), 2)
    })

if __name__ == "__main__":
    app.run()
