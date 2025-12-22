from fastapi import FastAPI
import pandas as pd
from pathlib import Path

app = FastAPI(title="Corn Exports API",version="1.0")

# Load Processed Data
processed_path = Path("/Users/tommyayers/projects/project1/data/processed/corn_exports_2025.csv")
weekly_data = pd.read_csv(processed_path, parse_dates=["date"])
commentary_path = Path("/Users/tommyayers/projects/project1/data/processed/corn_exports_2025_commentary.txt")
with open(commentary_path, "r") as f:
    commentary = f.read()

# Example health check (hardcoded for now)
@app.get("/health")
def health():
    return {"status": "ok"}

# Weekly Export Data
@app.get("/exports")
def get_exports():
    return weekly_data.to_dict(orient="records")

# Commentary
@app.get("/commentary")
def get_commentary():
    return {"commentary": commentary}

# Summary Metrics
@app.get("/metrics")
def get_metrics():
    total_exports = weekly_data["weekly_exports_mt"].sum()
    avg_weekly = weekly_data["weekly_exports_mt"].mean()
    peak_week = weekly_data.loc[weekly_data["weekly_exports_mt"].idxmax()]

    return {
        "total_exports_mt": int(total_exports),
        "avg_weekly_mt": float(avg_weekly),
        "peak_week_date": str(peak_week["date"]),
        "peak_week_exports_mt": int(peak_week["weekly_exports_mt"])
    }