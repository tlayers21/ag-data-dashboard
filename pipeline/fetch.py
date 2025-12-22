import requests, json
from pathlib import Path
from typing import List, Dict, Any
from .utils import raw_data_path
BASE_URL = "https://api.fas.usda.gov"

class USDAClient:
    def __init__(self, api_key: str, base_dir: Path) -> None:
        self.api_key = api_key
        self.base_dir = base_dir

        
    def _get(self, endpoint: str) -> List[Dict[str, Any]]:
        url = BASE_URL + endpoint
        params = {"api_key": self.api_key}

        response = response.get(url, params=params)
        if response.status_code != 200:
            raise Exception(
                f"USDA API Error {response.status_code}: {response.text}"
            )
        
        return response.json()
    
    def save_raw_data(self, data, filename: str) -> Path:
        raw_dir = self.base_dir/"data"/"raw"
        raw_dir.mkdir(parents=True, exist_ok=True)

        raw_path = raw_dir/filename
        with open(raw_path, "w") as f:
            json.dump(data, f, indent=2)
        
        return raw_path
    
    def esr_exports_all(self, commodity_code: str, market_year: str) -> List[Dict[str, Any]]:
        endpoint = f"/api/esr/exports/commodityCode/{commodity_code}/allCountries/marketYear/{market_year}"
        return self._get(endpoint)
