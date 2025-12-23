COMMODITIES = {
    "corn": {
        "esr": "401",
        "psd": "0440000",
        "countries": [
            ("MX", "Mexico"),
            ("JA", "Japan"),
            ("CO", "Colombia"),
            ("KS", "South Korea"),
            ("CA", "Canada"),
            ("E4", "European Union"),
            ("TW", "Taiwan"),
        ],
    },
    "soybeans": {
        "esr": "801",
        "psd": "0810000",
        "countries": [
            ("CH", "China"),
            ("E4", "European Union"),
            ("MX", "Mexico"),
            ("ID", "Indonesia"),
            ("EG", "Egypt"),
            ("JA", "Japan"),
            ("TW", "Taiwan"),
        ],
    },
    "wheat": {
        "esr": "107",
        "psd": "0410000",
        "countries": [
            ("MX", "Mexico"),
            ("RP", "Philippines"),
            ("JA", "Japan"),
            ("KS", "South Korea"),
            ("CH", "China"),
            ("TW", "Taiwan"),
            ("E4", "European Union"),
        ],
    },
}

ETHANOL_CONFIG = {
    "endpoint": "petroleum/sum/sndw/data",
    "product": "EPOOXE",
    "areas": ["NUS", "NUS-Z00"],
}