import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lab4.settings")
django.setup()

from a import models

print(models.Kandydat.objects.get(pk=1))

