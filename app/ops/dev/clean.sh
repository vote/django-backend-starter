#!/bin/bash

autoflake --remove-unused-variables --remove-all-unused-imports --ignore-init-module-imports --in-place --recursive --exclude /*/migrations/* /app/

isort -m 3 -w 88 --skip migrations /app/

black --exclude /*/migrations/* /app/
