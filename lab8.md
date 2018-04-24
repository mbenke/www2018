# Zaliczeniowe Zadanie Laboratoryjne 3

nie ma jeszcze ale można przygotować się na scenariusz podobny do zesłorocznego:

* Należy zmodernizować wyniki zadania drugiego przerabiając serwer na RESTowy.
* Klient powinien być statycznym HTML + CSS + JS (może być serwowany przez django)
* Po załadowaniu HTML, klient powinien rozpocząć pobieranie danych z serwera. Do momentu pobrania danych klient powinien wyświetlać informacje pobrane w poprzedniej sesji przechowywane po stronie przeglądarki
* Klient powinien komunikować się z serwisem RESTowym
* Komunikacja powinna odbywać się przy wykorzystaniu JSONa
* Należy obsługiwać błędy po obu stronach
* Można wykorzystać dodatkową bibliotekę JS



# Laboratorium 8

* Przygotowujemy serwer, który potrafi udostępnić wyniki wyborów w JSON
* Napiszemy kod w JavaScript, który za pomocą XMLHttpRequest pobiera wyniki, rozparsowuje je i wyświetla na stronie
* Uczymy się używać konsoli javascript

# JSONResponse

Używamy Django jak dotąd, tylko widok zamiast HTML serwuje JSON


```
from django.http import JsonResponse

def info(request):
    d = { 'answer' : 42,
      	  'message' : 'We apologise for the inconvenience'
	}
    return JsonResponse(d)
```

# httpbin.org

Np.

```
$ curl http://httpbin.org/ip
{
  "origin": "193.0.96.15"
}
```

```
$ curl http://httpbin.org/get\?key\=value 
{
  "args": {
    "key": "value"
  }, 
  "headers": {
    "Accept": "*/*", 
    "Connection": "close", 
    "Host": "httpbin.org", 
    "User-Agent": "curl/7.43.0"
  }, 
  "origin": "193.0.96.15", 
  "url": "http://httpbin.org/get?key=value"
}

```

# Modyfikacja dokumentu przez jQuery

```
<!doctype html>
<meta charset="utf-8">
<html>
<body>
<h1>h1</h1>
</body>
<script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.2.1.min.js"></script>

<script>
$(document).ready(function() {
$("body h1:first").text('welcome')
})
</script>
</html>
``` 

[learn.jquery.com](https://learn.jquery.com/)

# Konsola JavaScript

```
$("h1:first").text("hello")
```

```
$.ajax({
  url: "http://httpbin.org/ip",
  success: function( result ) {
   console.log( result);
  }
});
```

[learn.jquery.com/ajax/](https://learn.jquery.com/ajax/)

# Lepsza identyfikacja

```
<!doctype html>
<meta charset="utf-8">
<html>
<body>
<h1 id="h1-1">h1</h1>
</body>
<script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
<p id="ip"></p>
<script>
$(document).ready(function() {
$("#h1-1").text('welcome')
})
</script>
</html>
```

# Jeszcze AJAX
```
$.ajax({ url: "http://httpbin.org/ip" })
  .done(function(json){ 
           $("#ip").text(json.origin);
	 })
   .fail(function(xhr, status, error) {
	     alert( "Error!" );
	     console.log( "Error: " + errorThrown );
	     console.log( "Status: " + status );
	     console.dir( xhr );
  	 })
   .always(function( xhr, status ) { alert( "Done." ); });
```

# Wskazywanie elementów

Zamiast `document.getElementById('id')`

wystarczy `$(selektor CSS)` np.

```
$('#table1)

$('.inactive-user').hide()
```

# Tworzenie elementów

```
h = $('<h1>Tytuł</h1>');
$('#content').append(h);
$('#content').prepend(h);
```

# Zmiana zawartości elementu

```
$(document).ready(function() {
$("body h1:first").text('welcome')
})
```


```
$('#title').html('<b>Tytuł</b>')
```


# Pokazywanie/ukrywanie wierszy

```
// Requires a button with id=btn-toggle-inactive
// toggles visibility of elements with class inactive-user
// assumes visibility starts at hidden
$(document).ready(function() {
  $('.inactive-user').hide();
  window.inactiveHidden = true;
  $('#btn-toggle-inactive').click(function(event){
    var btn =  $('#btn-toggle-inactive');
    if(window.inactiveHidden) {
      btn.text('Ukryj nieaktywnych użytkowników');
      window.inactiveHidden = false;
      $('.inactive-user').show();
    } else {
      btn.text('Pokaż nieaktywnych użytkowników');
      window.inactiveHidden = true;
      $('.inactive-user').hide();
    }
  })
})
```

# Zaznaczenie wszystkich checkboxów

Mamy ma stronie ileś checkboxów. Chcemy dodać jeszcze jeden, który
będzie zaznaczał/odznaczał wszystkie

```
<input type="checkbox" id="all_accept">

<script>    
  $("#all_accept").change(function(event){
  var check = event.target.checked;
  $('#protocols .accept').prop('checked',check)});
 </script>
```
