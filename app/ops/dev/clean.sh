#!/bin/bash

autoflake --remove-unused-variables --remove-all-unused-imports --ignore-init-module-imports --in-place --recursive --exclude /*/migrations/* /app/

isort -m 3 -tc -w 88 --skip migrations --recursive /app/

black --exclude /*/migrations/* /app/
