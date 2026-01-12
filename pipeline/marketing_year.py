import pandas as pd

# When each marketing year starts for each commodity
MARKETING_YEAR_START = {
    "corn": 9,
    "soybeans": 9,
    "wheat": 6,
    "soybean meal": 10,
    "soybean oil": 10
}

# Calculates the marketing year based on the calendar year
def compute_marketing_year(date: pd.Series, start_month: int) -> pd.Series:
    return date.dt.year.where(date.dt.month < start_month, date.dt.year + 1).astype(int)

# Determines the true start date of a marketing year based on its starting month
def compute_marketing_year_start_date(date: pd.Series, start_month: int) -> pd.Series:
    marketing_year = compute_marketing_year(date, start_month)
    start_year = (marketing_year - 1).astype(str)

    if isinstance(start_month, pd.Series):
        start_month_str = start_month.astype(int).astype(str).str.zfill(2)
    else:
        start_month_str = str(start_month).zfill(2)
        
    return pd.to_datetime(start_year + "-" + start_month_str + "-01")

# Determines the first weekday (on or after) that the data contains
def first_weekday_on_or_after(date: pd.Timestamp, weekday: int) -> pd.Timestamp:
    offset = (weekday - date.weekday()) % 7
    return date + pd.Timedelta(days=offset)

# Determines the first week ending date for all start dates for a given marketing year
def compute_first_week_ending(start_dates: pd.Series, weekday: int) -> pd.Series:
    return start_dates.apply(lambda d: first_weekday_on_or_after(d, weekday))

# Calculates the marketing year weeks in the data (esr)
def compute_marketing_year_week_esr(week_ending: pd.Series, first_week_ending: pd.Series) -> pd.Series:
    weeks = ((week_ending - first_week_ending).dt.days // 7) + 1
    #TODO: Figure out how to fix edge cases for marketing year weeks (esr) to account for edge cases
    """
    Some of the week data from previous year gets pushed to the next year, causing discrepancies.
    Since these charts are more used as a comparison to previous years, this solution
    fixes this issue, however loses a bit of data.
    """
    return weeks.where(weeks > 1).astype("Int64")

# Calculates the marketing year weeks in the data (export inspections)
def compute_marketing_year_week_inspections(week_ending: pd.Series, first_week_ending: pd.Series) -> pd.Series:
    return ((week_ending - first_week_ending).dt.days // 7) + 1

# Calculates the marketing year month by comparing it's calendar date to the marketing year start month
def compute_marketing_year_month(date: pd.Series, start_month: int) -> pd.Series:
    return (((date.dt.month - start_month) % 12) + 1).astype(int)