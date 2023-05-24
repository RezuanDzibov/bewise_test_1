#!/bin/bash

bash -c "cd src && alembic upgrade head"
exec "$@"