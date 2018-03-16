---
title: Aplikacje WWW
subtitle: Szablony Jinja
author: Marcin Benke
date: 16 marca 2018
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
      {% for n in numbers %}{{n}} {% endfor %}</p>
  </body>
</html>
```

# Szablony z pliku

```
from jinja2 import Template, FileSystemLoader, Environment, select_autoescape

loader = FileSystemLoader('./templates')
env = Environment(loader=loader, autoescape=select_autoescape(['html', 'xml']))

hello = env.get_template('hello.html')
print(hello.render(name='<foo&bar>', numbers=range(1..10)))
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

# Filtry

Wartości zmiennych podstawianych w szablonie mogą być modyfikowane przez filtry, np.

```
{{ user.name|escape }}
{{ user.name|e }}
{{ name|striptags|title }}
```

<http://jinja.readthedocs.io/en/stable/templates.html#builtin-filters>

# Pętle

```
<ul>
{% for user in users %}
  <li>{{ user.username|e }}</li>
{% endfor %}
</ul>
```

```
<dl>
{% for key, value in my_dict.iteritems() %}
    <dt>{{ key|e }}</dt>
    <dd>{{ value|e }}</dd>
{% endfor %}
</dl>
```
ale uwaga - słowniki nie są uporządkowane

<http://jinja.readthedocs.io/en/stable/templates.html#list-of-control-structures>

# If

```
{% if kenny.sick %}
    Kenny is sick.
{% elif kenny.dead %}
    You killed Kenny!  You bastard!!!
{% else %}
    Kenny looks okay --- so far
{% endif %}
```

Ograniczony zbiór wyrażeń <http://jinja.readthedocs.io/en/stable/templates.html#expressions>

# Więcej

<http://jinja.readthedocs.io/en/stable/>

<https://realpython.com/blog/python/primer-on-jinja-templating/>

# Ćwiczenie

* Na podstawie swojej strony z wynikami wyborów stwórz szablon Jinja
* Użyj konstrukcji `%for` tam gdzie potrzeba (np. w tabelach)
* Napisz program wypełniający szablon danymi

# Szablony Django "bez Django"

```
>>> from django.template import Template, Context
>>> from django.template.engine import Engine
>>> e = Engine(dirs=["."])
>>> t = e.from_string("<h1> {{ name }} </h1> "
... )
>>> c = Context({ 'name': 'foo', 'numbers': range(1,10) })
>>> t.render(c)
'<h1> foo </h1> '
>>> t = e.get_template('hello.html')
>>> t.render(c)
```
