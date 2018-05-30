# -*- encoding=utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
# Uruchomienie
driver = webdriver.Chrome()
driver.get("http://localhost:8000")

# Sprawdzenie tytułu okna
assert u'Aukcja Używany kapeć' in driver.title

# Znajdujemy aktualną cenę i obliczamy nową
elem = driver.find_element_by_css_selector(
    "span#current-price")
currentPrice = int(elem.text)
newPrice = str(currentPrice + 1)

# Wpisanie nowej ceny
elem = driver.find_element_by_css_selector("input#price")
elem.send_keys(newPrice)

# Klik
elem = driver.find_element_by_css_selector("button#bid")
elem.click()

# Czekanie
wait = WebDriverWait(driver, 10)
wait.until(expect.text_to_be_present_in_element(
        (By.ID, 'current-price'), newPrice))

# Finale
driver.close()
print("OK")

