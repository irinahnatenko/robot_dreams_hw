import os
import requests
import json
from dotenv import load_dotenv

def fetch_sales_data(raw_dir: str, date: str) -> None:
    """
    Fetch sales data from external API and save it locally.
    """
    url = "https://fake-api-vycpfa6oca-uc.a.run.app/"
    response = requests.post(url, json={"date": date})

    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code}, {response.text}")

    sales_data = response.json()

    os.makedirs(raw_dir, exist_ok=True)

    # Save to file
    file_path = os.path.join(raw_dir, f"sales_{date}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sales_data, f, indent=2, ensure_ascii=False)
