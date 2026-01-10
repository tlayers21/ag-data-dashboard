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

def fetch_last_5_years(data: str, commodity: str, country: str) -> list[dict]:
    five_years_ago = datetime.now() - timedelta(days=5*365 + 134)
    cutoff = five_years_ago.strftime("%Y-%m-%d")
    
    query = f"""
        SELECT *
        from {data}
        WHERE week_ending_date >= '{cutoff}'
    """

    # Commodity filter
    query += f" AND LOWER(commodity) = '{commodity}'"
    # Country filter (country will be world if world for esr)
    query += f" AND LOWER(country) = '{country}'"

    query += f" ORDER BY week_ending_date DESC;"

    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

@app.get("/esr/weekly/last5years")
def get_last_5_years_esr(commodity: str, country: str) -> list[dict]:
    return fetch_last_5_years("esr", commodity, country)

@app.get("/inspections/weekly/last5years")
def get_last_5_years_esr(commodity: str, country: str) -> list[dict]:
    return fetch_last_5_years("inspections", commodity, country)