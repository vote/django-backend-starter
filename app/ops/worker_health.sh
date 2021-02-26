#!/bin/bash

pipenv run celery inspect ping -A core.celery_app -d celery@$HOSTNAME
