import requests
from typing import Any

USDA_BASE_URL = "https://api.fas.usda.gov"

class USDAClient:
    def __init__(self, usda_api_key: str) -> None:
        self.usda_api_key = usda_api_key

    def _build_url(self, endpoint: str) -> str:
        return f"{USDA_BASE_URL}{endpoint}"
    
    def _get(self, endpoint: str) -> dict[str, Any]:
        usda_url = self._build_url(endpoint)
        params = {"api_key": self.usda_api_key}

        response = requests.get(usda_url, params=params)

        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return {}
        
        try:
            return response.json()
        except Exception:
            print("USDA Fetching Error: Response was not valid JSON")
            return {}
    
    # ESR Methods
    def esr_all_countries(self, commodity_code: str, marketing_year: int) -> list[dict[str, Any]]:
        endpoint = f"/api/esr/exports/commodityCode/{commodity_code}/allCountries/marketYear/{marketing_year}"
        return self._get(endpoint)
    
    def esr_country(self, commodity_code: str, country_code: str, marketing_year: int) -> list[dict[str, Any]]:
        endpoint = f"/api/esr/exports/commodityCode/{commodity_code}/countryCode/{country_code}/marketYear/{marketing_year}"
        return self._get(endpoint)

    # PSD Methods
    def psd_world(self, commodity_code: str, market_year: str) -> list[dict[str, Any]]:
        endpoint = f"/api/psd/commodity/{commodity_code}/world/year/{market_year}"
        return self._get(endpoint)
    
    def psd_country(self, commodity_code: str, country_code: str, market_year: str) -> list[dict[str, Any]]:
        endpoint = f"/api/psd/commodity/{commodity_code}/country/{country_code}/year/{market_year}"
        return self._get(endpoint)