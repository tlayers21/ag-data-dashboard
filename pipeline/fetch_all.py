import json
from .config import COMMODITIES, ESR_COUNTRY_NAMES, PSD_COUNTRY_NAMES
from .usda_client import USDAClient
from .utils import raw_data_path
    
def fetch_all_data(usda_api_key: str, esr_market_year: str, psd_market_year: str):
    usda_data = USDAClient(usda_api_key)

    total_data = {}

    print("Starting Data Fetching Process...")
    for name, cfg in COMMODITIES.items():
        print(f"Fetching: {name.capitalize()}")
        commodity_result = {}

        ## ESR
        esr_code = cfg["esr"]["commodity"]
        esr_countries = cfg["esr"]["countries"]

        # For to all countries
        esr_all_data = usda_data.esr_all_countries(esr_code, esr_market_year)
        with open(raw_data_path(f"{name}_esr_all_{esr_market_year}.json"), "w") as file:
            json.dump(esr_all_data, file, indent=2)
        commodity_result["esr_all"] = esr_all_data

        # For to individual countries
        esr_country_data = {}
        for country_code in esr_countries:
            country_data = usda_data.esr_country(esr_code, country_code, esr_market_year)
            country_name = ESR_COUNTRY_NAMES.get(country_code, country_code)
            with open(raw_data_path(f"{name}_esr_to_{country_name}_{esr_market_year}.json"), "w") as file:
                json.dump(country_data, file, indent=2)
            esr_country_data[country_code] = country_data

        ## PSD
        psd_code = cfg["psd"]["commodity"]
        psd_countries = cfg["psd"]["countries"]

        # For world data
        psd_world_data = usda_data.psd_world(psd_code, psd_market_year)
        with open(raw_data_path(f"{name}_psd_world_{psd_market_year}.json"), "w") as file:
            json.dump(psd_world_data, file, indent=2)
        commodity_result["psd_world"] = psd_world_data

        # For to individual countries
        psd_country_data = {}
        for country_code in psd_countries:
            country_data = usda_data.psd_country(psd_code, country_code, psd_market_year)
            country_name = PSD_COUNTRY_NAMES.get(country_code, country_code)
            with open(raw_data_path(f"{name}_psd_{country_name}_{psd_market_year}.json"), "w") as file:
                json.dump(country_data, file, indent=2)
            psd_country_data[country_code] = country_data

        total_data[name] = commodity_result
    
    return total_data
