#!/bin/bash -x

export PYTHONUNBUFFERED=1
pip3 install -r requirements.txt
python3 manage.py migrate --no-input
python3 manage.py run_celery_dev &
python3 manage.py runserver 0.0.0.0:8000
