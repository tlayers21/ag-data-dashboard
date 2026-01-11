COMMODITIES = {
    "corn": {
        "esr": {
            "commodity": "401",
            "countries": ["1220", "2", "2010", "2050"]
        },
        "psd": {
            "commodity": "0440000",
            "countries": ["US","MX", "E4", "JA", "CH"]
        }
    },

    "soybeans": {
        "esr": {
            "commodity": "801",
            "countries": ["1220", "2", "2010", "2050"]
        },
        "psd": {
            "commodity": "2222000", # Oilseed, Soybean
            "countries": ["US","MX", "E4", "JA", "CH"]
        }
    },

    "soybean meal": {
        "esr": {
            "commodity": "901", # Soybean cake & meal
            "countries": ["1220", "2", "2010", "2050"]
        },
        "psd": {
            "commodity": "0813100",
            "countries": ["US","MX", "E4", "JA", "CH"]
        }
    },

    "soybean oil": {
        "esr": {
            "commodity": "902",
            "countries": ["1220", "2", "2010", "2050"]
        },
        "psd": {
            "commodity": "4232000",
            "countries": ["US","MX", "E4", "JA", "CH"]
        }
    },

    "wheat": {
        "esr": {
            "commodity": "107",
            "countries": ["1220", "2", "2010", "2050"]
        },
        "psd": {
            "commodity": "0410000",
            "countries": ["US","MX", "E4", "JA", "CH"]
        }
    }
}

ESR_COUNTRY_NAMES = {
    "1220": "mexico",
    "2": "european union",
    "2010": "japan",
    "2050": "china"
}

PSD_COUNTRY_NAMES = {
    "00": "world",
    "US": "united states",
    "MX": "mexico",
    "E4": "european union",
    "JA": "japan",
    "CH": "china"
}

"""
DO LATER
ETHANOL = {
    "endpoint": "petroleum/sum/sndw/data",
    "product": "EPOOXE",
    "areas": ["NUS", "NUS-Z00"]
}
"""

DATA_BASE_URL = "postgresql://tlayers21:mustard33@localhost:5432/commodity_data"