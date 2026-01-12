import json
import requests
from .config import COMMODITIES, ESR_COUNTRY_NAMES, PSD_COUNTRY_NAMES
from .usda_client import USDAClient
from .utils import fas_data_path, inspections_data_path
from datetime import datetime, timedelta
import time
    
# Fetches both esr all and country data for each commodity
def fetch_esr_data(usda_api_key: str, marketing_year: int) -> None:
    usda_data = USDAClient(usda_api_key)

    print(f"Starting ESR Data Fetching Process For Marketing Year {marketing_year}...")
    for name, cfg in COMMODITIES.items():
        print(f"Fetching: {name.title()} For Marketing Year {marketing_year}")
        underscore_commodity_name = name.replace(" ", "_")

        esr_code = cfg["esr"]["commodity"]
        esr_countries = cfg["esr"]["countries"]

        # For to all countries
        esr_all_data = usda_data.esr_all_countries(esr_code, marketing_year)
        time.sleep(1)

        if esr_all_data:   
            with open(fas_data_path(f"{underscore_commodity_name}_esr_all_{marketing_year}.json"), "w") as file:
                json.dump(esr_all_data, file, indent=2)
        else:
            print(
                f"----------\nWARNING: No ESR All Data For {name.title()} " 
                f"For {marketing_year} Marketing Year\n----------"
            )

        # For to individual countries
        for country_code in esr_countries:
            country_data = usda_data.esr_country(esr_code, country_code, marketing_year)
            time.sleep(1)
            country_name = ESR_COUNTRY_NAMES.get(country_code, country_code)
            underscore_country_name = country_name.replace(" ", "_")

            if country_data:
                with open(fas_data_path(f"{underscore_commodity_name}_esr_to_{underscore_country_name}_{marketing_year}.json"), "w") as file:
                    json.dump(country_data, file, indent=2)
            else:
                print(
                    f"----------\nWARNING: No ESR Country Data For {name.title()} To {country_name.title()} "
                    f"For {marketing_year} Marketing Year\n----------"
                )
   
    print("Done.\n==========")

# Fetches both psd world and country data for each commodity
def fetch_psd_data(usda_api_key: str, marketing_year: int) -> None:
    usda_data = USDAClient(usda_api_key)

    print(f"Starting PSD Data Fetching Process For Marketing Year {marketing_year}...")
    for name, cfg in COMMODITIES.items():
        print(f"Fetching: {name.title()} For Marketing Year {marketing_year}")
        underscore_commodity_name = name.replace(" ", "_")

        psd_code = cfg["psd"]["commodity"]
        psd_countries = cfg["psd"]["countries"]

        # For world data
        psd_world_data = usda_data.psd_world(psd_code, marketing_year)
        time.sleep(1)

        if psd_world_data:   
            with open(fas_data_path(f"{underscore_commodity_name}_psd_world_{marketing_year}.json"), "w") as file:
                json.dump(psd_world_data, file, indent=2)
        else:
            print(
                f"----------\nWARNING: No PSD World Data For {name.title()} " 
                f"For {marketing_year} Marketing Year\n----------"
            )

        # For to individual countries
        for country_code in psd_countries:
            country_data = usda_data.psd_country(psd_code, country_code, marketing_year)
            time.sleep(1)
            country_name = PSD_COUNTRY_NAMES.get(country_code, country_code)
            underscore_country_name = country_name.replace(" ", "_")

            if country_data:
                with open(fas_data_path(f"{underscore_commodity_name}_psd_to_{underscore_country_name}_{marketing_year}.json"), "w") as file:
                    json.dump(country_data, file, indent=2)
            else:
                print(
                    f"----------\nWARNING: No PSD Country Data For {name.title()} To {country_name.title()} "
                    f"For {marketing_year} Marketing Year\n----------"
                )
                
    print("Done.\n==========")

# Fetches export inspections data using the URL that the USDA dynamically updates each week
def fetch_inspections() -> None:
    print("Fetching Latest Export Inspections Data...")

    url = "https://www.ams.usda.gov/mnreports/wa_gr101.txt"

    now = datetime.now()
    monday = now - timedelta(days=now.weekday())
    timestamp = monday.strftime("%Y-%m-%d")
    filename = f"{timestamp}_WA_GR101_.txt"
    filepath = inspections_data_path(filename)

    response = requests.get(url)
    if response.status_code == 200:
        filepath.write_bytes(response.content)
    else:
        print("WARNING: Failed To Download Weekly Export Inspections File")
