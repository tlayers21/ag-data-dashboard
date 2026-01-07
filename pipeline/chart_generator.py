import requests
import pandas as pd
import plotly.express as px
import plotly.io as pio
from pathlib import Path
from .config import COMMODITIES, ESR_COUNTRY_NAMES

API_BASE = "http://localhost:8000"

def fetch_esr_last5years(commodity: str, country: str) -> list:
    params = {
        "commodity": commodity.lower(),
        "country": country.lower()
    }

    url = f"{API_BASE}/esr/weekly/last5years"
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return []
        
    try:
        return response.json()
    except Exception:
        print("Database Fetching Error: Response was not valid JSON")
        return []

def generate_weekly_chart_calendar_year(commodity: str, country: str, value_column: str) -> None:
    data = fetch_esr_last5years(commodity, country)
    df = pd.DataFrame(data)

    unit = df["unit"].iloc[0]

    figure = px.line(
        df,
        x="calendar_week",
        y=f"{value_column}",
        color="calendar_year",
        markers=True,
        title=f"Weekly U.S. {commodity.title()} {value_column} to {country.title()} (Calendar Year)",
        labels={
            "calendar_week": "Calendar Week",
            f"{value_column}": f"Weekly Exports ({unit})",
            "calendar_year": "Calendar Year"
        }
    )

    json_dir = Path("dashboard/json").resolve()
    figure_dir = Path("dashboard/figures").resolve()

    json_path = (
        json_dir
         / f"us_{commodity.lower()}_to_{country.lower()}_{value_column}_last_5_years_cal.json"
    )

    pio.write_json(figure, str(json_path))

    png_path = (
        figure_dir
         / f"us_{commodity.lower()}_to_{country.lower()}_{value_column}_last_5_years_cal.png"
    )

    pio.write_image(figure, str(png_path))

def generate_weekly_chart_marketing_year(commodity: str, country: str, value_column: str) -> None:
    data = fetch_esr_last5years(commodity, country)
    df = pd.DataFrame(data)

    unit = df["unit"].iloc[0]

    figure = px.line(
        df,
        x="marketing_year_week",
        y=f"{value_column}",
        color="marketing_year",
        markers=True,
        title=f"Weekly U.S. {commodity.title()} {value_column} to {country.title()} (Marketing Year)",
        labels={
            "marketing_year_week": "Marketing Year Week",
            f"{value_column}": f"Weekly Exports ({unit})",
            "marketing_year": "Marketing Year"
        }
    )

    json_dir = Path("dashboard/json").resolve()
    figure_dir = Path("dashboard/figures").resolve()

    json_path = (
        json_dir
         / f"us_{commodity.lower()}_to_{country.lower()}_{value_column}_last_5_years_my.json"
    )

    pio.write_json(figure, str(json_path))

    png_path = (
        figure_dir
         / f"us_{commodity.lower()}_to_{country.lower()}_{value_column}_last_5_years_my.png"
    )

    pio.write_image(figure, str(png_path))

def generate_charts() -> None:
    print("Creating all charts...")

    for name, cfg in COMMODITIES.items():
        esr_info = cfg.get("esr")
    
        countries = esr_info["countries"]

        generate_weekly_chart_calendar_year(name, "world", value_column="current_marketing_year_total_commitment")
        generate_weekly_chart_marketing_year(name, "world", value_column="current_marketing_year_total_commitment")

        for country_code in countries:
            country = ESR_COUNTRY_NAMES.get(country_code)
            generate_weekly_chart_calendar_year(name, country, value_column="current_marketing_year_total_commitment")
            generate_weekly_chart_marketing_year(name, country, value_column="current_marketing_year_total_commitment")
    
    print("Done.")