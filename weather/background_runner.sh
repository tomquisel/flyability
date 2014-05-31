#!/usr/bin/env bash
export DJANGO_SETTINGS_MODULE='settings'
export DIR=/var/django/flyability
export PYTHONPATH=.:/var/django/flyability
python -u $DIR/weather/background_runner.py 2>&1 | logger -t flyrunner
