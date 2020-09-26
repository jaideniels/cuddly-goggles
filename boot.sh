#!/bin/sh
. venv/bin/activate

exec gunicorn --timeout 3000 --reload -b :8080 --access-logfile - --error-logfile - stacks:app
