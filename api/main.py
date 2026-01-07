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

@app.get("/esr/weekly/last5years")
def get_last_5_years_esr(commodity: str, country: str) -> list:
    ten_years_ago = datetime.now() - timedelta(days=5*365 + 1)
    cutoff = ten_years_ago.strftime("%Y-%m-%d")
    
    query = f"""
        SELECT *
        from esr
        WHERE week_ending_date >= '{cutoff}'
    """

    # Commodity filter
    query += f" AND LOWER(commodity) = '{commodity}'"
    # Country filter (country will be world if world)
    query += f" AND LOWER(country) ='{country}'"
    query += f" ORDER BY week_ending_date ASC;"

    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")