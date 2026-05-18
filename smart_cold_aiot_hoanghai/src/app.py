from fastapi import FastAPI
import pandas as pd
import joblib
import json

from data_utils import decision_rule

app = FastAPI()

model = joblib.load(
    "models/cold_storage_model.joblib"
)

with open("outputs/metrics.json") as f:
    metrics = json.load(f)

feature_cols = [
    "Temperature",
    "Humidity",
    "CO2",
    "DoorOpen",
    "PowerConsumption",
    "CompressorVibration",
    "hour",
    "dayofweek",
    "temp_rolling_mean",
    "co2_delta"
]


@app.get("/health")
def health():

    return {
        "model_loaded": True
    }


@app.get("/model-info")
def model_info():

    return {
        "model_type": "LogisticRegression",
        "feature_cols": feature_cols,
        "metrics": metrics
    }


@app.post("/predict")
def predict(data: dict):

    df = pd.DataFrame([data])

    probability = model.predict_proba(df)[0][1]

    prediction = int(probability >= 0.5)

    anomaly_score = abs(df["CO2"][0] - 500) / 200

    decision = decision_rule(
        probability,
        anomaly_score
    )

    return {
        "model_output": {
            "occupancy_probability": float(probability),
            "predicted_occupancy": prediction,
            "anomaly_score": float(anomaly_score),
            "is_anomaly": anomaly_score > 2.5
        },
        "decision": decision
    }