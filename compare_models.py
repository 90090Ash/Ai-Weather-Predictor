import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
import os
import pickle

def evaluate_models():
    # Load dataset
    data = pd.read_csv("data/weather.csv")

    # Input features
    X = data[['humidity', 'wind_speed', 'meanpressure']]
    y = data['meantemp']   # temperature to predict

    # Split into training and testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Define models
    models = {
        "Random Forest (Original)": RandomForestRegressor(n_estimators=100, random_state=42),
        "Linear Regression": LinearRegression(),
        "Decision Tree Regressor": DecisionTreeRegressor(random_state=42),
        "Gradient Boosting Regressor": GradientBoostingRegressor(random_state=42)
    }

    results = []

    print("Training and evaluating models...\n")
    print(f"{'Model':<30} | {'MAE':<10} | {'MSE':<10} | {'RMSE':<10} | {'R2 Score':<10}")
    print("-" * 81)

    os.makedirs("model", exist_ok=True)

    for name, model in models.items():
        # Train model
        model.fit(X_train, y_train)
        
        # Save model
        filename = name.replace(" ", "_").replace("(", "").replace(")", "").lower()
        with open(f"model/{filename}.pkl", "wb") as f:
            pickle.dump(model, f)
        
        # Predict
        y_pred = model.predict(X_test)
        
        # Evaluate
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = mse ** 0.5
        r2 = r2_score(y_test, y_pred)
        
        results.append({
            "Model": name,
            "MAE": mae,
            "MSE": mse,
            "RMSE": rmse,
            "R2": r2
        })
        
        print(f"{name:<30} | {mae:<10.4f} | {mse:<10.4f} | {rmse:<10.4f} | {r2:<10.4f}")

    return results

if __name__ == "__main__":
    evaluate_models()
