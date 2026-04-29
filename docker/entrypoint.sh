#!/usr/bin/env bash
set -euo pipefail

DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-3306}"

if [ "${WAIT_FOR_DB:-1}" = "1" ]; then
  echo "Waiting for MariaDB at ${DB_HOST}:${DB_PORT}..."
  until nc -z "$DB_HOST" "$DB_PORT"; do
    sleep 1
  done
  echo "MariaDB is available"
fi

if [ "${RUN_MIGRATIONS:-1}" = "1" ]; then
  echo "Applying database migrations..."
  flask db upgrade
fi

exec "$@"
