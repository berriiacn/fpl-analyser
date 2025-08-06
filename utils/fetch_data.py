import requests
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
URL = "https://fantasy.premierleague.com/api/bootstrap-static/"

def fetch_fpl_data():
    print("Fetching FPL data...")
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(os.path.join(DATA_DIR, 'bootstrap_static.json'), 'w') as f:
            json.dump(data, f, indent=2)
        print("✅ Data saved to data/bootstrap_static.json")
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    fetch_fpl_data()
# This script fetches the Fantasy Premier League data and saves it to a JSON file.
# It can be run directly to update the data.