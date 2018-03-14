---
title: Aplikacje WWW
subtitle: szablony Jinja
author: Marcin Benke
date: 8 marca 2018
---

# virtualenv

```
virtualenv foo && cd foo
source bin/activate
pip install Jinja2
# work
deactivate
```

# Jinja

System szablonów bardazo podobny do tego w Django

```
>>> from jinja2 import Template
>>> template = Template('Hello {{ name }}!')
>>> template.render(name='world')
'Hello world!'
```

# Szablon w pliku

```
<html>
  <head>
    <title>Hello {{ name }}</title>
  <body>
    <h1>Hello, {{ name }}</h1>
    <p>My favorite numbers:
      {% for n in range(1,10) %}{{n}} {% endfor %}</p>
  </body>
</html>
```

# Szablony z pliku

```
from jinja2 import Template, FileSystemLoader, Environment, select_autoescape

loader = FileSystemLoader('./templates')
env = Environment(loader=loader, autoescape=select_autoescape(['html', 'xml']))

hello = env.get_template('hello.html')
print(hello.render(name='<foo&bar>'))
```

# Kontekst

Doe metody Template.render można przekazać listę nazwanych argumentów albo słownik:

```
from jinja2 import Template, FileSystemLoader, Environment, select_autoescape

loader = FileSystemLoader('./templates')
env = Environment(loader=loader, autoescape=select_autoescape(['html', 'xml']))

hello = env.get_template('hello.html')
print(hello.render({'name': '<foo&bar>'}))
```

# Dziedziczenie szablonów

Szablon bazowy

`base.html`

``` html
<head>
<link href="style.css" rel="stylesheet">
{% block css %} {% endblock %}
</head>
<body>
    <div class="container">
      <h2>This is part of my base template</h2>
      <br>
      {% block content %}{% endblock %}
      <br>
      <h2>This is part of my base template</h2>
    </div>
</body>
```

# Szablon potomny


```
{% extends "base.html" %}
{% block css %}
{{ super() }}
<style> h2 { color: red } </style>
{% endblock %}
{% block content %}
<h3> This is part of my child template</h3>
{% endblock %}
```

# Efekt

```
<head>
<link href="style.css" rel="stylesheet">
 
<style> h2 { color: red } </style>
</head>
<body>
    <div class="container">
      <h2>This is part of my base template</h2>
      <br>
      
<h3> This is part of my child template</h3>

      <br>
      <h2>This is part of my base template</h2>
    </div>
</body>
```

# Więcej

<http://jinja.readthedocs.io/en/stable/>

<https://realpython.com/blog/python/primer-on-jinja-templating/>

# Ćwiczenie

* Na podstawie swojej strony z wynikami wyborów stwórz szablon Jinja
* Użyj konstrukcji `%for` tam gdzie potrzeba (np. w tabelach)
* Napisz program wypełniający szablon danymi