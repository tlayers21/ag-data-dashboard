import requests

API_BASE = "http://localhost:8000"

def fetch_data_last5years(data: str, commodity: str, country: str) -> list:
    params = {
        "commodity": commodity.lower(),
        "country": country.lower()
    }

    url = f"{API_BASE}/{data}/weekly/last5years"
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return []
        
    try:
        return response.json()
    except Exception:
        print("Database Fetching Error: Response was not valid JSON")
        return []