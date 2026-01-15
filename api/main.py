from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from pathlib import Path
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime, timedelta
from pipeline.chart_generator import generate_weekly_esr_or_inspections_chart, generate_weekly_psd_chart
from pipeline.commentary_generator import generate_home_page_commentary

load_dotenv()
POSTGRES_URL = os.getenv("POSTGRES_URL")

# For Render
CHART_DIR = Path(__file__).parent / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)
COMMENTARY_DIR = Path(__file__).parent / "commentary"

app = FastAPI()

# Grants access for site to use API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tlayers21.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine(POSTGRES_URL)

@app.get("/health")
def health():
    return {"status": "ok"}

# Fetches data from last 5 years dependent on the 3 types of data: ESR, PSD, and inspections (allows for some leeway)
def fetch_last_5_years(data: str, commodity: str, country: str):
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
def get_last_5_years_esr(commodity: str, country: str):
    return fetch_last_5_years("esr", commodity, country)

# Fetches PSD data from last 5 years
@app.get("/psd/last5years")
def get_last_5_years_psd(commodity: str, country: str):
    return fetch_last_5_years("psd", commodity, country)

# Fetches export inspections data from last 5 years
@app.get("/inspections/last5years")
def get_last_5_years_inspections(commodity: str, country: str):
    return fetch_last_5_years("inspections", commodity, country)

# TODO: Make these more efficient so users don't have to wait as long for API to communicate chart and commentary information

# Fetches JSON file to build Plotly chart for specific commodity page
@app.get("/api/{commodity}/{source}/{country}/{datatype}/{year}")
def get_chart(commodity: str, source: str, country: str, data_type: str, year_type: str):
    year = "marketing" if year_type == "my" else "calendar"

    # PSD
    if source == "psd":
        generate_weekly_psd_chart(
            source,
            commodity,
            country,
            data_type
        )
        filename = (
            f"{source}_{commodity}_for_{country}_{data_type}_last_5_years_{year_type}.json"
        )

    # ESR or inspections
    else:
        generate_weekly_esr_or_inspections_chart(
            source,
            commodity,
            country,
            data_type,
            year,
            home=False
        )
        filename = (
            f"{source}_us_{commodity}_to_{country}_{data_type}_last_5_years_{year_type}.json"
        )

    file_path = CHART_DIR / filename

    if not file_path.exists():
        return {"error": f"Chart not found: {filename}"}

    return FileResponse(file_path)

# Fetches JSON file to build Plotly chart for specific home page
@app.get("/api/home/{commodity}/{source}/{country}/{datatype}/{year}")
def get_home_chart(commodity: str, source: str, country: str, data_type: str, year_type: str):
    year = "marketing" if year == "my" else "calendar"
    
    generate_weekly_esr_or_inspections_chart(
            source,
            commodity,
            country,
            data_type,
            year,
            home=True
        )
    filename = (
        f"{source}_us_{commodity}_to_{country}_{data_type}_last_5_years_{year_type}_home.json"
    )
    file_path = CHART_DIR / filename

    if not file_path.exists():
        return {"error": f"Chart not found: {filename}"}

    return FileResponse(file_path)

# Fetches commentary for home page
@app.get("/commentary")
@app.get("/commentary/home")
def get_home_commentary():
    generate_home_page_commentary()

    texts = []
    for file in sorted(COMMENTARY_DIR.glob("*.txt")):
        with open(file, "r", encoding="utf-8") as f:
            texts.append(f.read())

    combined = "\n\n".join(texts)

    return combined