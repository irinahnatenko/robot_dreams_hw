import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
API_URL = "https://fake-api-vycpfa6oca-uc.a.run.app/sales"

def fetch_sales_data(page: str, date: str, raw_dir: str) -> None:
    """Fetch sales data from API and save it locally."""

    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    params = {"date": date, "page": page}

    try:
        response = requests.get(API_URL, params=params, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к API: {e}")
        return None

    sales_data = response.json()

    os.makedirs(raw_dir, exist_ok=True)
    file_path = os.path.join(raw_dir, f"sales_{date}_{page}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sales_data, f, indent=2, ensure_ascii=False)

    print(f"Данные сохранены: {file_path}")

