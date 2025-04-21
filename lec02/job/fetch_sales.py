import os
import json
import requests
from dotenv import load_dotenv

load_dotenv(".env")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
API_URL = "https://fake-api-vycpfa6oca-uc.a.run.app/sales"

def fetch_sales_data(page: str, date: str, raw_dir: str) -> None:
<<<<<<< HEAD
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

    os.makedirs(raw_dir, exist_ok=True)

    # Сохранение JSON-файла
    file_path = os.path.join(raw_dir, f"sales_{date}_{page}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sales_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Данные сохранены: {file_path}")

# 🔹 Вызов функции для проверки
fetch_sales_data("1", "2022-08-09", "C:/Users/User/robot_dreams_hw/lec02/job/raw/sales/")


=======
    """Fetch sales data from API и сохранить его локально."""
    
    headers = {'Authorization': AUTH_TOKEN}
    params = {"date": date, "page": page}

    response = requests.get(API_URL, params=params, headers=headers)
    
    if response.status_code == 200:
        os.makedirs(raw_dir, exist_ok=True)
        file_path = os.path.join(raw_dir, f"sales_{date}_{page}.json")
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(response.json(), f, indent=2, ensure_ascii=False)
        
        print(f"✅ Данные сохранены: {file_path}")
    else:
        print(f"Ошибка API: {response.status_code}, {response.text}")

# Вызов функции
fetch_sales_data("1", "2022-08-09", "C:/Users/User/robot_dreams_hw/lec02/raw/sales")

>>>>>>> 22ed162 (Edits done)

