---
title: Aplikacje WWW
author: Marcin Benke
date: 8 marca 2018
---

# CSS = Cascading Style Sheets
* `<style>... </style>`
* `<link href="foo.css" type="text/css" rel="stylesheet">`


```css
body {
    background-color:   #e2e699;
    font:               120% arial, verdana, helvetica, lucida, sans-serif;
}

#content{ background-color: #f7faee; } /* <foo id="content*/

.centered { text-align: center; } /* <foo class="centered" */
```

## Polecane materiały
* <https://internetingishard.com/html-and-css/>
* <https://www.w3schools.com/css/default.asp>
* [http://www.cssbasics.com/css-syntax/](http://www.cssbasics.com/css-syntax/)
* <https://developer.mozilla.org/en-US/docs/Learn/CSS>

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

* Style w `<style>` przesłaniają te w `styles.css`
* Elementy dziedziczą styl po przodkach
* Bardziej specyficzne własności przesłaniają ogólniejsze

Prosty przykład: <https://jsfiddle.net/dh5uv14t/17/>

# Bardziej zaawansowane selektory

``` css
#leftnav a { color: green; } /* a, potomek #leftnav */
#content h2 { color: red; } /* h2, potomek #content */
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

``` css
/* li, dziecko ul class="menu" */
ul.menu>li { display: inline; margin-left: 6px; margin-right: 6px;}
```

Bardziej rozbudowany przykład: <https://jsfiddle.net/11fw2y6x/31/>

# Inspector

* W Firefox Tools->Web Developer->Inspector
* Narzędzia->Dla twórców witryn->Inspektor
* `Shift+Ctrl+C`
* W Chrome Narzędzia dla programistów (`Ctrl+Shift+I`)

Obejrzyjmy <https://developer.mozilla.org/en-US/docs/Learn/CSS>

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

# Display

* `block`
* `inline`
* `none`

<https://www.w3schools.com/css/css_display_visibility.asp>

# Jednostki miary

Najważniejsze:

* `px` - pixel
* `em` - szerokość czcionki
* `%` - względem domyślnej (np `font-size: 120%`)

[w3schools.com/cssref/css_units.asp](http://www.w3schools.com/cssref/css_units.asp)

[7 CSS Units You Might Not Know About](http://webdesign.tutsplus.com/articles/7-css-units-you-might-not-know-about--cms-22573)

# Responsive Web Design

* [RWD Intro](https://www.w3schools.com/css/css_rwd_intro.asp)
* [Viewport](https://www.w3schools.com/css/css_rwd_viewport.asp)
* [Media queries](https://www.w3schools.com/css/css3_mediaqueries.asp)

``` css
@media screen and (min-width: 480px) {
    body {
        background-color: lightgreen;
    }
}
```