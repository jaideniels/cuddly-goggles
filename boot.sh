#!/bin/sh
source venv/bin/activate

echo "hi jay!"

exec gunicorn --reload -b :5000 --access-logfile - --error-logfile - stacks:app
