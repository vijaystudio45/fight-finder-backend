#!/bin/sh

python manage.py migrate

gunicorn contract_project.wsgi:application --bind 0.0.0.0:8000  --timeout 600
