import json
import time
import os
import subprocess
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
# ścieżka teams_data.json (pliku z danymi)
file_path = "Y:\\xampp\\htdocs\\ucl\\teams_data.json"

# sprawdzanie czasu modyfikacji pliku
def get_file_modification_time(file_path):
    return os.path.getmtime(file_path)

#sprawdzanie czasu ostatniego commitu
def get_last_commit_time():
    result = subprocess.run(
        ['git', 'log', '-1', '--format=%ct'], capture_output=True, text=True
    )
    if result.returncode == 0:
        return int(result.stdout.strip())
    else:
        raise Exception("Błąd podczas pobierania ostatniego commitu.")

# wymuszanie commitu
def force_commit_if_modified():
    try:
        # Pobierz czas modyfikacji pliku i czas ostatniego commitu
        file_mod_time = get_file_modification_time(file_path)
        last_commit_time = get_last_commit_time()

        # Porównaj czasy
        if file_mod_time > last_commit_time:
            print("Plik został zmodyfikowany po ostatnim commicie. Wykonuję commit...")
            subprocess.run(['git', 'add', file_path])  # Dodaj zmiany do staging area
            subprocess.run(['git', 'commit', '-m', 'Automatyczny commit po zmianie pliku'])
            print("Wykonuję push do zdalnego repozytorium...")
            subprocess.run(['git', 'push', 'origin', 'main'])  # Zakładając, że główną gałęzią jest 'main'
        else:
            print("Brak zmian w pliku po ostatnim commicie.")
    except Exception as e:
        print(f"Błąd: {e}")



# datascraping
def scrape_data():
    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = "https://www.livescore.com/en/football/italy/serie-a/table/"
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
    data_sorted = sorted(data, key=lambda x: x['team_name'])
    with open(file_path, "w") as file:
        json.dump(data_sorted, file)
    with open(file_path, "a") as file:
        file.write("\n")
    print(f"Dane zostały zapisane do pliku: {file_path}")

# loop co 60 sek
while True:
    print("Rozpoczynam scrapowanie danych...")
    scrape_data()
    force_commit_if_modified()
    print("Oczekiwanie 60 sekund...")
    time.sleep(60)
