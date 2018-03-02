# Laboratorium 1

Proszę przerobić stronę tabelkową na współczesną.

<http://prezydent2000.pkw.gov.pl/wb/wb.html>

Konkretnie:

* usunięcie tabelek
* zamiana divów w listach na elementy li
* wprowadzenie semantycznej treści zgodnie z http://www.w3schools.com/html/html5_semantic_elements.asp (header, nav, section, footer)
* sensowne ułożenie elementów na stronie
* (opcjonalnie)wykorzystanie zewnętrznych bibliotek JS do mapy i wykresu

# Zaliczeniowe zadanie laboratoryjne 1
Będziemy przygotowywać generator współczesnej wizualizacji wyborów prezydenckich z 2000 roku. http://prezydent2000.pkw.gov.pl/gminy/index.html

Należy przygotować generator stron HTML, który weźmie wyniki (pliki w excelu lub skonwertowane csv) wyborów i przygotuje zestaw stron:

* Wyniki wyborów w całym kraju plus mapka z województwami, na których można klikać
* Wyniki wyborów w każdym z województw plus odnośniki do okręgów
* Wyniki wyborów w każdym okręgu plus odnośniki do gmin
* Wyniki wyborów w każdej gminie w podziale na obwody

Wszystkie podstrny są bardzo podobne, więc wystarczy przerobić stronę główną plus ew. podstronę jednej gminy (przyda się później)
Wymagania dodatkowe

* Powinien być generowany poprawny HTML
* Powinien być generowany porawny CSS
* Strona powinna być responsywna (odpowiedino zachowywać się przy zmianie rozmiaru, w tym do rozmiaru ekranu komórki)