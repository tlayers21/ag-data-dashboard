import pandas as pd

MARKETING_YEAR_START = {
    "corn": 9,
    "soybeans": 9,
    "wheat": 6,
    "soybean meal": 10,
    "soybean oil": 10
}

def compute_marketing_year(date: pd.Series, start_month: int) -> pd.Series:
    return date.dt.year.where(date.dt.month < start_month, date.dt.year + 1).astype(int)

def compute_marketing_year_start_date(date: pd.Series, start_month: int) -> pd.Series:
    marketing_year = compute_marketing_year(date, start_month)
    start_year = (marketing_year - 1).astype(str)

    # For inspections it will be applied to an entire column
    if isinstance(start_month, pd.Series):
        start_month_str = start_month.astype(int).astype(str).str.zfill(2)
    else:
        start_month_str = str(start_month).zfill(2)
        
    return pd.to_datetime(start_year + "-" + start_month_str + "-01")

def first_weekday_on_or_after(date: pd.Timestamp, weekday: int) -> pd.Timestamp:
    # Inspections weeks end on thursdays, esr weeks end on tuesdays
    offset = (weekday - date.weekday()) % 7
    return date + pd.Timedelta(days=offset)

def compute_first_week_ending(start_dates: pd.Series, weekday: int) -> pd.Series:
    return start_dates.apply(lambda d: first_weekday_on_or_after(d, weekday))

def compute_marketing_year_week(week_ending: pd.Series, first_week_ending: pd.Series) -> pd.Series:
    return (((week_ending - first_week_ending).dt.days // 7) + 1).astype(int)

def compute_marketing_year_month(date: pd.Series, start_month: int) -> pd.Series:
    return (((date.dt.month - start_month) % 12) + 1).astype(int)