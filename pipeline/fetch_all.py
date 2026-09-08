import json
import requests
from .config import COMMODITIES, ESR_COUNTRY_NAMES, PSD_COUNTRY_NAMES
from .usda_client import USDAClient, USDAFetchError, REQUEST_TIMEOUT
from pathlib import Path
from .utils import fas_data_path, inspections_data_path
from .marketing_year import (
    current_marketing_year,
    marketing_year_end_date,
    marketing_year_start_date,
    marketing_year_status,
)
from datetime import date, datetime, timedelta

FAS_DIR = Path(__file__).parent.parent / "data" / "raw" / "fas"
INSPECTIONS_DIR = Path(__file__).parent.parent / "data" / "raw" / "inspections"

ESR_NEW_YEAR_GRACE_DAYS = 21
ESR_SETTLED_GRACE_DAYS = 30

def _esr_year_too_new(commodity: str, marketing_year: int) -> bool:
    if marketing_year_status(marketing_year, commodity) == "projection":
        return True

    start_date = marketing_year_start_date(marketing_year, commodity)
    return date.today() < start_date + timedelta(days=ESR_NEW_YEAR_GRACE_DAYS)

# A marketing year that closed a while ago and was fetched after it closed has nothing left
# to give, so its ~19 requests are spent re-downloading files already on disk
def _esr_year_settled(commodity: str, dash_commodity_name: str, marketing_year: int) -> bool:
    if marketing_year_status(marketing_year, commodity) != "final":
        return False

    settled_on = (
        marketing_year_end_date(marketing_year, commodity)
        + timedelta(days=ESR_SETTLED_GRACE_DAYS)
    )
    if date.today() < settled_on:
        return False

    all_countries_file = fas_data_path(f"{dash_commodity_name}_esr_all_{marketing_year}my.json")
    if not all_countries_file.exists():
        return False

    return date.fromtimestamp(all_countries_file.stat().st_mtime) >= settled_on

# Fetches both esr all and country data for each commodity
def fetch_esr_data(usda_api_key: str, marketing_year: int | None = None, years_back: int = 2) -> None:
    usda_data = USDAClient(usda_api_key)
    FAS_DIR.mkdir(parents=True, exist_ok=True)

    print("Starting ESR Data Fetching Process...")
    for name, cfg in COMMODITIES.items():
        dash_commodity_name = name.replace(' ', '-')

        esr_code = cfg["esr"]["commodity"]
        esr_countries = cfg["esr"]["countries"]

        if marketing_year is None:
            esr_years = [current_marketing_year(name) - offset for offset in range(years_back)]
            unreported_years = {
                year for year in esr_years if _esr_year_too_new(name, year)
            }
        else:
            esr_years = [marketing_year]
            unreported_years = set()

        for esr_year in esr_years:
            if _esr_year_settled(name, dash_commodity_name, esr_year):
                print(f"{name.title()} {esr_year} Marketing Year Already Settled - Skipping")
                continue

            _fetch_esr_marketing_year(
                usda_data,
                name,
                dash_commodity_name,
                esr_code,
                esr_countries,
                esr_year,
                warn_if_missing=esr_year not in unreported_years,
            )

    print("Done.\n==========")

# Fetches one commodity's esr data for a single marketing year
def _fetch_esr_marketing_year(
        usda_data: USDAClient,
        name: str,
        dash_commodity_name: str,
        esr_code: str,
        esr_countries: list,
        marketing_year: int,
        warn_if_missing: bool = True
) -> None:
    print(f"Fetching: {name.title()} For Marketing Year {marketing_year}")

    # For to all countries. A failed endpoint is reported and stepped over rather than
    # raised, so one flaky request cannot cost the run every later commodity and the load
    try:
        esr_all_data = usda_data.esr_all_countries(esr_code, marketing_year)
        all_countries_failed = False
    except USDAFetchError as error:
        print(
            f"----------\nWARNING: ESR All Fetch Failed For {name.title()} "
            f"For {marketing_year} Marketing Year: {error}\n----------"
        )
        esr_all_data = None
        all_countries_failed = True

    if esr_all_data:
        with open(fas_data_path(f"{dash_commodity_name}_esr_all_{marketing_year}my.json"), "w") as file:
            json.dump(esr_all_data, file, indent=2)
    elif all_countries_failed:
        # The fetch broke rather than came back empty, so the countries are still worth trying
        pass
    elif warn_if_missing:
        print(
            f"----------\nWARNING: No ESR All Data For {name.title()} " 
            f"For {marketing_year} Marketing Year\n----------"
        )
    else:
        # Nothing reported for this marketing year yet, so no country has it either
        print(f"{name.title()} {marketing_year} Marketing Year Not Reported Yet - Skipping")
        return

    # For to individual countries
    for country_code in esr_countries:
        country_name = ESR_COUNTRY_NAMES.get(country_code, country_code)
        dash_country_name = country_name.replace(' ', '-')

        try:
            country_data = usda_data.esr_country(esr_code, country_code, marketing_year)
        except USDAFetchError as error:
            print(
                f"----------\nWARNING: ESR Country Fetch Failed For {name.title()} "
                f"To {country_name.title()} For {marketing_year} Marketing Year: {error}\n----------"
            )
            continue

        if country_data:
            with open(fas_data_path(f"{dash_commodity_name}_esr_to_{dash_country_name}_{marketing_year}my.json"), "w") as file:
                json.dump(country_data, file, indent=2)
        elif warn_if_missing:
            print(
                f"----------\nWARNING: No ESR Country Data For {name.title()} To {country_name.title()} "
                f"For {marketing_year} Marketing Year\n----------"
            )

# Fetches both psd world and country data for each commodity
def fetch_psd_data(usda_api_key: str, marketing_year: int | None = None, years_back: int = 2) -> None:
    usda_data = USDAClient(usda_api_key)
    FAS_DIR.mkdir(parents=True, exist_ok=True)

    print("Starting PSD Data Fetching Process...")
    for name, cfg in COMMODITIES.items():
        if "psd" not in cfg:
            print(f"Skipping {name.title()} - no PSD configuration found.")
            continue

        dash_commodity_name = name.replace(' ', '-')

        psd_code = cfg["psd"]["commodity"]
        psd_countries = cfg["psd"]["countries"]

        if marketing_year is None:
            # current_marketing_year is an end year, so -1 converts it to PSD's start year.
            # The extra +1 year on the front picks up the new-crop projection, which USDA
            # starts publishing around May, months before that marketing year begins.
            current_psd_year = current_marketing_year(name) - 1
            psd_years = [
                current_psd_year + 1 - offset for offset in range(years_back + 1)
            ]
            # Outside roughly May-August that new-crop year has not been published yet, so
            # an empty response is the expected answer rather than something to warn about
            unpublished_years = {current_psd_year + 1}
        else:
            psd_years = [marketing_year]
            unpublished_years = set()

        for psd_year in psd_years:
            _fetch_psd_marketing_year(
                usda_data,
                name,
                dash_commodity_name,
                psd_code,
                psd_countries,
                psd_year,
                warn_if_missing=psd_year not in unpublished_years,
            )

    print("Done.\n==========")

# Fetches one commodity's psd data for a single (start-year) marketing year
def _fetch_psd_marketing_year(
        usda_data: USDAClient,
        name: str,
        dash_commodity_name: str,
        psd_code: str,
        psd_countries: list,
        marketing_year: int,
        warn_if_missing: bool = True
) -> None:
    print(f"Fetching: {name.title()} For Marketing Year {marketing_year}")

    # For world data
    try:
        psd_world_data = usda_data.psd_world(psd_code, marketing_year)
        world_failed = False
    except USDAFetchError as error:
        print(
            f"----------\nWARNING: PSD World Fetch Failed For {name.title()} "
            f"For {marketing_year} Marketing Year: {error}\n----------"
        )
        psd_world_data = None
        world_failed = True

    if psd_world_data:
        with open(fas_data_path(f"{dash_commodity_name}_psd_world_{marketing_year}my.json"), "w") as file:
            json.dump(psd_world_data, file, indent=2)
    elif world_failed:
        # The fetch broke rather than came back empty, so the countries are still worth trying
        pass
    elif warn_if_missing:
        print(
            f"----------\nWARNING: No PSD World Data For {name.title()} " 
            f"For {marketing_year} Marketing Year\n----------"
        )
    else:
        # Nothing published for this marketing year yet, so no country has it either
        print(f"{name.title()} {marketing_year} Marketing Year Not Published Yet - Skipping")
        return

    # For to individual countries
    for country_code in psd_countries:
        country_name = PSD_COUNTRY_NAMES.get(country_code, country_code)
        dash_country_name = country_name.replace(' ', '-')

        try:
            country_data = usda_data.psd_country(psd_code, country_code, marketing_year)
        except USDAFetchError as error:
            print(
                f"----------\nWARNING: PSD Country Fetch Failed For {name.title()} "
                f"To {country_name.title()} For {marketing_year} Marketing Year: {error}\n----------"
            )
            continue

        if country_data:
            with open(fas_data_path(f"{dash_commodity_name}_psd_to_{dash_country_name}_{marketing_year}my.json"), "w") as file:
                json.dump(country_data, file, indent=2)
        elif warn_if_missing:
            print(
                f"----------\nWARNING: No PSD Country Data For {name.title()} To {country_name.title()} "
                f"For {marketing_year} Marketing Year\n----------"
            )

# TODO: Find a way to fetch inspections data so I don't have to store actual files

# Fetches export inspections data using the URL that the USDA dynamically updates each week
def fetch_inspections() -> None:
    INSPECTIONS_DIR.mkdir(parents=True, exist_ok=True)

    print("Fetching Latest Export Inspections Data...")

    url = "https://www.ams.usda.gov/mnreports/wa_gr101.txt"

    now = datetime.now()
    monday = now - timedelta(days=now.weekday())
    timestamp = monday.strftime("%Y-%m-%d")
    filename = f"{timestamp}_WA_GR101_.txt"
    filepath = inspections_data_path(filename)

    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    if response.status_code == 200:
        new_content = response.content

        for file in INSPECTIONS_DIR.iterdir():
            if file.read_bytes() == new_content:
                print(f"File with identical content already exists: {file.name}")
                return
            
        filepath.write_bytes(response.content)
    else:
        print("WARNING: Failed To Download Weekly Export Inspections File")