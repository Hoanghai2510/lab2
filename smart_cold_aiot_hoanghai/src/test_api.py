import requests

payload = {
    "Temperature": -10,
    "Humidity": 70,
    "CO2": 800,
    "DoorOpen": 1,
    "PowerConsumption": 1800,
    "CompressorVibration": 1.5,
    "hour": 10,
    "dayofweek": 1,
    "temp_rolling_mean": -12,
    "co2_delta": 100
}

response = requests.post(
    "http://127.0.0.1:8000/predict",
    json=payload
)

print(response.json())

print("API TEST PASSED")