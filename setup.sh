#!/bin/bash

echo "Running migrations:"
python manage.py makemigrations
python manage.py migrate

echo ""
echo "Load data:"
python manage.py loaddata ./*/fixtures/*.json
