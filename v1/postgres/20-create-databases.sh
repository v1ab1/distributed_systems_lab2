#!/bin/bash
set -e

echo "Starting database creation script..."

# Используем суперпользователя из POSTGRES_USER (это будет program или postgres)
SUPERUSER="${POSTGRES_USER:-program}"
DB_PASSWORD="${POSTGRES_PASSWORD:-test}"
APP_USER="program"

echo "Superuser: $SUPERUSER"
echo "App user: $APP_USER"

# Устанавливаем пароль для подключения
export PGPASSWORD="$DB_PASSWORD"

# Определяем, к какой базе данных подключаться
# Сначала пробуем postgres, если не получается - используем template1
TARGET_DB="postgres"
echo "Testing connection to postgres database..."
if ! psql -h postgres -U "$SUPERUSER" -d postgres -c "SELECT 1" > /dev/null 2>&1; then
  echo "Database 'postgres' not accessible, trying 'template1'..."
  if psql -h postgres -U "$SUPERUSER" -d template1 -c "SELECT 1" > /dev/null 2>&1; then
    TARGET_DB="template1"
    echo "Using template1 database"
  else
    echo "Waiting for PostgreSQL to be ready..."
    until psql -h postgres -U "$SUPERUSER" -d template1 -c "SELECT 1" > /dev/null 2>&1; do
      echo "Waiting for PostgreSQL..."
      sleep 1
    done
    TARGET_DB="template1"
    echo "PostgreSQL is ready, using template1 database"
  fi
else
  echo "Connection to postgres database successful"
fi

# Сначала создаем пользователя program, если его нет
echo "Creating user $APP_USER if not exists..."
psql -h postgres -U "$SUPERUSER" -d "$TARGET_DB" <<EOSQL || true
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$APP_USER') THEN
        CREATE ROLE $APP_USER WITH PASSWORD '$DB_PASSWORD';
        ALTER ROLE $APP_USER WITH LOGIN;
        RAISE NOTICE 'User $APP_USER created';
    ELSE
        RAISE NOTICE 'User $APP_USER already exists';
    END IF;
END
\$\$;
EOSQL

# Создаем базы данных, если они не существуют
echo "Creating databases if they don't exist..."
psql -h postgres -U "$SUPERUSER" -d "$TARGET_DB" <<EOSQL
SELECT 'CREATE DATABASE tickets'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'tickets')\gexec

SELECT 'CREATE DATABASE flights'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'flights')\gexec

SELECT 'CREATE DATABASE privileges'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'privileges')\gexec

-- Выдаем права
GRANT ALL PRIVILEGES ON DATABASE tickets TO $APP_USER;
GRANT ALL PRIVILEGES ON DATABASE flights TO $APP_USER;
GRANT ALL PRIVILEGES ON DATABASE privileges TO $APP_USER;
EOSQL

echo "Databases created successfully"
