import os
import requests
import json
from dotenv import load_dotenv

def fetch_sales_data(page: str, date: str) -> None:
    """
    Fetch sales data from external API and save it locally.
    """
    url = "https://fake-api-vycpfa6oca-uc.a.run.app/sales"
    response = requests.post(url, json={"date": date}, json={"page": page})

    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code}, {response.text}")

    sales_data = response.json()

    os.makedirs(page, exist_ok=True)

    # Save to file
    file_path = os.path.join(page, f"sales_{date}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sales_data, f, indent=2, ensure_ascii=False)
