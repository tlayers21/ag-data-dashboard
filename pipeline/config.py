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

    "soybean_meal": {
        "esr": {
            "commodity": "901", # Soybean cake & meal
            "countries": ["1220", "2", "2010", "2050"]
        },
        "psd": {
            "commodity": "0813100",
            "countries": ["US","MX", "E4", "JA", "CH"]
        }
    },

    "soybean_oil": {
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
    "2": "european_union",
    "2010": "japan",
    "2050": "china"
}

PSD_COUNTRY_NAMES = {
    "US": "united_states",
    "MX": "mexico",
    "E4": "european_union",
    "JA": "japan",
    "CH": "china"
}

PSD_ATTRIBUTE_IDS = {
    4: "Area Harvested",
    7: "Crush",
    20: "Beginning Stocks",
    28: "Production",
    57: "Imports",
    81: "TY Imports",
    84: "TY Imp. from U.S.",
    86: "Total Supply",
    88: "Exports",
    113: "TY Exports",
    125: "Domestic Consumption",
    130: "Feed Dom. Consumption",
    140: "Industrial Dom. Cons.",
    149: "Food Use Dom. Cons.",
    161: "Feed Waste Dom. Cons.",
    176: "Ending Stocks",
    178: "Total Distribution",
    181: "Extr. Rate",
    184: "Yield",
    192: "FSI Consumption",
    194: "SME"
}

"""
DO LATER
ETHANOL = {
    "endpoint": "petroleum/sum/sndw/data",
    "product": "EPOOXE",
    "areas": ["NUS", "NUS-Z00"]
}
"""