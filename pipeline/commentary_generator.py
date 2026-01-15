import pandas as pd
from .agdata_api_client import AgDataClient
from pathlib import Path

# Generates weekly commentary for all page charts (calculates WoW, YoY, and comparison to 5-year average metrics)
def generate_weekly_commentary(
    data_type: str,
    commodity: str,
    country: str,
    value_column: str,
) -> str:
    database_data = AgDataClient()
    df_data = database_data.get(data_type, commodity, country)

    df = pd.DataFrame(df_data)

    if df.empty:
        return f"There is no {data_type} data available for {commodity.replace("-", " ")} {value_column.replace('_', ' ')} to {country.replace("-", " ")}."
    
    df["date_collected"] = pd.to_datetime(df["date_collected"])
    df = df.sort_values("date_collected", ascending=False)
    latest_date = (
        df["date_collected"].iloc[0].strftime("%b").upper() +
        df["date_collected"].iloc[0].strftime("-%d")
    )

    df["week_ending_date"] = pd.to_datetime(df["week_ending_date"])
    df = df.sort_values("week_ending_date", ascending=False)

    latest_week_ending = df["week_ending_date"].iloc[0]
    day = latest_week_ending.day

    latest_value = df[value_column].iloc[0]
    unit = df["unit"].iloc[0]
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    latest_week_ending = f"{latest_week_ending.strftime("%B")} {day}{suffix}"

    # WoW
    if len(df) > 1:
        last_week_value = df[value_column].iloc[1]
        wow_change = (latest_value - last_week_value) / last_week_value
    else:
        wow_change = None

    # YoY
    latest_cal_year = df["calendar_year"].iloc[0]
    latest_cal_week = df["calendar_week"].iloc[0]

    df_yoy = df[
        (df["calendar_year"] == latest_cal_year - 1) &
        (df["calendar_week"] == latest_cal_week)
    ]

    if not df_yoy.empty:
        yoy_value = df_yoy[value_column].iloc[0]
        yoy_change = (latest_value - yoy_value) / yoy_value
    else:
        yoy_change = None
    
    # 5-year average
    df_5yr = df[df["calendar_week"] == latest_cal_week]

    if not df_5yr.empty:
        five_year_avg = df_5yr[value_column].mean()
        avg_change = (latest_value - five_year_avg) / five_year_avg
    else:
        five_year_avg = None
        avg_change = None

    # Actual commentary
    commentary = (
        f"{latest_date}: {commodity.replace("-", " ").capitalize()} {value_column.replace('_', ' ')} to " 
        f"{"the world" if country == "world" else country.title()} "
        f"for the week ending on {latest_week_ending} "
        f"{"was" if "commitment" in value_column else "were"}"
        f" {int(latest_value):,} {unit.replace('_', ' ').lower()} ("
    )

    # WoW
    if wow_change is not None:
        commentary += f"WoW: {wow_change * 100:+.2f}%, "
    else:
        commentary += f"WoW: not available, "
    
    # YoY
    if yoy_change is not None:
        commentary += f"YoY: {yoy_change * 100:+.2f}%, "
    else:
        commentary += f"YoY: not available, "
    
    # 5-year average
    if yoy_change is not None:
        commentary += f"{avg_change * 100:+.2f}% "
        commentary += f"{"above" if avg_change >= 0 else "below"}"
        commentary += " the 5-year average)."
    
    commentary_dir = Path("api/commentary").resolve()
    
    # For Render
    commentary_dir.mkdir(parents=True, exist_ok=True)
    commentary_path = (
        commentary_dir
         / f"us_{commodity.lower()}_to_{country.lower()}_{value_column}_commentary.txt"
    )
    with open(commentary_path, "w", encoding="utf-8") as f:
        f.write(commentary)
    
# Generates commentary for all home page charts
def generate_home_page_commentary() -> None:
    print("Generating All Home Page Commentary...")

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
        generate_weekly_commentary(
            data_type="inspections",
            commodity=commodity,
            country="world",
            value_column="export_inspections"
        )

        for val_col in home_page_esr_value_columns:
            generate_weekly_commentary(
                data_type="esr",
                commodity=commodity,
                country="world",
                value_column=val_col
            )

    print("Done.")