import json
import pandas as pd
from pathlib import Path
from .config import COMMODITIES

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
    "weekEndingDate": "week_ending_date",
    "marketYear": "marketing_year"
}

MARKETING_YEAR_START = {
    "corn": 9,
    "soybeans": 9,
    "wheat": 6,
    "soybean oil": 10,
    "soybean meal": 10
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
    marketing_year = df["marketing_year"].iloc[0]

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
    aggregated_data["marketing_year"] = marketing_year

    # Extract calendar week, month, and year then assign marketing year weeks and months
    aggregated_data["calendar_week"] = aggregated_data["week_ending_date"].dt.isocalendar().week
    aggregated_data["calendar_month"] = aggregated_data["week_ending_date"].dt.month
    aggregated_data["calendar_year"] = aggregated_data["week_ending_date"].dt.year

    aggregated_data = aggregated_data.sort_values("week_ending_date").reset_index(drop=True)
    marketing_year_start_month = MARKETING_YEAR_START.get(commodity_name)
    start_dates = aggregated_data.loc[
        (aggregated_data["calendar_month"] == marketing_year_start_month) &
        (aggregated_data["commodity"] == commodity_name),
        "week_ending_date"
    ].dropna()

    if start_dates.empty:
        fallback_year = aggregated_data["calendar_year"].iloc[0]
        fallback_date = pd.Timestamp(year=fallback_year, month=marketing_year_start_month, day=1)
        start_dates = pd.Series([fallback_date])
    
    first_week_date = start_dates.min()

    aggregated_data["marketing_year_week"] = (
        (aggregated_data["week_ending_date"] - first_week_date).dt.days // 7 + 1
    )
    aggregated_data["marketing_year_month"] = ((aggregated_data["calendar_month"] - marketing_year_start_month) % 12) + 1

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