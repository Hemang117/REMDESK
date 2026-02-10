#!/bin/bash
set -e

echo "Installing dependencies..."
python3 -m pip install -r requirements.txt --break-system-packages

# Migrations should be run manually or via a separate release command
# python3 manage.py migrate

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Done!"
