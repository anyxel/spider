from django.db import models


class Tools(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=10)
    url = models.TextField()
    folder = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    has_dependencies = models.BooleanField(default=False)
