from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import datetime
from pymongo import MongoClient

# Ne conectam la MongoDB local!
client = MongoClient("mongodb://localhost:27017/")

# Alegem numele database!
db = client["proiect_crypto"] 

# Alegem colectia!
collection = db["istoric_preturi"]

# Configurare Browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

lista_monede = [
    'bitcoin', 'ethereum', 'tether', 'bnb', 'solana', 'xrp', 'cardano', 
    'avalanche', 'dogecoin', 'tron', 'polkadot', 'chainlink', 
    'wrapped-bitcoin', 'shiba-inu', 'litecoin', 'bitcoin-cash', 'uniswap', 
    'toncoin', 'cosmos', 'monero', 'ethereum-classic', 'stellar', 
    'internet-computer', 'filecoin', 'hedera', 'aptos',
    'leo-token' 
]

print(f"{'NUME':<20} | {'PRET':<15} | {'MODIFICARE (24h)':<15}")
print("-" * 60)

for moneda in lista_monede:
    try:
        driver.get(f"https://coinmarketcap.com/currencies/{moneda}/")
        time.sleep(2)

        # Extragerea numelui!
        nume = driver.title.split(" price today")[0]
        
        # Extragerea pretului!
        pret_element = driver.find_element(By.CSS_SELECTOR, 'span[data-test="text-cdp-price-display"]')
        pret = pret_element.text

        # Extragerea procentajului!
        try:
            change_element = driver.find_element(By.CSS_SELECTOR, 'p[data-change]')
            procent_text = change_element.text.strip()
            directie = change_element.get_attribute('data-change')
            
            if directie == 'up':
                change = f"+{procent_text}"
            elif directie == 'down':
                if not procent_text.startswith('-'):
                    change = f"-{procent_text}"
                else:
                    change = procent_text
            else:
                change = procent_text
                
        except Exception as e:
            change = "N/A"

        # Salvvare si stocare data de baze!
        pachet_date = {
            "nume_moneda": nume,
            "pret": pret,
            "modificare_24h": change,
            "timestamp": datetime.datetime.now()
        }
        
        # Trimitem pachetul in baza de date
        collection.insert_one(pachet_date)

        # Afisare frumos!
        print(f"{nume:<20} | {pret:<15} | {change:<15}")

    except Exception:
        print(f"{moneda:<20} | EROARE (Link invalid sau timeout)")

print("-" * 60)
driver.quit()

# -->Comenzi ajutatoare prima parte:
# Set-ExecutionPolicy Unrestricted -Scope Process
# .\venv\Scripts\activate
# pip install selenium webdriver-manager beautifulsoup4 lxml flask pymongo requests
