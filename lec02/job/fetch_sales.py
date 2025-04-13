import os
import requests
import json
from dotenv import load_dotenv

load_dotenv(".env")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
API_URL = "https://fake-api-vycpfa6oca-uc.a.run.app/sales"

def fetch_sales_data(page: str, date: str, raw_dir: str) -> None:
    """Fetch sales data from API and save it locally."""

    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    params = {"date": date, "page": page}


response = requests.get(API_URL, params=params, headers=headers)
if response.status_code == 200:
    with open("C:/Users/User/robot_dreams_hw/lec02/sales_2022-08-09_1.json", "w", encoding="utf-8") as f:
        json.dump(response.json(), f, indent=2, ensure_ascii=False)
    print("✅ Данные сохранены!")
else:
    print(f"Ошибка API: {response.status_code}, {response.text}")

    sales_data = response.json()

    os.makedirs(raw_dir, exist_ok=True)
    file_path = os.path.join(raw_dir, f"sales_{date}_{page}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sales_data, f, indent=2, ensure_ascii=False)

    print(f"Данные сохранены: {file_path}")

