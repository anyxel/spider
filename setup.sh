#!/bin/bash

echo "Collecting static files:"
RUN python manage.py collectstatic --noinput

echo "Running migrations:"
python manage.py makemigrations
python manage.py migrate

echo ""
echo "Load data:"
python manage.py loaddata ./*/fixtures/*.json

echo ""
echo "Create external tools directory:"
directory="et"
if [ ! -d "$directory" ]; then
    echo "Creating directory: $directory"
    mkdir -p "$directory"
else
    echo "Directory already exists: $directory"
fi
