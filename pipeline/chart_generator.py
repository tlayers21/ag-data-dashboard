import pandas as pd
import plotly.express as px
import plotly.io as pio
from pathlib import Path
from .agdata_api_client import AgDataClient
from .config import COMMODITIES, ESR_COUNTRY_NAMES, PSD_COUNTRY_NAMES

# Generates a weekly ESR or inspections chart for a given data set
def generate_weekly_esr_or_inspections_chart(
        data_type: str,
        commodity: str,
        country: str,
        value_column: str,
        year_type: str,
        home: bool
) -> None:
    database_data = AgDataClient()
    df_data = database_data.get(data_type, commodity, country)

    if df_data is None:
        return
    
    df = pd.DataFrame(df_data)

    if (df[value_column] == 0).all():
        return

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

    figure.add_annotation(
        text=f"<b>Source: {"USDA<b>" if data_type == "inspections" else "<b>USDA ESR API<b>"}",
        xref="paper", yref="paper",
        x=1,
        y=1.05,
        yanchor="top",
        showarrow=False,
        font=dict(size=12, color="grey")
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

    # Makes sure more recent years have prioritized z-order
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

    json_dir = Path("api/charts").resolve()

    if home:
        json_path = (
            json_dir
             / f"{data_type}_us_{commodity.lower().replace(" ", "_")}_to_{country.lower().replace(" ", "_")}_{value_column}_last_5_years_{file_suffix}_home.json"
        )
    else:
        json_path = (
            json_dir
             / f"{data_type}_us_{commodity.lower().replace(" ", "_")}_to_{country.lower().replace(" ", "_")}_{value_column}_last_5_years_{file_suffix}.json"
        )

    pio.write_json(figure, str(json_path))

# Generates a weekly ESR or inspections chart for a given data set
def generate_weekly_psd_chart(
        data_type: str,
        commodity: str,
        country: str,
        attribute: str,
) -> None:
    database_data = AgDataClient()
    df_data = database_data.get(data_type, commodity, country)

    if df_data is None:
        return

    df = pd.DataFrame(df_data)

    df["attribute_norm"] = (
    df["attribute"]
    .str.lower()
    .str.replace(" ", "_")
    )

    df = df[df["attribute_norm"] == attribute]

    if df.empty:
        return

    df = df.drop(columns=["attribute_norm"])

    if (df["amount"] == 0).all():
        return

    mapping = {
        2026: "2025/2026",
        2025: "2024/2025",
        2024: "2023/2024",
        2023: "2022/2023",
        2022: "2021/2022",
        2021: "2020/2021",
    }
        
    df["marketing_year"] = df["marketing_year"].map(mapping)
    df = df.dropna(subset=["marketing_year"])
    df["marketing_year"] = df["marketing_year"].astype(str)

    df = df.sort_values(by="marketing_year")

    unit = df["unit"].iloc[0]
    latest_date = pd.to_datetime(df["date_collected"].iloc[0]).strftime("%m/%d/%Y")

    figure = px.bar(
        df,
        x="marketing_year",
        y="amount",
        color="marketing_year",
        title=(
            f"{country.title()} {commodity.title()} {attribute.replace('_', ' ').title()} "
            f"(as of {latest_date})"
        ),
        labels={
            "marketing_year": "Marketing Year",
            "amount": unit
        },
        text="amount"
    )

    figure.add_annotation(
        text=f"Source: <b>USDA PSD API<b>",
        xref="paper", yref="paper",
        x=1,
        y=1.05,
        yanchor="top",
        showarrow=False,
        font=dict(size=12, color="grey")
    )

    max_val = df["amount"].max()
    figure.update_yaxes(range=[0, max_val * 1.15])

    latest_year_raw = df["marketing_year"].max()
    latest_year_key = str(latest_year_raw).split("/")[0]

    for trace in figure.data:
        trace_label = str(trace.name)
        trace_first = trace_label.split("/")[0]

        if trace_first == latest_year_key:
            trace.update(marker=dict(color="red"))
        else:
            trace.update(opacity=0.7)

    if attribute in ["yield", "extraction_rate"]:
        figure.update_traces(texttemplate="%{text:,.3f}", textposition="outside")
    else:
        figure.update_traces(texttemplate="%{text:,.0f}", textposition="outside")

    figure.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(showgrid=True, gridcolor="lightgray", gridwidth=0.5),
        xaxis=dict(showgrid=False)
    )

    figure.update_traces(
        hovertemplate=
        f"{commodity.title()}: %{{y:,}} {unit}<br>"
        f"{"Marketing Year"}: %{{x}}<extra></extra>"
    )

    json_dir = Path("api/charts").resolve()
    commodity_slug = commodity.lower().replace(" ", "_")
    country_slug = country.lower().replace(" ", "_")

    json_path = (
        json_dir
         / f"{data_type}_{commodity_slug}_for_{country_slug}_{attribute}_last_5_years_my.json"
    )

    pio.write_json(figure, str(json_path))

# Generates every single chart possible for all commodities and marketing/calendar years if applicable
def generate_charts() -> None:
    print("Generating All Specific Page Charts...")

    esr_value_columns = [
        "weekly_exports",
        "accumulated_exports",
        "outstanding_sales",
        "gross_new_sales",
        "current_marketing_year_net_sales",
        "current_marketing_year_total_commitment",
        "next_marketing_year_outstanding_sales",
        "next_marketing_year_net_sales",
    ]

    psd_attributes = [
        "area_harvested",
        "crush",
        "beginning_stocks",
        "production",
        "imports",
        "trade_year_imports",
        "trade_year_imports_from_united_states",
        "total_supply",
        "exports",
        "trade_year_exports",
        "domestic_consumption",
        "feed_domestic_consumption",
        "industrial_domestic_consumption",
        "food_use_domestic_consumption",
        "feed_waste_domestic_consumption",
        "ending_stocks",
        "total_distribution",
        "extraction_rate",
        "yield",
        "food_seed_and_industrial_consumption",
        "soybean_meal_equivalent"
    ]


    for commodity in COMMODITIES.keys():
        esr_countries = ESR_COUNTRY_NAMES.values()
        psd_countries = PSD_COUNTRY_NAMES.values()

        for year_type in ["marketing", "calendar"]:
            if commodity not in ["soybean meal", "soybean oil"]:
                generate_weekly_esr_or_inspections_chart(
                data_type="inspections",
                commodity=commodity,
                country="world",
                value_column="export_inspections",
                year_type=year_type,
                home=False
                )

            for val_col in esr_value_columns:
                    generate_weekly_esr_or_inspections_chart(
                        data_type="esr",
                        commodity=commodity,
                        country="world",
                        value_column=val_col,
                        year_type=year_type,
                        home=False
                    )

                    for country in esr_countries:
                        generate_weekly_esr_or_inspections_chart(
                            data_type="esr",
                            commodity=commodity,
                            country=country,
                            value_column=val_col,
                            year_type=year_type,
                            home=False
                        )
        
        # PSD data only releases once per marketing year, so plotting by calendar year doesn't make sense
        
        for attribute in psd_attributes:
            generate_weekly_psd_chart(
                data_type="psd",
                commodity=commodity,
                country="world",
                attribute=attribute
            )

            for country in psd_countries:
                generate_weekly_psd_chart(
                data_type="psd",
                commodity=commodity,
                country=country,
                attribute=attribute
            )
        
    print("Done.\n==========")

# Specifically generates every single home page chart (makes it easier to format charts in JavaScript)
def generate_home_page_charts() -> None:
    print("Generating All Home Page Charts...")

    home_page_commodities = [
        "corn",
        "wheat",
        "soybeans"
    ]

    home_page_esr_value_columns = [
        "gross_new_sales",
        "current_marketing_year_total_commitment",
        "next_marketing_year_outstanding_sales"
    ]

    for commodity in home_page_commodities:
        generate_weekly_esr_or_inspections_chart(
            data_type="inspections",
            commodity=commodity,
            country="world",
            value_column="export_inspections",
            year_type="marketing",
            home=True
        )

        for val_col in home_page_esr_value_columns:
            generate_weekly_esr_or_inspections_chart(
                data_type="esr",
                commodity=commodity,
                country="world",
                value_column=val_col,
                year_type="marketing",
                home=True
            )

    print("Done.\n==========")