import requests
import pandas as pd
import plotly.express as px
import plotly.io as pio
from pathlib import Path

API_BASE = "http://localhost:8000"

def fetch_data_last5years(data: str, commodity: str, country: str) -> list:
    params = {
        "commodity": commodity.lower(),
        "country": country.lower()
    }

    url = f"{API_BASE}/{data}/weekly/last5years"
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return []
        
    try:
        return response.json()
    except Exception:
        print("Database Fetching Error: Response was not valid JSON")
        return []

def generate_weekly_chart(
        data: str,
        commodity: str,
        country: str,
        value_column: str,
        year_type: str
) -> None:
    df_data = fetch_data_last5years(data, commodity, country)
    df = pd.DataFrame(df_data)

    if year_type == "calendar":
        x_axis = "calendar_week"
        color_axis = "calendar_year"
        file_suffix = "cal"
        title_year = "Calendar Year"
    elif year_type == "marketing":
        x_axis = "marketing_year_week"
        color_axis = "marketing_year"
        file_suffix = "my"
        title_year = "Marketing Year"
    else:
        raise ValueError("year_type must be either 'calendar' or 'marketing'")

    unit = df["unit"].iloc[0]

    figure = px.line(
        df,
        x=x_axis,
        y=value_column,
        color=color_axis,
        markers=True,
        title=f"Weekly U.S. {commodity.title()} {value_column} to {country.title()} ({title_year})",
        labels={
            x_axis: f"{title_year} Week",
            value_column: f"{value_column.title()} ({unit})",
            color_axis: title_year
        }
    )

    json_dir = Path("frontend/public").resolve()
    figure_dir = Path("frontend/figures").resolve()

    json_path = (
        json_dir
         / f"us_{commodity.lower()}_to_{country.lower()}_{value_column}_last_5_years_{file_suffix}.json"
    )

    pio.write_json(figure, str(json_path))

    png_path = (
        figure_dir
         / f"us_{commodity.lower()}_to_{country.lower()}_{value_column}_last_5_years_{file_suffix}.png"
    )

    pio.write_image(figure, str(png_path))

"""
def generate_charts() -> None:
    print("Creating all charts...")
    generate_weekly_chart("esr", "corn", "world", "weekly_exports", "calendar")
    generate_weekly_chart("esr", "corn", "world", "weekly_exports", "marketing")
    generate_weekly_chart("inspections", "corn", "world", "inspections", "calendar")
    generate_weekly_chart("inspections", "corn", "world", "inspections", "marketing")

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
"""

def generate_home_page_charts() -> None:
    print("Generating home page charts...")

    generate_weekly_chart("inspections", "corn", "world", "inspections", "marketing")
    generate_weekly_chart("esr", "corn", "world", "accumulated_exports", "marketing")
    generate_weekly_chart("esr", "corn", "world", "current_marketing_year_total_commitment", "marketing")

    generate_weekly_chart("inspections", "wheat", "world", "inspections", "marketing")
    generate_weekly_chart("esr", "wheat", "world", "accumulated_exports", "marketing")
    generate_weekly_chart("esr", "wheat", "world", "current_marketing_year_total_commitment", "marketing")

    generate_weekly_chart("inspections", "soybeans", "world", "inspections", "marketing")
    generate_weekly_chart("esr", "soybeans", "world", "accumulated_exports", "marketing")
    generate_weekly_chart("esr", "soybeans", "world", "current_marketing_year_total_commitment", "marketing")
    