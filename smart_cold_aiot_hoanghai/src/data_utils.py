import pandas as pd
import numpy as np


REQUIRED_COLUMNS = [
    "timestamp",
    "Temperature",
    "Humidity",
    "CO2",
    "DoorOpen",
    "PowerConsumption",
    "CompressorVibration",
    "CoolingRisk"
]


def check_schema(df):
    missing = []

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            missing.append(col)

    return {
        "missing_columns": missing,
        "num_rows": len(df),
        "num_duplicates": df.duplicated().sum()
    }


def clean_data(df):

    df = df.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df = df.drop_duplicates()

    numeric_cols = [
        "Temperature",
        "Humidity",
        "CO2",
        "PowerConsumption",
        "CompressorVibration"
    ]

    for col in numeric_cols:
        df[col] = df[col].interpolate()

    return df


def create_features(df):

    df = df.copy()

    df["hour"] = df["timestamp"].dt.hour
    df["dayofweek"] = df["timestamp"].dt.dayofweek

    df["temp_rolling_mean"] = (
        df["Temperature"]
        .rolling(window=3, min_periods=1)
        .mean()
    )

    df["co2_delta"] = df["CO2"].diff().fillna(0)

    return df


def calculate_anomaly_score(df, train_stats):

    z_temp = abs(
        (df["Temperature"] - train_stats["temp_mean"])
        / train_stats["temp_std"]
    )

    z_co2 = abs(
        (df["CO2"] - train_stats["co2_mean"])
        / train_stats["co2_std"]
    )

    anomaly_score = (z_temp + z_co2) / 2

    return anomaly_score


def decision_rule(probability, anomaly_score):

    if anomaly_score > 2.5:
        return {
            "decision": "STOP_AUTO_CONTROL",
            "command_hint": "CHECK_SENSOR_AND_COOLING",
            "safety_note": "High anomaly score"
        }

    if probability >= 0.8:
        return {
            "decision": "CHECK_COOLING",
            "command_hint": "INSPECT_COMPRESSOR",
            "safety_note": "High cooling risk"
        }

    return {
        "decision": "NORMAL",
        "command_hint": "NONE",
        "safety_note": "System stable"
    }