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

PSD_ATTRIBUTE_IDS = {
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

def clean_esr_file(path: Path) -> pd.DataFrame:
    
    with open(path, "r") as file:
        raw = json.load(file)
    
    df = pd.DataFrame(raw)

    df = df.rename(columns={
        "week"
    })