#!/usr/bin/env bash
workon mrsix
../manage.py collectstatic
uwsgi --reload /tmp/mrsix.pid
