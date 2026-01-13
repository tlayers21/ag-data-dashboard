import requests
from typing import List, Dict, Any

AGDATA_BASE_URL = "https://ag-data-dashboard-6908.onrender.com"

class AgDataClient:
    def __init__(self) -> None:
        pass    

    # Builds URL
    def _build_url(self, endpoint: str) -> str:
        return f"{AGDATA_BASE_URL}{endpoint}"
    
    # Fetches specified data from API which communicates with database
    def get(self, data_type, commodity: str, country: str) -> List[Dict[str, Any]]:
        endpoint = f"/{data_type}/last5years"
        agdata_url = self._build_url(endpoint)

        params = {
            "commodity": commodity.lower(),
            "country": country.lower()
        }

        response = requests.get(agdata_url, params=params)

        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return []
        
        try:
            return response.json()
        except Exception:
            print("Agdata Fetching Error: Response was not valid JSON")
            return []