import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# config
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# chromedriver ścieżka
service = Service("Y:\\chromedriver.exe")

def scrape_data():
    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = "https://www.livescore.com/en/football/champions-league/league-stage/table/"
    driver.get(url)
    driver.implicitly_wait(20)

    data = []

    try:
        rows_with_wv = driver.find_elements(By.XPATH, "//tr[.//td[contains(@class, 'wv')]]")
        if rows_with_wv:
            print("Znalezione wiersze z wartością wv:")
            for row in rows_with_wv:
                try:
                    wv_value = row.find_element(By.XPATH, ".//td[contains(@class, 'wv')]").text
                    team_name = row.find_element(By.XPATH, ".//td[contains(@class, 'Zg')]//a").text
                    data.append({"position": wv_value, "team_name": team_name})
                except Exception as e:
                    print(f"Błąd podczas pobierania danych z wiersza: {e}")
        else:
            print("Nie znaleziono wierszy z wartością wv.")
    except Exception as e:
        print(f"Błąd podczas scrapowania: {e}")
    finally:
        driver.quit()

    # zapis
    file_path = "Y:\\xampp\\htdocs\\ucl\\teams_data.json"
    data_sorted = sorted(data, key=lambda x: x['team_name'])
    with open(file_path, "w") as file:
        json.dump(data_sorted, file)
    print(f"Dane zostały zapisane do pliku: {file_path}")

# loop co 60 sek
while True:
    print("Rozpoczynam scrapowanie danych...")
    scrape_data()
    print("Oczekiwanie 60 sekund...")
    time.sleep(60)
