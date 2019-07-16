#!/bin/bash

# /code/deploy/scripts/
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# /code/
ROOT_DIR=$(dirname "$(dirname "$BASE_DIR")")

export PYTHONUNBUFFERED=1
. /venv/bin/activate

echo '>> [Running] Uwsgi server'
celery -A config worker -l info --concurrency=2
