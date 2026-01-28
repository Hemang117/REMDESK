#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run migrations (safe to run on every deploy)
python3.9 manage.py migrate

# Collect static files
python3.9 manage.py collectstatic --noinput
