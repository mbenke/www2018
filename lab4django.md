---
title: Aplikacje WWW
subtitle: Import CSV, Django
author: Marcin Benke
date: 23 marca 2018
---

# Python 3

Polecam używanie Python 3, zwłaszcza z uwagi na Unicode

```
$ which python3
/usr/bin/python3
$ virtualenv -p /usr/bin/python3 lab3
Running virtualenv with interpreter /usr/bin/python3
Using base prefix '/usr'
New python executable in /home/ben/venv/lab3/bin/python3
Also creating executable in /home/ben/venv/lab3/bin/python
Installing setuptools, pip, wheel...done.
```

# Import CSV

``` python
import csv

with open('gm-okr01.csv', 'r', encoding='utf-8') as csvfile:
    freader = csv.reader(csvfile, dialect='excel', delimiter=',')
    wyniki = [row for row in freader]

for i in range(5):
    print(wyniki[i])
```

# Django - instalacja i tutorial

```
$ source ~/venv/lab3/bin/activate
(lab3) $ pip install django ipython
```

Na początek proponuję szybko przerobić tutorial, części 1 i 2

<https://docs.djangoproject.com/en/2.0/intro/tutorial01/>

# Zadania z modeli

Zadania z modeli

* Napisz modele dla: kandydata, obwodu, gminy,i okręgu (nie cała gmina jest w okręgu) i wyniku kandydata w obwodzie
* Zaimportuj dane z pliku CSV
* Wypisz sumę głosów dla każdego kandydata w całym kraju (imię, nazwisko, liczba głosów)
* Wypisz sumę głosów dla każdego kandydata w podziale na okręgi (numer okręgu, imię, nazwisko, liczba głosów)
* Wypisz obwody w których brakuje wyników dla co najmniej jednego z kandydatów (nazwa gminy, numer obwodu)
* Wypisz obwody w których brakuje wyników dokładnie jednego z kandydatów (nazwa gminy, numer obwodu)
* Wypisz największą i najmniejszą liczbę głosów, którą uzyskał każdy z kandydatów w obwodach w których uprawnionych do głosowania było między 1000 a 2000 osób

# Tworzenie projektu i aplikacji

```
(lab3) Django$ django-admin startproject lab4
(lab3) Django$ ls lab4
lab4  manage.py
(lab3) Django$ cd lab4 && ./manage.py startapp a
(lab3) lab4$ ls
a  lab4  manage.py
(lab3) lab4$ emacs -nw lab4/settings.py
INSTALLED_APPS = [
...
    'a',
]
```

# Edycja modeli