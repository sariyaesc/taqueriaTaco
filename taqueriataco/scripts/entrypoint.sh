#!/bin/sh
set -e

# Install any local editable deps (not used here) and run migrations
python manage.py migrate --noinput || true
python manage.py runserver 0.0.0.0:8000
