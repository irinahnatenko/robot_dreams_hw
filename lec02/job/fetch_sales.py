import os
import requests
import json
from dotenv import load_dotenv

# Загрузка токена из .env
load_dotenv(".env")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
API_URL = "https://fake-api-vycpfa6oca-uc.a.run.app/sales"

def fetch_sales_data(page: str, date: str, raw_dir: str) -> None:
    """Запрашивает данные о продажах и сохраняет их в файл."""
    
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    params = {"date": date, "page": page}

    try:
        response = requests.get(API_URL, params=params, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка API: {e}")
        return None

    sales_data = response.json()

    # Создание папки, если она не существует
    os.makedirs(raw_dir, exist_ok=True)

    # Сохранение JSON-файла
    file_path = os.path.join(raw_dir, f"sales_{date}_{page}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sales_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Данные сохранены: {file_path}")

# 🔹 Вызов функции для проверки
fetch_sales_data("1", "2022-08-09", "C:/Users/User/robot_dreams_hw/lec02/job/raw/sales/")



