from pathlib import Path

required_files = [
    "data/processed/telemetry_clean.csv",
    "data/processed/feature_dataset.csv",
    "models/cold_storage_model.joblib",
    "outputs/metrics.json",
    "outputs/decision_log.csv"
]

missing = []

for file in required_files:

    if not Path(file).exists():
        missing.append(file)

if len(missing) == 0:
    print(
        "PROJECT CHECK PASSED: Notebook outputs and model artifacts are complete."
    )
else:
    print("MISSING FILES:")

    for file in missing:
        print(file)