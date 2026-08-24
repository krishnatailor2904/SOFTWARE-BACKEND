#!/usr/bin/env bash
# Render is script - build ke time automatically chalti hai
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate
