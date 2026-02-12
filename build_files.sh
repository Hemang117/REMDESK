#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt --no-cache-dir --break-system-packages || \
pip install -r requirements.txt --no-cache-dir || \
python3 -m pip install -r requirements.txt --no-cache-dir

echo "Running database migrations..."
python3 manage.py migrate --noinput

echo "Collecting static files..."
mkdir -p staticfiles
python3 manage.py collectstatic --noinput

echo "Done!"
