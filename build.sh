#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python Ausencias/manage.py collectstatic --no-input
python Ausencias/manage.py migrate
python manage.py init_users