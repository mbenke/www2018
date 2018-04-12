---
title: Aplikacje WWW
author: Marcin Benke
date: 6 kwietnia 2018
---

# Plan

* Należy zainstalować gunicorna jako alternatywny dla developerskiego sposób serwowania stron https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/gunicorn/
* Należy zgrać statici do jednego miejsca
* Należy zrobić middleware, które będzie logowało wszystkie żądania, które nie mają w parametrach foo=secret
* Należy napisać test jednostkowy sprawdzający sumowanie całkowitej liczby głosów
* Użyć fixtures do ładowania danych di bazy i w testach

# Gunicorn

[docs.gunicorn.org](http://docs.gunicorn.org)

> Gunicorn ‘Green Unicorn’ is a Python WSGI HTTP Server for UNIX.
> It’s a pre-fork worker model ported from Ruby’s Unicorn project. 

Instalacja:
```
(django2) ➜  mysite git:(master) pip install gunicorn
Collecting gunicorn
  Using cached gunicorn-19.7.1-py2.py3-none-any.whl
Installing collected packages: gunicorn
Successfully installed gunicorn-19.7.1
```

Uruchomienie

```
(django2) ➜  mysite git:(master) ls -l mysite/wsgi.py
-rw-r--r--  1 ben  staff  389 26 lut 16:44 mysite/wsgi.py
(django2) ➜  mysite git:(master) gunicorn mysite.wsgi -b 0.0.0.0:8000 --workers=2
[2018-04-10 14:03:19 +0200] [79399] [INFO] Starting gunicorn 19.7.1
[2018-04-10 14:03:19 +0200] [79399] [INFO] Listening at: http://0.0.0.0:8000 (79399)
[2018-04-10 14:03:19 +0200] [79399] [INFO] Using worker: sync
[2018-04-10 14:03:19 +0200] [79404] [INFO] Booting worker with pid: 79404
[2018-04-10 14:03:19 +0200] [79407] [INFO] Booting worker with pid: 79407
```

# Static

```
STATIC_ROOT = '/srv/app/static/'
STATIC_URL = '/static/'
```

```
./manage.py collectstatic
cp -a /srv/app/static/* /var/www/static  # mapowane na URL /static/
```

Może być na innym serwerze (np nginx reverse proxy), wtedy rsync, Ansible, ...



# Nowe middleware (od 1.10)

```
class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
```

```
class AuditMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            if not settings.AUDIT_REQUESTS:
                return response
            if not settings.AUDIT_GET_REQUESTS and request.method == 'GET':
                return response

            if request.user and request.user.id:
                r = Request()
                r.fill_from_request(request, response)
                r.save()

        except AttributeError:
            # in some corner cases request.user may not be present
            # also safeguard against missing settings
            pass

        return response

```

`settings.py`:
```
MIDDLEWARE = (
myapp.middleware.AuditMiddleware,
...
```

<https://docs.djangoproject.com/en/2.0/topics/http/middleware/>

# Stare Middleware

Django do wersji 1.9 

[docs.djangoproject.com/en/1.9/topics/http/middleware/#writing-your-own-middleware](https://docs.djangoproject.com/en/1.9/topics/http/middleware/#writing-your-own-middleware)

`settings.py`:
```
MIDDLEWARE_CLASSES = (
myapp.middleware.AuditMiddleware,
...
```

`myapp/middleware.py`:
```
class AuditMiddleware(object):
    def process_response(self, request, response):
        try:
            if not settings.AUDIT_REQUESTS:
                return response
            if not settings.AUDIT_GET_REQUESTS and request.method == 'GET':
                return response

            if request.user and request.user.id:
                r = Request()
                r.fill_from_request(request, response)
                r.save()

        except AttributeError:
            # in some corner cases request.user may not be present
            # also safeguard against missing settings
            pass

        return response
```


# Testy

```
from django.test import TestCase
from myapp.models import Animal

class AnimalTestCase(TestCase):
    def setUp(self):
        Animal.objects.create(name="lion", sound="roar")
        Animal.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')
```

```
(django2) $ ./manage.py test animals          
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.002s

OK
Destroying test database for alias 'default'...
```

# Liczenie głosów

```
class ResultsTest(CommunityReferendumTestSetup, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData() # CommunityReferendumTestSetup

        protocol_1_json = {
            "issues": [{
                "description": "Pytanie", "id": cls.question.id,
                "invalid_votes": 2, "valid_votes": 5, "valid_votes_no": 3, "valid_votes_yes": 2
            }],
        }
        cls.protocol_1 = PollstationProtocol(pollstation=cls.pollstation_1,
            status=PollstationProtocol.ACCEPTED,
            hash_value='hash1111', voting_start=cls.voting_start, voting_end_hour=time(21, 0),
            headquaters="head", json_file=protocol_1_json)
        cls.protocol_1.save()
# ...
```

```
    def test_simple_ref_results(self):
        cls = self.__class__
        self.call_view()

        results = LocalReferendumResult.objects.filter(
            question=cls.question, territorial_unit=cls.comm)
        if results:
            results = results[0]
            self.assertEqual(results.valid_votes, 16)
            self.assertEqual(results.valid_votes_no, 6)
            self.assertEqual(results.valid_votes_yes, 10)
            self.assertEqual(results.passed, True)

    def call_view(self):
        response = self.client.get(
	    resolve_url('ref_close', ResultsTest.ref_round.id,
                        ResultsTest.question.id, self.comm.id), follow=True)
        self.assertRedirects(response, resolve_url('ref_results', ResultsTest.ref_round.id))

        self.context = response.context
```

# Fixtures

Metoda serializacji danych modeli

```
$ ./manage.py dumpdata animals | tee animals/fixtures/animals.json
[{"model": "animals.animal", "pk": 1, "fields": {"name": "lion", "sound": "roar"}},
{"model": "animals.animal", "pk": 2, "fields": {"name": "cat", "sound": "meow"}}]

$ sqlite3 db.sqlite3 
sqlite> select * from animals_animal;
1|lion|roar
2|cat|meow
sqlite> delete from animals_animal;

$ ./manage.py loaddata animals/fixtures/animals.json
Installed 2 object(s) from 1 fixture(s)
$ sqlite3 db.sqlite3                                
sqlite> select * from animals_animal;
1|lion|roar
2|cat|meow
```

# Fixtures w testach

``` python
class AnimalFixtureTestCase(TestCase):
    fixtures = ['animals']

    def setUp(self):
        pass

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')
```

# Koniec

# Bonus - Upload

* <https://docs.djangoproject.com/en/2.0/topics/http/file-uploads/>
* <https://docs.djangoproject.com/en/2.0/ref/settings/#file-uploads>

`settings.py`:
```
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

Form:

```
class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. XX megabytes'
    )
```

View:
```
def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('myapp.views.list'))
    else:
        form = DocumentForm() # An empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'myapp/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
```

`MEDIA_ROOT` nie jest domyślnie udostępniony, musimy to jakoś oprogramować.

Na etapie programowania można

```
urlpatterns = patterns('',
    (r'^', include('myapp.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

w produkcji to potencjalna luka bezpieczeństwa.

