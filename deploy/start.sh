#!/usr/bin/env bash
workon mrsix
../manage.py collectstatic
uwsgi --ini uwsgi.ini
