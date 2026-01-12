from fastapi import FastAPI
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime, timedelta
from pipeline.config import DATA_BASE_URL

app = FastAPI()
engine = create_engine(DATA_BASE_URL)

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

# Fetches data from last 5 years dependent on the 3 types of data: ESR, PSD, and inspections (allows for some leeway)
def fetch_last_5_years(data: str, commodity: str, country: str) -> list[dict]:
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

    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

# Fetches ESR data from last 5 years
@app.get("/esr/last5years")
def get_last_5_years_esr(commodity: str, country: str) -> list[dict]:
    return fetch_last_5_years("esr", commodity, country)

# Fetches PSD data from last 5 years
@app.get("/psd/last5years")
def get_last_5_years_esr(commodity: str, country: str) -> list[dict]:
    return fetch_last_5_years("psd", commodity, country)

# Fetches export inspections data from last 5 years
@app.get("/inspections/last5years")
def get_last_5_years_esr(commodity: str, country: str) -> list[dict]:
    return fetch_last_5_years("inspections", commodity, country)