#!/bin/bash

pipenv run celery -A core.celery_beat beat --scheduler redbeat.RedBeatScheduler --pidfile="/app/celerybeat-checkable.pid"
