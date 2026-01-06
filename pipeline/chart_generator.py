import requests
import pandas as pd
import plotly.express as px
import plotly.io as pio
from pathlib import Path

API_BASE = "http://localhost:8000"

def fetch_exports_last5years(commodity: str, country: str) -> list:
    params = {
        "commodity": commodity.lower(),
        "country": country.lower()
    }

    url = f"{API_BASE}/exports/weekly/last5years"
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return []
        
    try:
        return response.json()
    except Exception:
        print("Database Fetching Error: Response was not valid JSON")
        return []

def generate_weekly_exports_chart_calendar_year(commodity: str, country: str):
    print(f"Creating chart for calendar year {commodity} exports to {country}...")
    data = fetch_exports_last5years(commodity, country)
    df = pd.DataFrame(data)
    unit = df["unit"].iloc[0]

    figure = px.line(
        df,
        x="calendar_week",
        y="weekly_exports",
        color="calendar_year",
        markers=True,
        title=f"Weekly U.S. {commodity.title()} Exports to {country.title()} (Calendar Year)",
        labels={
            "calendar_week": "Calendar Week",
            "weekly_exports": f"Weekly Exports ({unit})",
            "calendar_year": "Calendar Year"
        }
    )

    out_dir = Path("dashboard/figures").resolve()

    json_path = (
        out_dir
         / f"united_states_exports_{commodity.lower()}_{country.lower()}_weekly_exports_last_5_years_cal.json"
    )

    pio.write_json(figure, str(json_path))

    png_path = (
        out_dir
         / f"united_states_exports_{commodity.lower()}_{country.lower()}_weekly_exports_last_5_years_cal.png"
    )

    pio.write_image(figure, str(png_path))

    print("Done.")

def generate_weekly_exports_chart_marketing_year(commodity: str, country: str):
    print(f"Creating chart for marketing year {commodity} exports to {country}...")
    data = fetch_exports_last5years(commodity, country)
    df = pd.DataFrame(data)
    unit = df["unit"].iloc[0]

    figure = px.line(
        df,
        x="marketing_year_week",
        y="weekly_exports",
        color="marketing_year",
        markers=True,
        title=f"Weekly U.S. {commodity.title()} Exports to {country.title()} (Marketing Year)",
        labels={
            "marketing_year_week": "Marketing Year Week",
            "weekly_exports": f"Weekly Exports ({unit})",
            "marketing_year": "Marketing Year"
        }
    )

    out_dir = Path("dashboard/figures").resolve()

    json_path = (
        out_dir
         / f"united_states_exports_{commodity.lower()}_{country.lower()}_weekly_exports_last_5_years_my.json"
    )

    pio.write_json(figure, str(json_path))

    png_path = (
        out_dir
         / f"united_states_exports_{commodity.lower()}_{country.lower()}_weekly_exports_last_5_years_my.png"
    )

    pio.write_image(figure, str(png_path))

    print("Done.")