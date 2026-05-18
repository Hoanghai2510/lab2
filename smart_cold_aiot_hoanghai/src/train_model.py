import json
import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from data_utils import (
    clean_data,
    create_features,
    calculate_anomaly_score,
    decision_rule
)


df = pd.read_csv("data/raw/cold_storage_raw.csv")

df = clean_data(df)

df.to_csv("data/processed/telemetry_clean.csv", index=False)

df = create_features(df)

df.to_csv("data/processed/feature_dataset.csv", index=False)

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

train_size = int(len(df) * 0.75)

train_df = df[:train_size]
test_df = df[train_size:]

X_train = train_df[feature_cols]
y_train = train_df["CoolingRisk"]

X_test = test_df[feature_cols]
y_test = test_df["CoolingRisk"]

model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

preds = model.predict(X_test)

probs = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, preds)
precision = precision_score(y_test, preds)
recall = recall_score(y_test, preds)
f1 = f1_score(y_test, preds)

metrics = {
    "accuracy": float(accuracy),
    "precision": float(precision),
    "recall": float(recall),
    "f1": float(f1)
}

with open("outputs/metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

joblib.dump(model, "models/cold_storage_model.joblib")

train_stats = {
    "temp_mean": train_df["Temperature"].mean(),
    "temp_std": train_df["Temperature"].std(),
    "co2_mean": train_df["CO2"].mean(),
    "co2_std": train_df["CO2"].std()
}

test_df["occupancy_probability"] = probs

test_df["anomaly_score"] = calculate_anomaly_score(
    test_df,
    train_stats
)

test_df["is_anomaly"] = (
    test_df["anomaly_score"] > 2.5
)

decision_rows = []

for _, row in test_df.iterrows():

    decision = decision_rule(
        row["occupancy_probability"],
        row["anomaly_score"]
    )

    decision_rows.append({
        "timestamp": row["timestamp"],
        "occupancy_probability": row["occupancy_probability"],
        "anomaly_score": row["anomaly_score"],
        "is_anomaly": row["is_anomaly"],
        "decision": decision["decision"],
        "command_hint": decision["command_hint"],
        "safety_note": decision["safety_note"]
    })

decision_df = pd.DataFrame(decision_rows)

decision_df.to_csv(
    "outputs/decision_log.csv",
    index=False
)

print("TRAINING COMPLETED")
print(metrics)