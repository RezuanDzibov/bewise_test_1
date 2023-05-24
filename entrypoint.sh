#!/bin/bash

while ! nc -z db 5432; do
  sleep 0.1
done

bash -c "cd src && alembic upgrade head"
exec "$@"