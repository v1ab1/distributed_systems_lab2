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

# Сначала создаем пользователя program, если его нет
psql -h postgres -U "$SUPERUSER" -d postgres <<EOSQL || true
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
psql -h postgres -U "$SUPERUSER" -d postgres <<EOSQL
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
