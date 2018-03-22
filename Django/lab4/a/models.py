from django.db import models

class Kandydat(models.Model):
    imie = models.CharField(max_length=42)
    nazwisko = models.CharField(max_length=42)
    pesel = models.CharField(max_length=11)

