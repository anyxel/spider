#!/bin/bash

echo "Collecting static files..."
RUN python manage.py collectstatic --noinput
echo "Collected successfully!"
echo

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate
echo "Migration done!"
echo

echo
echo "Load data..."
python manage.py loaddata ./tools/fixtures/category.json
python manage.py loaddata ./tools/fixtures/tools/*.json
echo "Loaded successfully!"

echo
echo "Create external tools directory..."
directory="et"
if [ ! -d "$directory" ]; then
    echo "Creating directory: $directory"
    mkdir -p "$directory"
else
    echo "Directory already exists: $directory"
fi
