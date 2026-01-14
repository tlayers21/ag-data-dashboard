from fastapi import FastAPI
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os
from pathlib import Path
from typing import List, Dict, Any
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime, timedelta

load_dotenv()
POSTGRES_URL = os.getenv("POSTGRES_URL")

CHART_DIR = Path(__file__).parent / "charts"
# For Render
CHART_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tlayers21.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/generate-charts")
def generate_charts_endpoint():
    from pipeline.chart_generator import generate_charts
    generate_charts()
    return {"status": "ok"}

@app.get("/debug/charts")
def debug_charts():
    return [f.name for f in CHART_DIR.glob("*.json")]

engine = create_engine(POSTGRES_URL)

@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}

@app.get("/maintenance")
def maintenance_status() -> Dict[str, bool]:
    return {"active": os.path.exists("maintenance.flag")}

# Fetches data from last 5 years dependent on the 3 types of data: ESR, PSD, and inspections (allows for some leeway)
def fetch_last_5_years(data: str, commodity: str, country: str) -> List[Dict[str, Any]]:
    cutoff_year = datetime.now().year - 6
    
    if data == "psd":
        data_column = "calendar_year"
        cutoff = cutoff_year
    else:
        data_column = "week_ending_date"
        cutoff = (datetime.now() - timedelta(days=5*365 + 134)).strftime("%Y-%m-%d")

    commodity = commodity.strip().lower()
    country = country.strip().lower()

    query = f"""
        SELECT *
        from {data}
        WHERE {data_column} >= {cutoff if data == 'psd' else f"'{cutoff}'"}
        AND commodity = '{commodity}'
        AND country = '{country}'
        ORDER BY {data_column} DESC;
    """

    with engine.begin() as conn:
        df = pd.read_sql(query, conn)

    return df.to_dict(orient="records")

# Fetches ESR data from last 5 years
@app.get("/esr/last5years")
def get_last_5_years_esr(commodity: str, country: str) -> List[Dict[str, Any]]:
    return fetch_last_5_years("esr", commodity, country)

# Fetches PSD data from last 5 years
@app.get("/psd/last5years")
def get_last_5_years_psd(commodity: str, country: str) -> List[Dict[str, Any]]:
    return fetch_last_5_years("psd", commodity, country)

# Fetches export inspections data from last 5 years
@app.get("/inspections/last5years")
def get_last_5_years_inspections(commodity: str, country: str) -> List[Dict[str, Any]]:
    return fetch_last_5_years("inspections", commodity, country)

# Fetches JSON flie to build Plotly chart for specific commodity page
@app.get("/api/{commodity}/{source}/{country}/{datatype}/{year}")
def get_chart(commodity: str, source: str, country: str, datatype: str, year: str):
    source = source.lower()
    commodity = commodity.lower()
    country = country.lower()
    datatype = datatype.lower()
    year = year.lower()

    # PSD pattern
    if source == "psd":
        filename = (
            f"{source}_{commodity}_for_{country}_{datatype}_last_5_years_{year}.json"
        )

    # ESR or Inspections pattern
    else:
        filename = (
            f"{source}_us_{commodity}_to_{country}_{datatype}_last_5_years_{year}.json"
        )

    file_path = CHART_DIR / filename

    if not file_path.exists():
        return {"error": f"Chart not found: {filename}"}

    return FileResponse(file_path)

# Fetches JSON flie to build Plotly chart for specific home page
@app.get("/api/home/{commodity}/{source}/{country}/{datatype}/{year}")
def get_home_chart(commodity: str, source: str, country: str, datatype: str, year: str):
    filename = (
        f"{source}_us_{commodity}_to_{country}_{datatype}_last_5_years_{year}_home.json"
    )
    file_path = CHART_DIR / filename

    if not file_path.exists():
        return {"error": f"Chart not found: {filename}"}

    return FileResponse(file_path)
