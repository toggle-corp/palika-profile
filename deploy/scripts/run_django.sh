#!/bin/bash -x

# /code/deploy/scripts/
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# /code/
ROOT_DIR=$(dirname "$(dirname "$BASE_DIR")")

export PYTHONUNBUFFERED=1

echo '>> [Running] Django Collectstatic and Migrate'
python3 $ROOT_DIR/manage.py collectstatic --no-input 2>&1
python3 $ROOT_DIR/manage.py migrate --no-input 2>&1

echo '>> [Running] Uwsgi server'
uwsgi --ini $ROOT_DIR/deploy/configs/uwsgi.ini # Start uwsgi server
