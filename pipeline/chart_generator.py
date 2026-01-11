import pandas as pd
import plotly.express as px
import plotly.io as pio
from pathlib import Path
from .api_client import fetch_data_last5years
from .config import COMMODITIES, ESR_COUNTRY_NAMES

def generate_weekly_chart(
        data: str,
        commodity: str,
        country: str,
        value_column: str,
        year_type: str,
        home: bool
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
    latest_date = df["date_collected"].iloc[0]
    latest_date = pd.to_datetime(latest_date).strftime("%m/%d/%Y")

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
            x_axis: f"Week Ending Date",
            value_column: f"{unit}",
            color_axis: title_year
        }
    )

    # Format x-axis
    df["week_ending_date"] = pd.to_datetime(df["week_ending_date"])
    tick_weeks = [2, 9, 16, 23, 30, 37, 44, 51]
    if year_type == "marketing":
        tick_rows = df[df["marketing_year_week"].isin(tick_weeks)]
        tick_map = dict(zip(
            tick_rows["marketing_year_week"],
            tick_rows["week_ending_date"].dt.strftime("%b-%d")
        ))
    else:
        tick_rows = df[df["calendar_week"].isin(tick_weeks)]
        tick_map = dict(zip(
            tick_rows["calendar_week"],
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

    if home:
        json_path = (
            json_dir
             / f"{data}_us_{commodity.lower().replace(" ", "_")}_to_{country.lower().replace(" ", "_")}_{value_column}_last_5_years_{file_suffix}_home.json"
        )
    else:
        json_path = (
            json_dir
             / f"{data}_us_{commodity.lower().replace(" ", "_")}_to_{country.lower().replace(" ", "_")}_{value_column}_last_5_years_{file_suffix}.json"
        )

    pio.write_json(figure, str(json_path))

def generate_charts() -> None:
    print("Creating all charts...")

    for name, cfg in COMMODITIES.items():
        esr_info = cfg.get("esr")
    
        countries = esr_info["countries"]

        generate_weekly_chart("esr", name, "world", value_column="weekly_exports", year_type="marketing", home=False)
        generate_weekly_chart("esr", name, "world", value_column="accumulated_exports", year_type="marketing", home=False)
        generate_weekly_chart("esr", name, "world", value_column="outstanding_sales", year_type="marketing", home=False)
        generate_weekly_chart("esr", name, "world", value_column="gross_new_sales", year_type="marketing", home=False)
        generate_weekly_chart("esr", name, "world", value_column="current_marketing_year_net_sales", year_type="marketing", home=False)
        generate_weekly_chart("esr", name, "world", value_column="current_marketing_year_total_commitment", year_type="marketing", home=False)
        generate_weekly_chart("esr", name, "world", value_column="next_marketing_year_outstanding_sales", year_type="marketing", home=False)
        generate_weekly_chart("esr", name, "world", value_column="next_marketing_year_net_sales", year_type="marketing", home=False)
        generate_weekly_chart("esr", name, "world", value_column="weekly_exports", year_type="calendar", home=False)
        generate_weekly_chart("esr", name, "world", value_column="accumulated_exports", year_type="calendar", home=False)
        generate_weekly_chart("esr", name, "world", value_column="outstanding_sales", year_type="calendar", home=False)
        generate_weekly_chart("esr", name, "world", value_column="gross_new_sales", year_type="calendar", home=False)
        generate_weekly_chart("esr", name, "world", value_column="current_marketing_year_net_sales", year_type="calendar", home=False)
        generate_weekly_chart("esr", name, "world", value_column="current_marketing_year_total_commitment", year_type="calendar", home=False)
        generate_weekly_chart("esr", name, "world", value_column="next_marketing_year_outstanding_sales", year_type="calendar", home=False)
        generate_weekly_chart("esr", name, "world", value_column="next_marketing_year_net_sales", year_type="calendar", home=False)
        if name not in ["soybean oil", "soybean meal"]:
            generate_weekly_chart("inspections", name, "world", "export_inspections", "marketing", home=False)
            generate_weekly_chart("inspections", name, "world", "export_inspections", "calendar", home=False)

        for country_code in countries:
            country = ESR_COUNTRY_NAMES.get(country_code)

            generate_weekly_chart("esr", name, country, value_column="weekly_exports", year_type="marketing", home=False)
            generate_weekly_chart("esr", name, country, value_column="accumulated_exports", year_type="marketing", home=False)
            generate_weekly_chart("esr", name, country, value_column="outstanding_sales", year_type="marketing", home=False)
            generate_weekly_chart("esr", name, country, value_column="gross_new_sales", year_type="marketing", home=False)
            generate_weekly_chart("esr", name, country, value_column="current_marketing_year_net_sales", year_type="marketing", home=False)
            generate_weekly_chart("esr", name, country, value_column="current_marketing_year_total_commitment", year_type="marketing", home=False)
            generate_weekly_chart("esr", name, country, value_column="next_marketing_year_outstanding_sales", year_type="marketing", home=False)
            generate_weekly_chart("esr", name, country, value_column="next_marketing_year_net_sales", year_type="marketing", home=False)

            generate_weekly_chart("esr", name, country, value_column="weekly_exports", year_type="calendar", home=False)
            generate_weekly_chart("esr", name, country, value_column="accumulated_exports", year_type="calendar", home=False)
            generate_weekly_chart("esr", name, country, value_column="outstanding_sales", year_type="calendar", home=False)
            generate_weekly_chart("esr", name, country, value_column="gross_new_sales", year_type="calendar", home=False)
            generate_weekly_chart("esr", name, country, value_column="current_marketing_year_net_sales", year_type="calendar", home=False)
            generate_weekly_chart("esr", name, country, value_column="current_marketing_year_total_commitment", year_type="calendar", home=False)
            generate_weekly_chart("esr", name, country, value_column="next_marketing_year_outstanding_sales", year_type="calendar", home=False)
            generate_weekly_chart("esr", name, country, value_column="next_marketing_year_net_sales", year_type="calendar", home=False)

    print("Done.")

def generate_home_page_charts() -> None:
    print("Generating home page charts...")

    generate_weekly_chart("inspections", "corn", "world", "export_inspections", "marketing", home=True)
    generate_weekly_chart("esr", "corn", "world", "gross_new_sales", "marketing", home=True)
    generate_weekly_chart("esr", "corn", "world", "current_marketing_year_total_commitment", "marketing", home=True)
    generate_weekly_chart("esr", "corn", "world", "next_marketing_year_outstanding_sales", "marketing", home=True)

    generate_weekly_chart("inspections", "wheat", "world", "export_inspections", "marketing", home=True)
    generate_weekly_chart("esr", "wheat", "world", "gross_new_sales", "marketing", home=True)
    generate_weekly_chart("esr", "wheat", "world", "current_marketing_year_total_commitment", "marketing", home=True)
    generate_weekly_chart("esr", "wheat", "world", "next_marketing_year_outstanding_sales", "marketing", home=True)

    generate_weekly_chart("inspections", "soybeans", "world", "export_inspections", "marketing", home=True)
    generate_weekly_chart("esr", "soybeans", "world", "gross_new_sales", "marketing", home=True)
    generate_weekly_chart("esr", "soybeans", "world", "current_marketing_year_total_commitment", "marketing", home=True)
    generate_weekly_chart("esr", "soybeans", "world", "next_marketing_year_outstanding_sales", "marketing", home=True)

    print("Done.\n==========")
    