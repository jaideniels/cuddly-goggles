#!/bin/sh
. venv/bin/activate

exec gunicorn --reload -b :8080 --access-logfile - --error-logfile - stacks:app
