import pandas as pd
from .api_client import fetch_data_last5years
from pathlib import Path
from datetime import datetime

def generate_weekly_commentary(
    data: str,
    commodity: str,
    country: str,
    value_column: str,
) -> str:
    df_data = fetch_data_last5years(data, commodity, country)
    df = pd.DataFrame(df_data)

    if df.empty:
        return f"There is no {data} data available for {commodity} {value_column.replace("_", " ")} to {country}."
    
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
        f"{latest_date}: {commodity.capitalize()} {value_column.replace("_", " ")} to " 
        f"{"the world" if country == "world" else country.title()} "
        f"for the week ending on {latest_week_ending} "
        f"{"was" if "commitment" in value_column else "were"}"
        f" {int(latest_value):,} {unit.replace("_", " ").lower()} ("
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
    
    commentary_dir = Path("frontend/src/commentary/").resolve()
    commentary_path = (
        commentary_dir
         / f"us_{commodity.lower()}_to_{country.lower()}_{value_column}_commentary.txt"
    )
    with open(commentary_path, "w", encoding="utf-8") as f:
        f.write(commentary)
    
def generate_home_page_commentary() -> None:
    print("Generating home page commentary...")
    generate_weekly_commentary("inspections", "corn", "world", "export_inspections")
    generate_weekly_commentary("esr", "corn", "world", "gross_new_sales")
    generate_weekly_commentary("esr", "corn", "world", "current_marketing_year_total_commitment")
    generate_weekly_commentary("esr", "corn", "world", "next_marketing_year_outstanding_sales")

    generate_weekly_commentary("inspections", "wheat", "world", "export_inspections")
    generate_weekly_commentary("esr", "wheat", "world", "gross_new_sales")
    generate_weekly_commentary("esr", "wheat", "world", "current_marketing_year_total_commitment")
    generate_weekly_commentary("esr", "wheat", "world", "next_marketing_year_outstanding_sales")

    generate_weekly_commentary("inspections", "soybeans", "world", "export_inspections")
    generate_weekly_commentary("esr", "soybeans", "world", "gross_new_sales")
    generate_weekly_commentary("esr", "soybeans", "world", "current_marketing_year_total_commitment")
    generate_weekly_commentary("esr", "soybeans", "world", "next_marketing_year_outstanding_sales")

    print("Done.")