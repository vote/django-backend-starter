#!/bin/bash

npm run build

export SECRET_KEY=abcd
pipenv run /app/manage.py collectstatic --noinput

# Save space by deleting unnecessary content
rm -rf /root/.cache
rm -rf /app/node_modules/
rm -rf /app/assets/
