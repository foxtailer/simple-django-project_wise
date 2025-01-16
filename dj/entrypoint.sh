#!/bin/sh

set -e  # Exit immediately if a command exits with a non-zero status

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to start..."
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 1
done
echo "PostgreSQL is up - continuing..."

# Apply migrations
echo "Applying migrations..."
python manage.py makemigrations
python manage.py migrate

# Load initial data
echo "Loading initial data..."
python manage.py loaddata user.json
python manage.py loaddata post.json

# Start Django server
echo "Starting Django server..."
exec "$@"
