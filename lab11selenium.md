# Selenium

[Selenium](http://www.seleniumhq.org) to framework do automatyzacji czynności wykonywanych w
przeglądarce internetowej.

Jest w stanie automatyzować wyszukiwanie elementów, wpisywanie znaków
w formularz, klikanie na guziki i inne.

Wszystko to dzieje się w prawdziwej
przeglądarce z jej natywną implementacją JavaScript i innych technologii.
Wspierane są najpopularniejsze przeglądarki, m. in. Firefox, Chrome, IE,
Safari, Opera.

Możemy sobie wybrać na czym testujemy.

# Selenium - warianty

Jest kilka produktów Selenium:

* Selenium WebDriver - służy do automatycznego wykonywania
czynności w przeglądarce za pomocą skryptu w języku programowania
Python, Java, C#, Ruby, Perl lub PHP;
* Selenium IDE - to add-on do Firefoxa, który nagrywa makra z
czynności które ręcznie wykonujemy w przeglądarce, a potem
odtwarza je;
* Selenium Grid - gdybyśmy chcieli odpalić testy na wielu serwerach z
różnymi konfiguracjami;
* Selenium Remote Control - kontrolowanie przeglądarki uruchomionej
na innym serwerze lub lokalnie jako aplikacja klient-serwer.

My będziemy używać Selenium WebDrivera do testów automatycznych.

# Selenium w Pythonie

Instalacja selenium w virtualenv

```
$ virtualenv ve
$ source ve/bin/activate
(ve)$ pip install selenium
```

Tu jest dobry tutorial/dokumentacja na początek:

[http://selenium-python.readthedocs.org.](http://selenium-python.readthedocs.org.)

Aby sterować przeglądarką należy jeszczwe zainstalować [chromedriver](https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver) lub geckodriver.

# Przykład 1

```
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.send_keys("django")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source

driver.close()
```

# Przykład 2 - aukcje

* Prosta aplikacja z aukcjami
* Sprawdź tytuł aukcji
* Znajdź pole z ceną
* Wpisz nową
* Kliknij Licytuj
* Sprawdź że działa cena wyższa, nie da się wprowadzić ceny niższej niż dotychczasowa

# 02auctions.py

```
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
```

# Otwieranie przeglądarki

Otwieranie przeglądarki
```
driver = webdriver.Chrome()
```
Stworzenie obiektu drivera otwiera przeglądarkę podłączoną pod selenium. W tym przypadku otwierany jest Chrome i otwierane jest jego okno.

Otwieranie strony w przeglądarce
```
driver.get("http://localhost:8000")
```

# Sprawdzenie tytułu

```
assert u'Aukcja Używany kapeć' in driver.title
```

Sprawdzamy czy tutuł zawiera podany napis

# Wybór elementu i jego zawartości tekstowej

```
elem = driver.find_element_by_css_selector(
    "span#current-price")
currentPrice = int(elem.text)
newPrice = str(currentPrice + 1)
```

Znajdujemy element z obecną ceną za pomocą selektora CSS i pobieramy z niego obecną wartość tekstową. Jeżeli element nie zostanie znaleziony to będzie rzucony wyjątek. Konwertujemy cenę na inta i obliczamy podbitą cenę.

# Interakcja z formularzem

```
elem = driver.find_element_by_css_selector("input#price")
elem.send_keys(newPrice)
```

Znajdujemy pole do wpisania nowej ceny i symulujemy wpisywanie znaków.

```
elem = driver.find_element_by_css_selector("button#bid")
elem.click()
```

Znajdujemy guzik do wysłania nowej ceny i symulujemy kliknięcie. W tym momencie przeglądarka wysyła formularz.

Ponieważ aplikacja jest Ajaxowa, zaczyna wykonywać asynchronicznie żądanie AJAX.

# Czekanie na zmianę tekstu

```
wait = WebDriverWait(driver, 10)
wait.until(expected_conditions.
    text_to_be_present_in_element(
    (By.ID, ’current-price’), newPrice))
```

Potrzebujemy mechanizmu do poczekania na wykonanie się AJAXa lub innej akcji - waita. Czekamy do 10 sekund aż tekst w elemencie o id current-price zmieni swoją wartość na nową cenę. W przeciwnym razie rzucamy wyjątek. Jest wiele akcji, na które możemy czekać - patrz dokumentacja.

# Zamykanie przeglądarki

 
Zamykanie przeglądarki w przypadku sukcesu:
```
driver.close()
```
W ten sposób zamykamy przeglądarkę. Jeżeli po drodze wystąpi wyjątek to przeglądarka pozostanie otwarta.

Zamykanie przeglądarki zawsze
```
try:
    # skrypt testujacy
finally:
    driver.close()
```
W ten sposób zamykamy przeglądarkę po wykonaniu się testów, nawet jeżeli wystąpi wyjątek.

# 03alert.py

```
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
# Uruchomienie
driver = webdriver.Chrome()
driver.get("http://localhost:8000")
try:
    # Sprawdzenie tytułu okna
    assert u'Aukcja Używany kapeć' in driver.title

    # Znajdujemy aktualną cenę i obliczamy nową
    elem = driver.find_element_by_css_selector(
        "span#current-price")
    currentPrice = elem.text
    newPrice = str(int(currentPrice) - 1)

    # Wpisanie nowej ceny
    elem = driver.find_element_by_css_selector("input#price")
    elem.send_keys(newPrice)

    # Klik
    elem = driver.find_element_by_css_selector("button#bid")
    elem.click()

    # Czekanie
    wait = WebDriverWait(driver, 10)
    wait.until(expect.alert_is_present())
    Alert(driver).dismiss()
    elem = driver.find_element_by_css_selector("span#current-price")
    assert currentPrice == elem.text
finally:
    # Finale
    driver.close()
    print("OK")
```

# Czekanie na alert
```
wait.until(expected_conditions.alert_is_present())
```
W ten sposób czekamy na pojawienie się alertu.

```
Alert(driver).dismiss()
```

W ten sposób zamykamy alert. Gdyby alert zawierał opcję tak/nie, moglibyśmy również użyć `accept()/dismiss()` odpowiednio.

# Materiały

* Dobra nieoficjalna dokumentacja-tutorial: http://selenium-python.readthedocs.org.
* Pełna dokumentacja dla Pythona: http: //selenium.googlecode.com/svn/trunk/docs/api/py/index.html.
* Pełna dokumentacja narzędzia: http://www.seleniumhq.org/docs.
* Łączenie selenium z testami automatycznymi Django: http://agiliq.com/blog/2014/09/selenium-testing/.