#!/bin/bash

echo "Collecting static files:"
RUN python manage.py collectstatic --noinput

echo "Running migrations:"
python manage.py makemigrations
python manage.py migrate

echo ""
echo "Load data:"
python manage.py loaddata ./*/fixtures/*.json
