from django.db import models


class Category(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=20, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Tool(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100, unique=True)
    lang = models.CharField(max_length=10)
    folder = models.CharField(max_length=100)
    run = models.CharField(max_length=100)
    script = models.CharField(max_length=100)
    category_slug = models.SlugField(max_length=20)
    url = models.TextField()

    class Meta:
        verbose_name = "Tool"
        verbose_name_plural = "Tools"
