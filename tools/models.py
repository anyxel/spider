from django.db import models


class Tools(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=10)
    folder = models.CharField(max_length=100)
    run = models.CharField(max_length=100)
    script = models.CharField(max_length=100)
    url = models.TextField()
