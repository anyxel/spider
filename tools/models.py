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
    lang = models.CharField(max_length=10, null=True, blank=True)
    directory = models.CharField(max_length=100, null=True, blank=True)
    run = models.CharField(max_length=100)
    script = models.CharField(max_length=100)
    category_slug = models.SlugField(max_length=20)
    git_repo = models.TextField(null=True, blank=True)
    website = models.CharField(max_length=191, null=True, blank=True)
    short_desc = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Tool"
        verbose_name_plural = "Tools"
