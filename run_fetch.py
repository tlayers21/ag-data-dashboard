from pipeline.fetch_all import fetch_all_data

if __name__ == "__main__":
    USDA_API_KEY = "GA0LAyk7zcLgEjKMdSfOIOl7GJmL4wRleIlflcfp"
    ESR_MARKET_YEAR = "2026"
    PSD_MARKET_YEAR = "2025"

    data = fetch_all_data(usda_api_key=USDA_API_KEY, esr_market_year=ESR_MARKET_YEAR, psd_market_year=PSD_MARKET_YEAR)