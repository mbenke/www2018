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