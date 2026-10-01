# pyrefly: ignore [missing-import]
from flask import Flask, request, jsonify, send_from_directory
import pickle
# pyrefly: ignore [missing-import]
import numpy as np

# Serve static files from the current directory
app = Flask(__name__, static_url_path='', static_folder='.')

# Load all 4 models
models = {
    "Random Forest": pickle.load(open("model/random_forest_original.pkl", "rb")),
    "Linear Regression": pickle.load(open("model/linear_regression.pkl", "rb")),
    "Decision Tree": pickle.load(open("model/decision_tree_regressor.pkl", "rb")),
    "Gradient Boosting": pickle.load(open("model/gradient_boosting_regressor.pkl", "rb"))
}

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route("/")
def home():
    return send_from_directory('.', 'index.html')

@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    data = request.json

    humidity = data["humidity"]
    wind_speed = data["wind_speed"]
    meanpressure = data["meanpressure"]

    features = np.array([[humidity, wind_speed, meanpressure]])
    
    predictions = {}
    for name, model in models.items():
        prediction = model.predict(features)
        predictions[name] = round(float(prediction[0]), 2)

    return jsonify({
        "input_features": {
            "humidity": humidity,
            "wind_speed": wind_speed,
            "meanpressure": meanpressure
        },
        "predictions": predictions
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)
