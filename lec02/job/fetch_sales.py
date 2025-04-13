import os 
import requests 
import shutil
from pathlib import Path

API_URL = 'https://fake-api-vycpfa6oca-uc.a.run.app/sales?date=2022-08-09&page=1'

def fetch_sales_data(raw_dir, date):
  path = Path(raw_dir) / 'sales' / date
  if path.exists():
    shutil.rmtree(path)
  path.mkdir(parents=True, exist_ok=True)

  token = os.getenv("AUTH_TOKEN")
  if not token:
      raise EnvironmentError("AUTH_TOKEN is not set")

  page = 1
  while True:
      response = requests.get(API_URL, params={'date': date, 'page': page}, headers={'Authorization': f'Bearer {token}'})
      if response.status_code != 200:
          raise Exception(f"API error: {response.status_code}")
        
      data = response.json()
      if not data.get("data"):
          break  # якщо нема даних — зупинка

      filename = f'sales_{date}.json' if page == 1 else f'sales_{date}_{page}.json'
      with open(path / filename, 'w', encoding='utf-8') as f:
          f.write(response.text)

      if not data.get("has_more"):
          break
      page += 1
