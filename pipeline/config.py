COMMODITIES = {
    "corn": {
        "esr": {
            "commodity": "401",
            "countries": ["1220", "2", "2010", "2050"]
        },
        "psd": {
            "commodity": "0440000",
            "countries": ["MX", "E4", "JA", "CH"]
        }
    },

    "soybeans": {
        "esr": {
            "commodity": "801",
            "countries": ["1220", "2", "2010", "2050"]
        },
        "psd": {
            "commodity": "2222000", # Oilseed, Soybean
            "countries": ["MX", "E4", "JA", "CH"]
        }
    },

    "soybean_meal": {
        "esr": {
            "commodity": "901", # Soybean cake & meal
            "countries": ["1220", "2", "2010", "2050"]
        },
        "psd": {
            "commodity": "0813100",
            "countries": ["MX", "E4", "JA", "CH"]
        }
    },

    "soybean_oil": {
        "esr": {
            "commodity": "902",
            "countries": ["1220", "2", "2010", "2050"]
        },
        "psd": {
            "commodity": "4232000",
            "countries": ["MX", "E4", "JA", "CH"]
        }
    },

    "wheat": {
        "esr": {
            "commodity": "107",
            "countries": ["1220", "2", "2010", "2050"]
        },
        "psd": {
            "commodity": "0410000",
            "countries": ["MX", "E4", "JA", "CH"]
        }
    }
}

ETHANOL = {
    "endpoint": "petroleum/sum/sndw/data",
    "product": "EPOOXE",
    "areas": ["NUS", "NUS-Z00"]
}