#!/bin/bash
set -e

echo "Installing dependencies..."
python3 -m pip install -r requirements.txt --break-system-packages

echo "Running migrations..."
python3 manage.py migrate

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Done!"
