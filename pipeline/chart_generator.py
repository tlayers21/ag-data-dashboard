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

        df[color_axis] = df[color_axis].astype(str)
    elif year_type == "marketing":
        x_axis = "marketing_year_week"
        color_axis = "marketing_year"
        file_suffix = "my"
        title_year = "Marketing Year"

        mapping = {
            2026: "2025/2026",
            2025: "2024/2025",
            2024: "2023/2024",
            2023: "2022/2023",
            2022: "2021/2022",
            2021: "2020/2021",
        }
        df[color_axis] = df[color_axis].map(mapping)
    else:
        raise ValueError("year_type must be either 'calendar' or 'marketing'")

    unit = df["unit"].iloc[0]
    latest_date = df["week_ending_date"].iloc[0]
    latest_date = pd.to_datetime(latest_date).strftime("%Y-%m-%d")

    figure = px.line(
        df,
        x=x_axis,
        y=value_column,
        color=color_axis,
        markers=True,
        custom_data=["week_ending_date", value_column],
        title=(
            f"Weekly U.S. {commodity.title()} {value_column.replace("_", " ").title()}<br>"
            f"to {country.title()} (as of {latest_date})"
        ),
        labels={
            x_axis: f"{title_year} Week",
            value_column: f"{unit}",
            color_axis: title_year
        }
    )

    # Format x-axis
    df["week_ending_date"] = pd.to_datetime(df["week_ending_date"])
    tick_weeks = [2, 9, 16, 23, 30, 37, 44, 51]
    tick_rows = df[df["marketing_year_week"].isin(tick_weeks)]
    tick_map = dict(zip(
        tick_rows["marketing_year_week"],
        tick_rows["week_ending_date"].dt.strftime("%b-%d")
    ))

    figure.update_xaxes(
        tickmode="array",
        tickvals=list(tick_map.keys()),
        ticktext=list(tick_map.values()),
        tickangle=0,
        tickfont=dict(size=10)
    )

    latest_year_raw= df[color_axis].max()
    latest_year_key = str(latest_year_raw).split("/")[0]

    latest_trace = None

    for trace in figure.data:
        trace_label = str(trace.name)
        trace_first = trace_label.split("/")[0]

        if trace_first == latest_year_key:
            trace.update(
                line=dict(width=4, color="red"),
                marker=dict(size=7),
                name=f"<b>{trace_label}</b>"
            )
            latest_trace = trace
        else:
            trace.update(
                line=dict(width=2),
                marker=dict(size=6),
                opacity=0.6
            )
    if latest_trace is not None:
        figure.data = tuple(reversed(figure.data))

    figure.update_layout(
        title={
            "text": figure.layout.title.text,
            "x": 0.5,
            "xanchor": "center"
        },
        legend=dict(
            title_text="",
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5,
            entrywidth=100
        )
    )

    for i, trace in enumerate(figure.data):
        trace.update(legendrank=len(figure.data) - i)

    figure.update_xaxes(showgrid=True, gridcolor="lightgray", gridwidth=0.5)
    figure.update_yaxes(showgrid=True, gridcolor="lightgray", gridwidth=0.5, tickfont=dict(size=11))
    figure.update_layout(plot_bgcolor="white", paper_bgcolor="white")

    figure.update_traces(
        hovertemplate=
        f"{commodity.title()}: %{{customdata[1]:,}}<br>"
        f"Week ending: %{{customdata[0]|%b-%d-%Y}}<extra></extra>"
    )

    json_dir = Path("frontend/public").resolve()
    figure_dir = Path("frontend/figures").resolve()

    json_path = (
        json_dir
         / f"us_{commodity.lower()}_to_{country.lower()}_{value_column}_last_5_years_{file_suffix}.json"
    )

    pio.write_json(figure, str(json_path))

    """
    png_path = (
        figure_dir
         / f"us_{commodity.lower()}_to_{country.lower()}_{value_column}_last_5_years_{file_suffix}.png"
    )

    pio.write_image(figure, str(png_path))
    """

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
    generate_weekly_chart("esr", "corn", "world", "weekly_exports", "marketing")
    generate_weekly_chart("esr", "corn", "world", "current_marketing_year_total_commitment", "marketing")
    generate_weekly_chart("esr", "corn", "world", "next_marketing_year_outstanding_sales", "marketing")

    generate_weekly_chart("inspections", "wheat", "world", "inspections", "marketing")
    generate_weekly_chart("esr", "wheat", "world", "weekly_exports", "marketing")
    generate_weekly_chart("esr", "wheat", "world", "current_marketing_year_total_commitment", "marketing")
    generate_weekly_chart("esr", "wheat", "world", "next_marketing_year_outstanding_sales", "marketing")

    generate_weekly_chart("inspections", "soybeans", "world", "inspections", "marketing")
    generate_weekly_chart("esr", "soybeans", "world", "weekly_exports", "marketing")
    generate_weekly_chart("esr", "soybeans", "world", "current_marketing_year_total_commitment", "marketing")
    generate_weekly_chart("esr", "soybeans", "world", "next_marketing_year_outstanding_sales", "marketing")

    print("Done.")
    