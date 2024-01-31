# Generated by Django 5.0.1 on 2024-01-31 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('lang', models.CharField(max_length=10)),
                ('directory', models.CharField(max_length=100)),
                ('run', models.CharField(max_length=100)),
                ('script', models.CharField(max_length=100)),
                ('category_slug', models.SlugField(max_length=20)),
                ('git_repo', models.TextField()),
            ],
            options={
                'verbose_name': 'Tool',
                'verbose_name_plural': 'Tools',
            },
        ),
    ]
