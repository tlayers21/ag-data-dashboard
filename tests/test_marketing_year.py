from datetime import date

import pandas as pd

from pipeline.chart_generator import YEARS_SHOWN, trim_to_recent_years
from pipeline.marketing_year import (
    current_marketing_year,
    format_marketing_year_labels,
    marketing_year_start_date,
)


# Wheat rolls over on June 1, so the end-year label advances mid-calendar-year
def test_wheat_rolls_over_in_june():
    assert current_marketing_year("wheat", date(2026, 5, 31)) == 2026
    assert current_marketing_year("wheat", date(2026, 6, 1)) == 2027
    assert current_marketing_year("wheat", date(2026, 12, 31)) == 2027


# Corn and soybeans roll over on September 1, three months after wheat
def test_corn_rolls_over_in_september():
    assert current_marketing_year("corn", date(2026, 8, 31)) == 2026
    assert current_marketing_year("corn", date(2026, 9, 1)) == 2027
    assert current_marketing_year("soybeans", date(2026, 9, 1)) == 2027


def test_soybean_products_roll_over_in_october():
    assert current_marketing_year("soybean oil", date(2026, 9, 30)) == 2026
    assert current_marketing_year("soybean oil", date(2026, 10, 1)) == 2027
    assert current_marketing_year("soybean meal", date(2026, 10, 1)) == 2027


# The API and chart layers pass dashed slugs rather than the spaced config keys
def test_commodity_slugs_are_accepted():
    assert current_marketing_year("srw-wheat", date(2026, 6, 1)) == 2027
    assert current_marketing_year("HRW-Wheat", date(2026, 6, 1)) == 2027


def test_marketing_year_start_date():
    assert marketing_year_start_date(2027, "wheat") == date(2026, 6, 1)
    assert marketing_year_start_date(2026, "corn") == date(2025, 9, 1)


def test_format_marketing_year_labels():
    labels = format_marketing_year_labels(pd.Series([2026, 2027, None]))
    assert list(labels[:2]) == ["2025/2026", "2026/2027"]
    assert labels.iloc[2] is None


# A brand new marketing year must push out the oldest one, not be dropped itself
def test_trim_keeps_the_newest_years():
    years = ["2021/2022", "2022/2023", "2023/2024", "2024/2025", "2025/2026", "2026/2027"]
    df = pd.DataFrame({"marketing_year": years})

    trimmed = sorted(trim_to_recent_years(df, "marketing_year")["marketing_year"].unique())

    assert len(trimmed) == YEARS_SHOWN
    assert trimmed[-1] == "2026/2027"
    assert "2021/2022" not in trimmed


def test_trim_handles_calendar_years():
    df = pd.DataFrame({"calendar_year": [str(y) for y in range(2019, 2027)]})

    trimmed = sorted(trim_to_recent_years(df, "calendar_year")["calendar_year"].unique())

    assert trimmed == ["2022", "2023", "2024", "2025", "2026"]


# The same observation reaches the clean step from several raw files, so the merged
# frame has to collapse them before it is written out and loaded into the database
def test_drop_duplicate_rows_keeps_newest():
    from pipeline.clean import drop_duplicate_rows

    df = pd.DataFrame(
        {
            "commodity": ["hrw-wheat"] * 3 + ["corn"],
            "country": ["bangladesh"] * 3 + ["world"],
            "week_ending_date": ["2025-07-31"] * 3 + ["2025-07-31"],
            "weekly_exports": [0, 0, 42, 100],
        }
    )

    result = drop_duplicate_rows(df, "esr")

    assert len(result) == 2
    # files are processed oldest-first, so the last copy of a row is the freshest
    assert result[result["commodity"] == "hrw-wheat"]["weekly_exports"].iloc[0] == 42


# PSD carries a marketing year from new-crop projection, through estimate while it runs,
# to a settled figure once it ends, and each commodity crosses those lines on its own date
def test_marketing_year_status_tracks_each_commodity():
    from pipeline.marketing_year import marketing_year_status

    today = date(2026, 8, 31)

    # corn: 2025/26 ends today, 2026/27 starts tomorrow
    assert marketing_year_status(2025, "corn", today) == "final"
    assert marketing_year_status(2026, "corn", today) == "estimate"
    assert marketing_year_status(2027, "corn", today) == "projection"

    # wheat is three months ahead: 2025/26 already ended, 2026/27 is underway
    assert marketing_year_status(2026, "wheat", today) == "final"
    assert marketing_year_status(2027, "wheat", today) == "estimate"
    assert marketing_year_status(2028, "wheat", today) == "projection"


def test_marketing_year_end_date():
    from pipeline.marketing_year import marketing_year_end_date

    assert marketing_year_end_date(2026, "corn") == date(2026, 8, 31)
    assert marketing_year_end_date(2026, "wheat") == date(2026, 5, 31)
