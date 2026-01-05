import json
from .config import COMMODITIES, ESR_COUNTRY_NAMES, PSD_COUNTRY_NAMES
from .usda_client import USDAClient
from .utils import raw_data_path
import time
    
def fetch_esr_data(usda_api_key: str, esr_market_year: str) -> None:
    usda_data = USDAClient(usda_api_key)

    print(f"Starting ESR Data Fetching Process for Marketing Year {esr_market_year}...")
    for name, cfg in COMMODITIES.items():
        print(f"Fetching: {name.capitalize()} for Marketing Year {esr_market_year}")
        underscore_commodity_name = name.replace(" ", "_")

        esr_code = cfg["esr"]["commodity"]
        esr_countries = cfg["esr"]["countries"]

        # For to all countries
        esr_all_data = usda_data.esr_all_countries(esr_code, esr_market_year)
        time.sleep(1)

        if esr_all_data:   
            with open(raw_data_path(f"{underscore_commodity_name}_esr_all_{esr_market_year}.json"), "w") as file:
                json.dump(esr_all_data, file, indent=2)
        else:
            print(
                f"----------\nWARNING: No ESR all data for {name} " 
                f"for {esr_market_year} Marketing Year\n----------"
            )

        # For to individual countries
        for country_code in esr_countries:
            country_data = usda_data.esr_country(esr_code, country_code, esr_market_year)
            time.sleep(1)
            country_name = ESR_COUNTRY_NAMES.get(country_code, country_code)
            underscore_country_name = country_name.replace(" ", "_")

            if country_data:
                with open(raw_data_path(f"{underscore_commodity_name}_esr_to_{underscore_country_name}_{esr_market_year}.json"), "w") as file:
                    json.dump(country_data, file, indent=2)
            else:
                print(
                    f"----------\nWARNING: No ESR country data for {name} to {country_name.capitalize()} "
                    f"for {esr_market_year} Marketing Year\n----------"
                )
   
    print("Done.\n==========")

def fetch_psd_data(usda_api_key: str, psd_market_year: str) -> None:
    usda_data = USDAClient(usda_api_key)

    print(f"Starting PSD Data Fetching Process for Marketing Year {psd_market_year}...")
    for name, cfg in COMMODITIES.items():
        print(f"Fetching: {name.capitalize()} for Marketing Year {psd_market_year}")
        underscore_commodity_name = name.replace(" ", "_")

        psd_code = cfg["psd"]["commodity"]
        psd_countries = cfg["psd"]["countries"]

        # For world data
        psd_world_data = usda_data.psd_world(psd_code, psd_market_year)
        time.sleep(1)

        if psd_world_data:   
            with open(raw_data_path(f"{underscore_commodity_name}_psd_world_{psd_market_year}.json"), "w") as file:
                json.dump(psd_world_data, file, indent=2)
        else:
            print(
                f"----------\nWARNING: No PSD world data for {name} " 
                f"for {psd_market_year} Marketing Year\n----------"
            )

        # For to individual countries
        for country_code in psd_countries:
            country_data = usda_data.psd_country(psd_code, country_code, psd_market_year)
            time.sleep(1)
            country_name = PSD_COUNTRY_NAMES.get(country_code, country_code)
            underscore_country_name = country_name.replace(" ", "_")

            if country_data:
                with open(raw_data_path(f"{underscore_commodity_name}_psd_to_{underscore_country_name}_{psd_market_year}.json"), "w") as file:
                    json.dump(country_data, file, indent=2)
            else:
                print(
                    f"----------\nWARNING: No PSD country data for {name} to {country_name.capitalize()} "
                    f"for {psd_market_year} Marketing Year\n----------"
                )
                
    print("Done.\n==========")