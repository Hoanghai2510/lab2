# SMART COLD STORAGE AIOT

### Hệ thống AIoT cho kho lạnh thông minh

---

## 1. Giới thiệu

Đề tài xây dựng hệ thống AIoT giúp:

- Giám sát kho lạnh bằng cảm biến IoT
- Dự đoán nguy cơ mất lạnh bằng AI
- Sinh cảnh báo và decision log
- Deploy AI model bằng FastAPI

---

## Pipeline hệ thống

```text
Raw Data
   ↓
Clean Data
   ↓
Feature Engineering
   ↓
Train AI Model
   ↓
Save Model
   ↓
FastAPI Deployment
   ↓
Prediction & Decision Layer
```

---

## Cấu trúc project

```text
smart_cold_storage_aiot/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── src/
│   ├── app.py
│   ├── train_model.py
│   ├── data_utils.py
│   ├── test_api.py
│   └── check_outputs.py
│
├── models/
│
├── outputs/
│
├── docs/
│
├── README.md
└── requirements.txt
```

---

## 2. Dataset

### File dữ liệu chính

```text
data/raw/cold_storage_raw.csv
```

### Các trường dữ liệu

- Temperature
- Humidity
- CO2
- DoorOpen
- PowerConsumption
- CompressorVibration
- CoolingRisk

---

## 3. Xử lý dữ liệu

Hệ thống thực hiện:

- Xóa dữ liệu trùng lặp
- Xử lý missing value
- Chuẩn hóa timestamp
- Feature engineering
- Tạo feature dataset cho AI

### Output sinh ra

```text
data/processed/telemetry_clean.csv
data/processed/feature_dataset.csv
```

---

## 4. AI Model

### Model sử dụng

```text
Logistic Regression
```

### Train/Test Split

- 75% Train
- 25% Test

### Output model

```text
models/cold_storage_model.joblib
outputs/metrics.json
```

---

## 5. Anomaly Detection

Hệ thống sử dụng:

- Temperature anomaly
- CO2 anomaly
- Z-score detection

### Mục đích

- Phát hiện dữ liệu bất thường
- Hỗ trợ safety layer
- Tránh điều khiển sai hệ thống kho lạnh

---

## 6. FastAPI Deployment

### Chạy API

```bash
uvicorn src.app:app --reload --port 8001
```

### Swagger Docs

```text
http://127.0.0.1:8001/docs
```

### API Endpoints

| Endpoint | Chức năng |
|---|---|
| `/health` | Kiểm tra API |
| `/model-info` | Thông tin model |
| `/predict` | Dự đoán AI |

---

## 7. Output Files

```text
outputs/
├── metrics.json
├── decision_log.csv
└── predictions.csv

models/
└── cold_storage_model.joblib
```

---

## 8. Decision Rule

### Rule 1

```text
anomaly_score > 2.5
```

→ STOP_AUTO_CONTROL

---

### Rule 2

```text
probability >= 0.8
```

→ CHECK_COOLING

---

### Rule 3

```text
Normal condition
```

→ NORMAL

---

## 9. Kết quả đạt được

Hệ thống đã:

- Xây dựng pipeline AIoT hoàn chỉnh
- Train AI model thành công
- Deploy FastAPI API
- Sinh decision log
- Phát hiện anomaly
- Tạo safety layer cho kho lạnh
