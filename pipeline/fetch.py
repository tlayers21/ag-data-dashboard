import requests, json
from pathlib import Path
from .utils import raw_data_path

BASE_URL = "https://api.fas.usda.gov"

class USDAClient:
    def __init__(self, api_key: str, base_dir: Path) -> None:
        self.api_key = api_key
        self.base_dir = base_dir

        
    def _get(self, endpoint: str) -> any
        url = BASE_URL + endpoint
        params = {"api_key": self.api_key}

        response = response.get(url, params=params)
        if response.status_code != 200:
            raise Exception(
                f"USDA API Error {response.status_code}: {response.text}"
            )
        
        return response.json()