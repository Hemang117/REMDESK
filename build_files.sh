#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt --no-cache-dir --break-system-packages || \
pip install -r requirements.txt --no-cache-dir || \
python3 -m pip install -r requirements.txt --no-cache-dir

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Done!"
