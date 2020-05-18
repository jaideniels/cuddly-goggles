#!/bin/sh
. venv/bin/activate

exec gunicorn --reload -b :8000 --access-logfile - --error-logfile - stacks:app
