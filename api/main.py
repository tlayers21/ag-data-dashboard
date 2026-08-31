from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import time
from pathlib import Path
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime, timedelta
from pipeline.chart_generator import generate_weekly_esr_or_inspections_chart, generate_weekly_psd_chart
from pipeline.commentary_generator import generate_home_page_commentary

load_dotenv()
POSTGRES_URL = os.getenv("POSTGRES_URL")

CHART_DIR = Path(__file__).parent / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)
COMMENTARY_DIR = Path(__file__).parent / "commentary"
CHART_TTL_SECONDS = int(os.getenv("CHART_TTL_SECONDS", "3600"))
CATALOG_TTL_SECONDS = int(os.getenv("CATALOG_TTL_SECONDS", "3600"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine(POSTGRES_URL)

@app.get("/health")
def health():
    return {"status": "ok"}

# Charts only change when the pipeline reloads the tables, so reuse a recent file
def is_fresh(path: Path) -> bool:
    return path.exists() and (time.time() - path.stat().st_mtime) < CHART_TTL_SECONDS

# Columns that describe a row rather than hold a plottable value
DIMENSION_COLUMNS = {
    "date_collected", "week_ending_date", "calendar_year", "marketing_year",
    "calendar_month", "marketing_year_month", "calendar_week",
    "marketing_year_week", "commodity", "country", "unit", "attribute", "amount",
}

_catalog = {}

# The values that actually exist in the database, so unknown ones are rejected
# before they reach a query or create a cache entry
def get_catalog() -> dict:
    if _catalog and time.time() - _catalog["loaded_at"] < CATALOG_TTL_SECONDS:
        return _catalog

    commodities, countries, datatypes = set(), set(), set()
    with engine.begin() as conn:
        for table in TABLE_DATE_COLUMNS:
            commodities |= {
                r[0] for r in conn.execute(text(f"SELECT DISTINCT commodity FROM {table}"))
            }
            countries |= {
                r[0] for r in conn.execute(text(f"SELECT DISTINCT country FROM {table}"))
            }
            if table == "psd":
                datatypes |= {
                    r[0].lower().replace(" ", "_")
                    for r in conn.execute(text("SELECT DISTINCT attribute FROM psd"))
                }
            else:
                columns = {
                    r[0] for r in conn.execute(
                        text(
                            "SELECT column_name FROM information_schema.columns "
                            "WHERE table_schema = 'public' AND table_name = :table"
                        ),
                        {"table": table},
                    )
                }
                datatypes |= columns - DIMENSION_COLUMNS

    _catalog.update(
        loaded_at=time.time(),
        commodities=commodities,
        countries=countries,
        datatypes=datatypes,
    )
    return _catalog


def validate_params(commodity: str, country: str, datatype: str | None = None) -> None:
    catalog = get_catalog()
    if commodity not in catalog["commodities"]:
        raise HTTPException(status_code=404, detail=f"Unknown commodity: {commodity}")
    if country not in catalog["countries"]:
        raise HTTPException(status_code=404, detail=f"Unknown country: {country}")
    if datatype is not None and datatype not in catalog["datatypes"]:
        raise HTTPException(status_code=404, detail=f"Unknown data type: {datatype}")

TABLE_DATE_COLUMNS = {
    "esr": "week_ending_date",
    "psd": "calendar_year",
    "inspections": "week_ending_date",
}

# Fetches data from last 5 years dependent on the 3 types of data: ESR, PSD, and inspections (allows for some leeway)
def fetch_last_5_years(data: str, commodity: str, country: str):
    data_column = TABLE_DATE_COLUMNS.get(data)
    if data_column is None:
        raise HTTPException(status_code=404, detail=f"Unknown data source: {data}")

    commodity = commodity.strip().lower()
    country = country.strip().lower()
    validate_params(commodity, country)

    if data == "psd":
        cutoff = datetime.now().year - 6
    else:
        # Midnight of the cutoff day, matching the old date-only comparison
        cutoff = (datetime.now() - timedelta(days=5*365 + 134)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

    query = text(f"""
        SELECT *
        FROM {data}
        WHERE {data_column} >= :cutoff
        AND commodity = :commodity
        AND country = :country
        ORDER BY {data_column} DESC;
    """)

    params = {
        "cutoff": cutoff,
        "commodity": commodity,
        "country": country,
    }

    with engine.begin() as conn:
        df = pd.read_sql(query, conn, params=params)

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

# Fetches JSON flie to build Plotly chart for specific commodity page
@app.get("/api/{commodity}/{source}/{country}/{datatype}/{year}")
def get_chart(commodity: str, source: str, country: str, datatype: str, year: str):
    source = source.lower()
    commodity = commodity.lower()
    country = country.lower()
    datatype = datatype.lower()
    year = year.lower()
    year_type = "marketing" if year == "my" else "calendar"

    if source not in TABLE_DATE_COLUMNS:
        raise HTTPException(status_code=404, detail=f"Unknown data source: {source}")
    validate_params(commodity, country, datatype)

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

    if not is_fresh(file_path):
        if source == "psd":
            generate_weekly_psd_chart(
                source,
                commodity,
                country,
                datatype
            )
        else:
            generate_weekly_esr_or_inspections_chart(
                source,
                commodity,
                country,
                datatype,
                year_type,
                home=False
            )

    if not file_path.exists():
        return {"error": f"Chart not found: {filename}"}

    return FileResponse(file_path)

# Fetches JSON file to build Plotly chart for specific home page
@app.get("/api/home/{commodity}/{source}/{country}/{datatype}/{year}")
def get_home_chart(commodity: str, source: str, country: str, datatype: str, year: str):
    year_type = "marketing" if year == "my" else "calendar"

    if source not in TABLE_DATE_COLUMNS:
        raise HTTPException(status_code=404, detail=f"Unknown data source: {source}")
    validate_params(commodity, country, datatype)

    filename = (
        f"{source}_us_{commodity}_to_{country}_{datatype}_last_5_years_{year}_home.json"
    )
    file_path = CHART_DIR / filename

    if not is_fresh(file_path):
        generate_weekly_esr_or_inspections_chart(
            source,
            commodity,
            country,
            datatype,
            year_type,
            home=True
        )

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