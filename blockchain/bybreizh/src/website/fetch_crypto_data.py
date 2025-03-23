# Fichier permettant de stocker les valeurs des cryptos sur les 7 derniers jours afin de compute les graphs sur le site web.

import requests
import json
from datetime import datetime

CRYPTO_IDS = ["bitcoin", "ethereum", "cardano", "solana", "ripple", "polkadot"]

DATA_FILE = "crypto_data.json"

def fetch_data():
    url = "https://api.coingecko.com/api/v3/coins/{}/market_chart"
    params = {"vs_currency": "usd", "days": 7}
    local_data = {}

    for crypto_id in CRYPTO_IDS:
        try:
            response = requests.get(url.format(crypto_id), params=params)
            if response.ok:
                data = response.json()
                local_data[crypto_id] = data
            else:
                print(f"Erreur pour {crypto_id}: {response.status_code}")
        except Exception as e:
            print(f"Échec de récupération pour {crypto_id}: {e}")

    # Enregistrement dans un fichier JSON
    with open(DATA_FILE, "w") as f:
        json.dump(local_data, f, indent=4)

    print("Données des cryptos enregistrées localement.")

if __name__ == "__main__":
    fetch_data()
