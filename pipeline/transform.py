import json
import pandas as pd
from pathlib import Path
import re
from .config import COMMODITIES
from .marketing_year import (
    MARKETING_YEAR_START,
    compute_marketing_year,
    compute_marketing_year_start_date,
    compute_first_week_ending,
    compute_marketing_year_week,
    compute_marketing_year_month
)

ESR_RENAME_MAP = {
    "commodityCode": "commodity_code",
    "countryCode": "country_code",
    "weeklyExports": "weekly_exports",
    "accumulatedExports": "accumulated_exports",
    "outstandingSales": "outstanding_sales",
    "grossNewSales": "gross_new_sales",
    "currentMYNetSales": "current_marketing_year_net_sales",
    "currentMYTotalCommitment": "current_marketing_year_total_commitment",
    "nextMYOutstandingSales": "next_marketing_year_outstanding_sales",
    "nextMYNetSales": "next_marketing_year_net_sales",
    "unitId": "unit_id",
    "weekEndingDate": "week_ending_date"
}

ESR_COMMODITY_LOOKUP = {data["esr"]["commodity"]: commodity for commodity, data in COMMODITIES.items()}

PSD_RENAME_MAP = {
    "commodityCode": "commodity_code",
    "countryCode": "country_code",
    "marketYear": "marketing_year",
    "calendarYear": "calendar_year",
    "month": "calendar_month",
    "attributeId": "attribute_id",
    "unitId": "unit_id",
    "value": "amount"
}

PSD_ATTRIBUTE_MAP = {
    4: "Area Harvested",
    7: "Crush",
    20: "Beginning Stocks",
    28: "Production",
    57: "Imports",
    81: "Trade Year Imports",
    84: "Trade Year Imports from U.S.",
    86: "Total Supply",
    88: "Exports",
    113: "Trade Year Exports",
    125: "Domestic Consumption",
    130: "Feed Domestic Consumption",
    140: "Industrial Domestic Consumption",
    149: "Food Use Domestic Consumption",
    161: "Feed Waste Domestic Consumption",
    176: "Ending Stocks",
    178: "Total Distribution",
    181: "Extraction Rate",
    184: "Yield",
    192: "Food, Seed, and Industrial Consumption",
    194: "Soybean Meal Equivalent"
}

PSD_UNIT_MAP = {
    4: "1000 Hectares",
    8: "1000 Metric Tons",
    23: "Percentage",
    26: "Yield (Metric Tons per Hectare)"
}

PSD_COMMODITY_LOOKUP = {data["psd"]["commodity"]: commodity for commodity, data in COMMODITIES.items()}

def clean_esr_world_file(path: Path) -> pd.DataFrame:
    with open(path, "r") as file:
        raw_data = json.load(file)
    
    df = pd.DataFrame(raw_data)

    df = df.rename(columns=ESR_RENAME_MAP)
    df["week_ending_date"] = pd.to_datetime(df["week_ending_date"])
    commodity_code = str(df["commodity_code"].iloc[0])

    commodity_name = ESR_COMMODITY_LOOKUP.get(commodity_code)
    start_month = MARKETING_YEAR_START[commodity_name]

    data_columns = [
        "weekly_exports", "accumulated_exports", "outstanding_sales",
        "gross_new_sales", "current_marketing_year_net_sales",
        "current_marketing_year_total_commitment",
        "next_marketing_year_outstanding_sales",
        "next_marketing_year_net_sales"
    ]

    aggregated_data = df.groupby("week_ending_date")[data_columns].sum().reset_index()
    aggregated_data["unit"] = "Metric Tons"
    aggregated_data["commodity"] = commodity_name
    aggregated_data["country"] = "world"

    # Determine calendar year, month, and week
    aggregated_data["calendar_year"] = aggregated_data["week_ending_date"].dt.year
    aggregated_data["calendar_month"] = aggregated_data["week_ending_date"].dt.month
    aggregated_data["calendar_week"] = aggregated_data["week_ending_date"].dt.isocalendar().week

    # Determine marketing year, month, and week
    aggregated_data["marketing_year"] = compute_marketing_year(aggregated_data["week_ending_date"], start_month)
    aggregated_data["marketing_year_start_date"] = compute_marketing_year_start_date(aggregated_data["week_ending_date"], start_month)
    # ESR weeks end on Tuesday
    aggregated_data["first_week_ending"] = compute_first_week_ending(aggregated_data["marketing_year_start_date"], weekday=1)

    aggregated_data["marketing_year_month"] = compute_marketing_year_month(
        aggregated_data["week_ending_date"], start_month
    )
    aggregated_data["marketing_year_week"] = compute_marketing_year_week(
        aggregated_data["week_ending_date"], aggregated_data["first_week_ending"]
    )

    aggregated_data = aggregated_data.drop(columns=["marketing_year_start_date", "first_week_ending"])

    column_order = [
        "week_ending_date",
        "calendar_year",
        "marketing_year",
        "calendar_month",
        "marketing_year_month",
        "calendar_week",
        "marketing_year_week",
        "commodity",
        "country",
        "weekly_exports",
        "accumulated_exports",
        "outstanding_sales",
        "gross_new_sales",
        "current_marketing_year_net_sales",
        "current_marketing_year_total_commitment",
        "next_marketing_year_outstanding_sales",
        "next_marketing_year_net_sales",
        "unit"
    ]

    return aggregated_data[column_order]

def clean_esr_country_file(path: Path, country_name: str) -> pd.DataFrame:
    df = clean_esr_world_file(path)
    df["country"] = country_name

    column_order = [
        "week_ending_date",
        "calendar_year",
        "marketing_year",
        "calendar_month",
        "marketing_year_month",
        "calendar_week",
        "marketing_year_week",
        "commodity",
        "country",
        "weekly_exports",
        "accumulated_exports",
        "outstanding_sales",
        "gross_new_sales",
        "current_marketing_year_net_sales",
        "current_marketing_year_total_commitment",
        "next_marketing_year_outstanding_sales",
        "next_marketing_year_net_sales",
        "unit"
    ]

    return df[column_order]

def clean_psd_world_file(path: Path) -> pd.DataFrame:
    with open(path, "r") as file:
        raw_data = json.load(file)
    
    df = pd.DataFrame(raw_data)

    df = df.rename(columns=PSD_RENAME_MAP)
    commodity_code = str(df["commodity_code"].iloc[0])
    commodity_name = PSD_COMMODITY_LOOKUP.get(commodity_code)
    df["calendar_month"] = df["calendar_month"].astype(int)

    df["unit"] = df["unit_id"].map(PSD_UNIT_MAP)
    df["attribute"] = df["attribute_id"].map(PSD_ATTRIBUTE_MAP)
    df = df.drop(columns=["commodity_code", "country_code", "unit_id", "attribute_id"])
    df["commodity"] = commodity_name
    df["country"] = "world"

    marketing_year_start = MARKETING_YEAR_START.get(commodity_name)
    df["marketing_year_month"] = ((df["calendar_month"] - marketing_year_start) % 12) + 1

    column_order = [
        "marketing_year",
        "calendar_year",
        "calendar_month",
        "marketing_year_month",
        "commodity",
        "country",
        "attribute",
        "amount",
        "unit"
    ]

    return df[column_order]

def clean_psd_country_file(path: Path, country_name: str) -> pd.DataFrame:
    df = clean_psd_world_file(path)
    df["country"] = country_name

    column_order = [
        "marketing_year",
        "calendar_year",
        "calendar_month",
        "marketing_year_month",
        "commodity",
        "country",
        "attribute",
        "amount",
        "unit"
    ]

    return df[column_order]

def clean_inspections_file(path: Path) -> pd.DataFrame:
    text = path.read_text(encoding="latin-1")

    # Example: REPORTED IN WEEK ENDING DEC 25, 2025
    date_pattern = r"WEEK ENDING ([A-Z]{3} \d{2}, \d{4})"
    date_match = re.search(date_pattern, text)

    # Files can contain date but say 'sorry it's delayed or something' so much check in extract_value too
    if not date_match:
        print(f"'{path.name}' Does Not Contain Inspections Data")
        return
    
    week_ending_date = pd.to_datetime(date_match.group(1))

    def extract_value(grain_name: str) -> int:
        # Example: CORN          *457,366*     672,835...
        amount_pattern = rf"{grain_name}\s+([\d,]+)"
        amount_match = re.search(amount_pattern, text)
        if not amount_match:
            print(f"'{path.name}' Does Not Contain Inspections Data")
            return
        
        amount = amount_match.group(1).replace(",", "")
        return int(amount)
    
    amounts = {
        "corn": extract_value("CORN"),
        "wheat": extract_value("WHEAT"),
        "soybeans": extract_value("SOYBEANS")
    }

    rows = []
    for commodity, amount in amounts.items():
        if amount is None:
            continue
        rows.append({
            "commodity": commodity,
            "week_ending_date": week_ending_date,
            "amount": amount,
            "unit": "Metric Tons"
        })
    
    df = pd.DataFrame(rows)

    # Determine calendar year, month, and week
    df["calendar_year"] = df["week_ending_date"].dt.year
    df["calendar_month"] = df["week_ending_date"].dt.month
    df["calendar_week"] = df["week_ending_date"].dt.isocalendar().week

    # Determine marketing year, month, and week (per commodity)
    df["start_month"] = df["commodity"].map(MARKETING_YEAR_START)

    df["marketing_year"] = compute_marketing_year(
        df["week_ending_date"], df["start_month"]
    )

    df["marketing_year_start_date"] = compute_marketing_year_start_date(
        df["week_ending_date"], df["start_month"]
    )

    df["first_week_ending"] = compute_first_week_ending(
        df["marketing_year_start_date"], weekday=3
    )

    df["marketing_year_month"] = compute_marketing_year_month(
        df["week_ending_date"], df["start_month"]
    )

    df["marketing_year_week"] = compute_marketing_year_week(
        df["week_ending_date"], df["first_week_ending"]
    )

    df = df.drop(columns=["start_month", "marketing_year_start_date", "first_week_ending"])

    column_order = [
        "week_ending_date",
        "calendar_year",
        "marketing_year",
        "calendar_month",
        "marketing_year_month",
        "calendar_week",
        "marketing_year_week",
        "commodity",
        "amount",
        "unit"
    ]

    return df[column_order]



