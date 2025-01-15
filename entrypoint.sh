#!/bin/sh

set -e

echo "Applying migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Loading initial data..."
python manage.py loaddata post.json
python manage.py loaddata user.json

echo "Starting Django server..."
exec "$@"
