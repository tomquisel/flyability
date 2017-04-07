#!/usr/bin/env bash
if [ $USER != 'www-data' ]; then
    echo "Must be run as user www-data"
    exit
fi
export DJANGO_SETTINGS_MODULE='flyability.settings'
export DIR=/var/django/flyability
export PYTHONPATH=.:/var/django/flyability
python -u $DIR/weather/background_runner.py 2>&1 | logger -t flyrunner
