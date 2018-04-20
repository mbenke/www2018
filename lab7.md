---
title: Aplikacje WWW
author: Marcin Benke
date: 20 kwietnia 2018
---

# Plan

* automatyczne testowanie za pomocą tox
* code coverage
* Bitbucket:
  * założyć sobie konto
  * założyć task,
  * zrealizować,
  * odpalić pipeline do testowania

<https://bitbucket.org/marcinbenke/www-cilab>

# Tox

[tox.readthedocs.io](https://tox.readthedocs.io/)

tox.ini:

```
# Tox (https://tox.readthedocs.io/) is a tool for running tests
# in multiple virtualenvs. This configuration file will run the
# test suite on all supported python versions. To use it, "pip install tox"
# and then run "tox" from this directory.

[tox]
envlist = py36
skipsdist = True # Pomiń krok 'setup.py sdist'

[testenv]
commands = {envpython} manage.py test
deps = -rrequirements.txt
```

# Uruchomienie

```
(lab)➜  www-cilab git:(success) ✗ tox -c cilab/tox.ini
py36 create: /Users/ben/Zajecia/www-cilab/cilab/.tox/py36
py36 installdeps: -rrequirements.txt
py36 installed: Django==2.0,pytz==2018.4
py36 runtests: PYTHONHASHSEED='950554278'
py36 runtests: commands[0] | /Users/ben/Zajecia/www-cilab/cilab/.tox/py36/bin/python manage.py test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).

----------------------------------------------------------------------
Ran 0 tests in 0.000s

OK
Destroying test database for alias 'default'...
_________________________________________ summary __________________________________________
  py36: commands succeeded
  congratulations :)
```

# Większy przykład

```
✗ tox                
py35 create: /Users/marcin/wow/src/platforma-wyborcza/src/pw/.tox/py35
ERROR: InterpreterNotFound: python3.5
py36 installed: appdirs==1.4.3,astroid==1.5.1,Babel==2.4.0,Django==1.10.4,django-debug-toolbar==1.6,docutils==0.13.1,docxtpl==0.3.5,editdistance==0.3.1,flake8==3.3.0,isort==4.2.5,Jinja2==2.9.6,lazy-object-proxy==1.2.2,lxml==3.7.3,MarkupSafe==1.0,mccabe==0.6.1,packaging==16.8,pep8==1.7.0,psycopg2==2.7.1,pycodestyle==2.3.1,pyflakes==1.5.0,pylint==1.7.0,pylint-django==0.7.2,pylint-plugin-utils==0.2.6,pyparsing==2.2.0,python-docx==0.8.6,pytz==2017.2,six==1.10.0,sqlparse==0.2.3,Unidecode==0.4.20,wrapt==1.10.10,XlsxWriter==0.9.6
py36 runtests: PYTHONHASHSEED='749134184'
py36 runtests: commands[0] | .../.tox/py36/bin/python manage.py test 
Creating test database for alias 'default'...
Creating test database for alias 'audit'...
....................................................................................................................................................................................................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 452 tests in 224.237s

OK
Destroying test database for alias 'default'...
Destroying test database for alias 'audit'...
_________________________________________________ summary __________________________________________________
ERROR:   py35: InterpreterNotFound: python3.5
  py36: commands succeeded
```

# coverage.py

```
(cilab) ➜  www-cilab git:(master) ✗ pip install coverage
Collecting coverage
  Downloading coverage-4.3.4-cp36-cp36m-macosx_10_10_x86_64.whl (168kB)
    100% |████████████████████████████████| 174kB 52kB/s 
Installing collected packages: coverage
Successfully installed coverage-4.3.4
(cilab) ➜  www-cilab git:(master) ✗ coverage run --source=cilab cilab/manage.py test 
Creating test database for alias 'default'...

----------------------------------------------------------------------
Ran 0 tests in 0.000s

OK
Destroying test database for alias 'default'...
(cilab) ➜  www-cilab git:(master) ✗ coverage report
Name                                 Stmts   Miss  Cover
--------------------------------------------------------
cilab/cilab/__init__.py                  0      0   100%
cilab/cilab/settings.py                 18      0   100%
cilab/cilab/urls.py                      3      3     0%
cilab/cilab/wsgi.py                      4      4     0%
cilab/manage.py                         13      6    54%
cilab/polls/__init__.py                  0      0   100%
cilab/polls/admin.py                     1      1     0%
cilab/polls/apps.py                      3      3     0%
cilab/polls/migrations/__init__.py       0      0   100%
cilab/polls/models.py                    1      1     0%
cilab/polls/tests.py                     1      1     0%
cilab/polls/views.py                     1      1     0%
--------------------------------------------------------
TOTAL                                   45     20    56%
```

# Docker

Docker jest systemem zarządzania kontenerami

Kontener jest izolowanym środowiskiem (niejako miniaturą systemu operacyjnego)

Pozwala m.in na powtarzalne testy i instalacje

W naszym scenariuszu wykorzystamy go w ramach Ciągłej Integracji

Tworzenie i uruchamianie kontenera jest opisane przez `Dockerfile`

Nie jest zainstalowany na students, można użyć <https://labs.play-with-docker.com/> ale nie jest to dziś niezbędne.

# Dockerfile

```
FROM python:3.6
WORKDIR ./cilab
ADD . /cilab
RUN pip install -U tox
CMD tox -c cilab/tox.ini
```

# docker build

```
(cilab) ➜  www-cilab git:(master) ✗ docker build -t cilab .
Sending build context to Docker daemon  45.9 MB
Step 1/5 : FROM python:3.6
 ---> 787e9f4da78e
Step 2/5 : RUN pip install -U tox
 ---> Running in 6174859c9320
Collecting tox
  Downloading tox-2.7.0-py2.py3-none-any.whl (49kB)
Collecting virtualenv>=1.11.2; python_version != "3.2" (from tox)
  Downloading virtualenv-15.1.0-py2.py3-none-any.whl (1.8MB)
Collecting pluggy<1.0,>=0.3.0 (from tox)
  Downloading pluggy-0.4.0-py2.py3-none-any.whl
Collecting py>=1.4.17 (from tox)
  Downloading py-1.4.33-py2.py3-none-any.whl (83kB)
Installing collected packages: virtualenv, pluggy, py, tox
Successfully installed pluggy-0.4.0 py-1.4.33 tox-2.7.0 virtualenv-15.1.0
 ---> 29430ba91b06
Removing intermediate container 6174859c9320
Step 3/5 : WORKDIR ./cilab
 ---> 97f44e5665e9
Removing intermediate container 56e477732bf5
Step 4/5 : ADD . /cilab
 ---> d3d3cd303047
Removing intermediate container 665a83b6f885
Step 5/5 : CMD tox -c cilab/tox.ini
 ---> Running in e481239bf6d9
 ---> 5a88a4f3949f
Removing intermediate container e481239bf6d9
Successfully built 5a88a4f3949f
```

# docker run

```
cilab) ➜  www-cilab git:(master) ✗ docker run cilab
py36 recreate: /cilab/cilab/.tox/py36
py36 installdeps: -rrequirements.txt

py36 installed: appdirs==1.4.3,Django==1.10,packaging==16.8,pyparsing==2.2.0,six==1.10.0
py36 runtests: PYTHONHASHSEED='4064046258'
py36 runtests: commands[0] | /cilab/cilab/.tox/py36/bin/python manage.py test

----------------------------------------------------------------------
Ran 0 tests in 0.000s

OK
Creating test database for alias 'default'...
Destroying test database for alias 'default'...
___________________________________ summary ____________________________________
  py36: commands succeeded
  congratulations :)
```

# Pośredni kontener

W praktyce lepiej zbudować sobie pośredni kontener:

```
FROM python:3.6
RUN pip install --upgrade pip
RUN pip install -U tox
RUN pip install django==2.0
```

```
docker build -f tox-Dockerfile -t tox .
docker tag tox mbenke/tox
```

```
FROM mbenke/tox
WORKDIR ./cilab
ADD . /cilab
CMD tox -c cilab/tox.ini
```

# Bitbucket pipelines

* Narzędzie Ciągłej Integracji (CI)
* Przy każdym push do repo uruchamiane są testy

Konfiguracja przez

```
# This is a sample build configuration for Python.
# Check our guides at https://confluence.atlassian.com/x/x4UWN for more examples.
# Only use spaces to indent your .yml configuration.
# -----
# You can specify a custom docker image from Docker Hub as your build environment.
image: python:3.6

pipelines:
  default:
    - step:
        script: # Modify the commands below to build your repository.
          - pip install -U tox
          - pip --version
          - tox --version
          - pip install Django==1.10
          - python cilab/manage.py test
          - tox -c cilab/tox.ini
```

# Własny obraz

```
image: mbenke/tox

pipelines:
  default:
    - step:
        script: 
          - python cilab/manage.py test
          - tox -c cilab/tox.ini
```
