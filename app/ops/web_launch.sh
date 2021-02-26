#!/bin/bash

pipenv run gunicorn -b 0.0.0.0:8000 -c /app/core/gunicorn.conf.py core.wsgi_prod
