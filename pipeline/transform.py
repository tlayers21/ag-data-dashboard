import json
import pandas as pd
from pathlib import Path
from .config import COMMODITIES

ESR_RENAME_MAP = {
    "commodityCode": "commodity code",
    "countryCode": "country code",
    "weeklyExports": "weekly exports",
    "accumulatedExports": "accumulated exports",
    "outstandingSales": "outstanding sales",
    "grossNewSales": "gross new sales",
    "currentMYNetSales": "current marketing year net sales",
    "currentMYTotalCommitment": "current marketing year total commitment",
    "nextMYOutstandingSales": "next marketing year outstanding sales",
    "nextMYNetSales": "next marketing year net sales",
    "unitId": "unit id",
    "weekEndingDate": "week ending date"
}

PSD_RENAME_MAP = {
    "commodityCode": "commodity code",
    "countryCode": "country code",
    "marketYear": "market year",
    "calendarYear": "calendar year",
    "month": "calendar month",
    "attributeId": "attribute id",
    "unitId": "unit id",
    "value": "amount"
}

PSD_ATTRIBUTE_MAP = {
    4: "area harvested",
    7: "crush",
    20: "beginning stocks",
    28: "production",
    57: "imports",
    81: "trade year imports",
    84: "trade year imports from u.s.",
    86: "total supply",
    88: "exports",
    113: "trade year exports",
    125: "domestic consumption",
    130: "feed domestic consumption",
    140: "industrial domestic consumption",
    149: "food use domestic consumption",
    161: "feed waste domestic consumption",
    176: "ending stocks",
    178: "total distribution",
    181: "extraction rate",
    184: "yield",
    192: "food, seed, and industrial consumption",
    194: "soybean meal equivalent"
}

PSD_UNIT_MAP = {
    4: "1000 hectares",
    8: "1000 metric tons",
    23: "percentage",
    26: "yield (metric tons per hectare)"
}

ESR_COMMODITY_LOOKUP = {data["esr"]["commodity"]: commodity for commodity, data in COMMODITIES.items()}
PSD_COMMODITY_LOOKUP = {data["psd"]["commodity"]: commodity for commodity, data in COMMODITIES.items()}

def clean_esr_world_file(path: Path) -> pd.DataFrame:
    with open(path, "r") as file:
        raw_data = json.load(file)
    
    df = pd.DataFrame(raw_data)

    df = df.rename(columns=ESR_RENAME_MAP)
    df["week ending date"] = pd.to_datetime(df["week ending date"])
    commodity_code = str(df["commodity code"].iloc[0])
    commodity_name = ESR_COMMODITY_LOOKUP.get(commodity_code, "unknown")

    data_columns = [
        "weekly exports", "accumulated exports", "outstanding sales",
        "gross new sales", "current marketing year net sales",
        "current marketing year total commitment",
        "next marketing year outstanding sales",
        "next marketing year net sales"
    ]

    aggregated_data = df.groupby("week ending date")[data_columns].sum().reset_index()
    aggregated_data["unit"] = "metric tons"
    aggregated_data["commodity"] = commodity_name
    

    column_order = [
        "week ending date",
        "commodity",
        "unit",
        "weekly exports",
        "accumulated exports",
        "outstanding sales",
        "gross new sales",
        "current marketing year net sales",
        "current marketing year total commitment",
        "next marketing year outstanding sales",
        "next marketing year net sales"
    ]

    return aggregated_data[column_order]

def clean_esr_country_file(path: Path, country_name: str) -> pd.DataFrame:
    df = clean_esr_world_file(path)
    df["country"] = country_name

    column_order = [
        "week ending date",
        "commodity",
        "country",
        "unit",
        "weekly exports",
        "accumulated exports",
        "outstanding sales",
        "gross new sales",
        "current marketing year net sales",
        "current marketing year total commitment",
        "next marketing year outstanding sales",
        "next marketing year net sales"
    ]

    return df[column_order]

def clean_psd_world_file(path: Path) -> pd.DataFrame:
    with open(path, "r") as file:
        raw_data = json.load(file)
    
    df = pd.DataFrame(raw_data)

    df = df.rename(columns=PSD_RENAME_MAP)
    commodity_code = str(df["commodity code"].iloc[0])
    commodity_name = PSD_COMMODITY_LOOKUP.get(commodity_code, "unknown")


    df["unit"] = df["unit id"].map(PSD_UNIT_MAP)
    df["attribute"] = df["attribute id"].map(PSD_ATTRIBUTE_MAP)
    df = df.drop(columns=["commodity code", "country code", "unit id", "attribute id"])
    df["commodity"] = commodity_name

    column_order = [
        "market year",
        "calendar year",
        "calendar month",
        "commodity",
        "attribute",
        "unit",
        "amount"
    ]

    return df[column_order]

def clean_psd_country_file(path: Path, country_name: str) -> pd.DataFrame:
    df = clean_psd_world_file(path)
    df["country"] = country_name
    return df