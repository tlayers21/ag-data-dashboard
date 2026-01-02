import json
import pandas as pd
from pathlib import Path

ESR_RENAME_MAP = {
    "commodityCode": "commodity_code",
    "countryCode": "country_code",
    "weeklyExports": "weekly_exports",
    "accumulatedExports": "accumulated_exports",
    "outstanding_sales": "outstanding_sales",
    "GrossNewSales": "gross_new_sales",
    "currentMYNetSales": "current_marketing_year_net_sales",
    "currentMYTotalCommitment": "current_marketing_year_total_commitment",
    "nextMYOutstandingSales": "next_marketing_year_outstanding_sales",
    "nextMYNetSales": "current_marketing_year_net_sales",
    "unitId": "unit_id",
    "weekEndingDate": "week_ending_date"
}

PSD_RENAME_MAP = {
    "commodityCode": "commodity_code",
    "countryCode": "country_code",
    "marketYear": "market_year",
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
    81: "TY Imports",
    84: "TY Imp. from U.S.",
    86: "Total Supply",
    88: "Exports",
    113: "TY Exports",
    125: "Domestic Consumption",
    130: "Feed Dom. Consumption",
    140: "Industrial Dom. Cons.",
    149: "Food Use Dom. Cons.",
    161: "Feed Waste Dom. Cons.",
    176: "Ending Stocks",
    178: "Total Distribution",
    181: "Extr. Rate",
    184: "Yield",
    192: "FSI Consumption",
    194: "SME"
}

PSD_UNIT_MAP = {
    4: "1000 Hectares (HA)",
    8: "1000 Metric Tons (MT)",
    23: "Percentage (%)",
    26: "Yield: Metric Tons per Hectare (MT/HA)"
}

def clean_esr_world_file(path: Path) -> pd.DataFrame:
    with open(path, "r") as file:
        raw_data = json.load(file)
    
    df = pd.DataFrame(raw_data)

    df = df.rename(columns=ESR_RENAME_MAP)
    df["week_ending_date"] = pd.to_datetime(df["week_ending_date"])

    data_columns = [
        "weekly_exports", "accumulated_exports", "outstanding_sales",
        "gross_new_sales", "current_marketing_year_net_sales",
        "current_marketing_year_total_commitment",
        "next_marketing_year_outstanding_sales",
        "current_marketing_year_net_sales"
    ]

    aggregated_data = df.groupby("week_ending_date")[data_columns].sum().reset_index()
    aggregated_data["unit"] = "metric_tons"

    return aggregated_data

def clean_esr_country_file(path: Path, country_name: str) -> pd.DataFrame:
    df = clean_esr_world_file(path)
    df["country"] = country_name
    return df

def clean_psd_world_file(path: Path) -> pd.DataFrame:
    with open(path, "r") as file:
        raw_data = json.load(file)
    
    df = pd.DataFrame(raw_data)
    df = df.rename(columns=PSD_RENAME_MAP)

    df["unit"] = df["unit_id"].map(PSD_ATTRIBUTE_MAP)
    df["attribute"] = df["attribute_id"].map(PSD_ATTRIBUTE_MAP)
    df = df.drop(columns=["unit_id", "attribute_id"])

    return df

def clean_psd_country_file(path: Path, country_name: str) -> pd.DataFrame:
    df = clean_psd_world_file(path)
    df["country"] = country_name
    return df