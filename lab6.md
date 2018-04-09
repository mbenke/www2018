---
title: Aplikacje WWW
author: Marcin Benke
date: 6 kwietnia 2018
---

# Plan

* Należy zainstalować gunicorna jako alternatywny dla developerskiego sposób serwowania stron https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/gunicorn/
* Należy zgrać statici do jednego miejsca
* Należy umożliwić upload pliku (np. protokół obwodowy w postaci pdf) dla zalogowanych użytkowników
* Należy zrobić middleware, które będzie logowało wszystkie żądania, które nie mają w parametrach foo=secret
* Należy napisać test jednostkowy sprawdzający sumowanie całkowitej liczby głosów

# Gunicorn

[docs.gunicorn.org](http://docs.gunicorn.org)

> Gunicorn ‘Green Unicorn’ is a Python WSGI HTTP Server for UNIX.
> It’s a pre-fork worker model ported from Ruby’s Unicorn project. 

Instalacja:
```
(wow) ➜  pw git:(master) pip install gunicorn
Collecting gunicorn
  Downloading gunicorn-19.7.1-py2.py3-none-any.whl (111kB)
    100% |████████████████████████████████| 112kB 1.6MB/s 
Installing collected packages: gunicorn
Successfully installed gunicorn-19.7.1
```

Uruchomienie

```
(wow) ➜  pw git:(master) ls -l pw/wsgi.py
-rw-r--r--  1 marcin  staff  379  5 sty 12:41 pw/wsgi.py

(wow) ➜  pw git:(master) gunicorn pw.wsgi -b 0.0.0.0:8000 --workers=2
[2017-04-05 16:50:49 +0200] [59259] [INFO] Starting gunicorn 19.7.1
[2017-04-05 16:50:49 +0200] [59259] [INFO] Listening at: http://0.0.0.0:8000 (59259)
[2017-04-05 16:50:49 +0200] [59259] [INFO] Using worker: sync
[2017-04-05 16:50:49 +0200] [59262] [INFO] Booting worker with pid: 59262
[2017-04-05 16:50:49 +0200] [59263] [INFO] Booting worker with pid: 59263
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


# Upload

* [docs.djangoproject.com/en/1.10/topics/http/file-uploads](https://docs.djangoproject.com/en/1.10/topics/http/file-uploads)
* [docs.djangoproject.com/en/1.10/ref/settings/#file-upload-settings](https://docs.djangoproject.com/en/1.10/ref/settings/#file-upload-settings)

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

# Middleware

Django 1.9 (od 1.10 nowy system, ale stary też działa)

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

[docs.djangoproject.com/en/1.10/topics/http/middleware/#writing-your-own-middleware](https://docs.djangoproject.com/en/1.10/topics/http/middleware/#writing-your-own-middleware)

# Nowe middleware (od 1.10)

`settings.py`:
```
MIDDLEWARE = (
myapp.middleware.AuditMiddleware,
...
```

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