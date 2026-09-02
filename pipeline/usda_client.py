import random
import requests
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import List, Dict, Any

USDA_BASE_URL = "https://api.fas.usda.gov"

# (connect, read)
REQUEST_TIMEOUT = (10, 30)

# How many times one endpoint is tried before the run gives up on it
MAX_ATTEMPTS = 4

# Backoff between attempts
BACKOFF_BASE = 2
BACKOFF_JITTER = 0.5

# Statuses worth another attempt
RETRY_STATUSES = {429, 500, 502, 503, 504}

# How FAS returns when it is being asked for too much
THROTTLE_STATUSES = {429, 503}

THROTTLE_COOLDOWN = 5.0
MAX_COOLDOWN = 60.0
COOLDOWN_DECAY = 0.5

# Ceiling on how long a single Retry-After header is allowed to park the run
MAX_RETRY_AFTER = 120.0

class USDAFetchError(Exception):
    """A USDA endpoint could not be fetched after repeated attempts."""

class USDAClient:
    def __init__(self, usda_api_key: str) -> None:
        self.usda_api_key = usda_api_key
        self.session = requests.Session()
        self._cooldown = 0.0

    # Builds URL
    def _build_url(self, endpoint: str) -> str:
        return f"{USDA_BASE_URL}{endpoint}"

    # Backoff delay for a given attempt
    def _backoff(self, attempt: int) -> float:
        return BACKOFF_BASE ** attempt + random.uniform(0, BACKOFF_JITTER)

    # Slows every later request down after FAS pushes back
    def _register_throttle(self) -> None:
        self._cooldown = min(max(self._cooldown * 2, THROTTLE_COOLDOWN), MAX_COOLDOWN)

    # Eases off the cooldown once the API starts cooperating again
    def _decay_cooldown(self) -> None:
        self._cooldown *= COOLDOWN_DECAY
        if self._cooldown < 1:
            self._cooldown = 0.0

    # Waits out whatever cooldown an earlier throttling response left behind
    def _wait_out_cooldown(self) -> None:
        if self._cooldown > 0:
            print(f"Throttled Earlier - Waiting {self._cooldown:.1f}s Before Next Request")
            time.sleep(self._cooldown)

    # Reads Retry-After, which is either a delay in seconds or an HTTP date
    def _parse_retry_after(self, response: requests.Response) -> float | None:
        value = response.headers.get("Retry-After")
        if not value:
            return None

        try:
            return min(float(value), MAX_RETRY_AFTER)
        except ValueError:
            pass

        try:
            retry_at = parsedate_to_datetime(value)
        except (TypeError, ValueError):
            return None

        if retry_at.tzinfo is None:
            retry_at = retry_at.replace(tzinfo=timezone.utc)

        delay = (retry_at - datetime.now(timezone.utc)).total_seconds()
        return min(max(delay, 0.0), MAX_RETRY_AFTER)

    # Fetches data from USDA FAS API, retrying transient failures and throttling
    def _get(self, endpoint: str) -> List[Dict[str, Any]]:
        usda_url = self._build_url(endpoint)
        params = {"api_key": self.usda_api_key}
        last_error: Exception | None = None

        for attempt in range(1, MAX_ATTEMPTS + 1):
            if attempt == 1:
                self._wait_out_cooldown()

            delay = self._backoff(attempt)

            try:
                response = self.session.get(usda_url, params=params, timeout=REQUEST_TIMEOUT)
            except requests.exceptions.RequestException as error:
                last_error = error
                reason = type(error).__name__
                # FAS tends to express rate limiting by resetting the connection
                if isinstance(error, requests.exceptions.ConnectionError):
                    self._register_throttle()
            else:
                if response.status_code == 200:
                    self._decay_cooldown()
                    try:
                        return response.json()
                    except Exception:
                        print("USDA Fetching Error: Response was not valid JSON")
                        return {}

                # Nothing published for this commodity/country/year combination
                if response.status_code == 404:
                    self._decay_cooldown()
                    return {}

                if response.status_code not in RETRY_STATUSES:
                    print(f"Error: {response.status_code}, {response.text}")
                    return {}

                last_error = USDAFetchError(f"HTTP {response.status_code} from {endpoint}")
                reason = f"HTTP {response.status_code}"

                if response.status_code in THROTTLE_STATUSES:
                    self._register_throttle()
                    retry_after = self._parse_retry_after(response)
                    if retry_after is not None:
                        delay = retry_after
                        reason = f"HTTP {response.status_code}, Retry-After {retry_after:.0f}s"

            if attempt == MAX_ATTEMPTS:
                break

            print(f"  Retry {attempt}/{MAX_ATTEMPTS - 1} In {delay:.1f}s ({reason})")
            time.sleep(delay)

        raise USDAFetchError(
            f"USDA request failed after {MAX_ATTEMPTS} attempts: {endpoint}"
        ) from last_error

    # ESR from all countries fetching
    def esr_all_countries(self, commodity_code: str, marketing_year: int) -> List[Dict[str, Any]]:
        endpoint = f"/api/esr/exports/commodityCode/{commodity_code}/allCountries/marketYear/{marketing_year}"
        return self._get(endpoint)

    # ESR from a specific country fetching
    def esr_country(self, commodity_code: str, country_code: str, marketing_year: int) -> List[Dict[str, Any]]:
        endpoint = f"/api/esr/exports/commodityCode/{commodity_code}/countryCode/{country_code}/marketYear/{marketing_year}"
        return self._get(endpoint)

    # PSD world fetching
    def psd_world(self, commodity_code: str, market_year: str) -> List[Dict[str, Any]]:
        endpoint = f"/api/psd/commodity/{commodity_code}/world/year/{market_year}"
        return self._get(endpoint)

    # PSD from a specific country fetching
    def psd_country(self, commodity_code: str, country_code: str, market_year: str) -> List[Dict[str, Any]]:
        endpoint = f"/api/psd/commodity/{commodity_code}/country/{country_code}/year/{market_year}"
        return self._get(endpoint)
