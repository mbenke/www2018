---
title: Aplikacje WWW
author: Marcin Benke
date: 8 marca 2018
---

# CSS = Cascading Style Sheets
* `<style>... </style>`
* `<link href="foo.css" type="text/css" rel="stylesheet">`
* [http://www.cssbasics.com/css-syntax/](http://www.cssbasics.com/css-syntax/)

```css
body {
    background-color:   #e2e699;
    font:               120% arial, verdana, helvetica, lucida, sans-serif;
}

#content{ background-color: #f7faee; } /* <foo id="content*/

.centered { text-align: center; } /* <foo class="centered" */
```

# Cascading

``` html
<head>
  <meta charset='UTF-8'/>
  <title>Dummy</title>
  <link rel='stylesheet' href='styles.css'/>
  <style>
    body {
      color: #0000FF;    /* Blue */
    }
  </style>
</head>
```

Style w `<style>` przesłaniają te w `styles.css`

# Bardziej zaawansowane selektory

``` css
#leftnav a { color: green; }
#content h2 { color: red; }
```

``` html
<body>
  <div id="leftnav">        <!-- body #leftnav -->
    <a href="#">Galeria</a> <!-- body #leftnav a -->
  </div>
  <div id="content">	
    <h2>Tytuł </h2>         <!-- #content h2 -->
  </div>
</body>	
```

# Firefox Inspector

* Tools->Web Developer->Inspector
* Narzędzia->Dla twórców witryn->Inspektor
* `Shift+Ctrl+C`
* Obejrzyjmy [http://benke.org/example1](http://benke.org/example1)

# Box model

[w3schools.com/css/css_boxmodel.asp](http://w3schools.com/css/css_boxmodel.asp)

``` css
#content{
margin-left: 200px;
background-color: #f7faee;
border-left: 1px solid gray;
padding: 1em;
max-width: 36em;
text-align: left;
}
```

# Jednostki miary

Najważniejsze:

* `px` - pixel
* `em` - szerokość czcionki
* `%` - względem domyślnej (np `font-size: 120%`)

[w3schools.com/cssref/css_units.asp](http://www.w3schools.com/cssref/css_units.asp)

[7 CSS Units You Might Not Know About](http://webdesign.tutsplus.com/articles/7-css-units-you-might-not-know-about--cms-22573)
