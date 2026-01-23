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

# Используем template1, так как он всегда существует в PostgreSQL
TARGET_DB="template1"
echo "Using template1 database (always exists in PostgreSQL)"

# Проверяем подключение к PostgreSQL
echo "Testing connection to PostgreSQL..."
until psql -h postgres -U "$SUPERUSER" -d "$TARGET_DB" -c "SELECT 1" > /dev/null 2>&1; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done
echo "PostgreSQL is ready"

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

# Проверяем и создаем базу данных tickets
if ! psql -h postgres -U "$SUPERUSER" -d "$TARGET_DB" -tc "SELECT 1 FROM pg_database WHERE datname = 'tickets'" | grep -q 1; then
  echo "Creating database tickets..."
  psql -h postgres -U "$SUPERUSER" -d "$TARGET_DB" -c "CREATE DATABASE tickets"
else
  echo "Database tickets already exists"
fi

# Проверяем и создаем базу данных flights
if ! psql -h postgres -U "$SUPERUSER" -d "$TARGET_DB" -tc "SELECT 1 FROM pg_database WHERE datname = 'flights'" | grep -q 1; then
  echo "Creating database flights..."
  psql -h postgres -U "$SUPERUSER" -d "$TARGET_DB" -c "CREATE DATABASE flights"
else
  echo "Database flights already exists"
fi

# Проверяем и создаем базу данных privileges
if ! psql -h postgres -U "$SUPERUSER" -d "$TARGET_DB" -tc "SELECT 1 FROM pg_database WHERE datname = 'privileges'" | grep -q 1; then
  echo "Creating database privileges..."
  psql -h postgres -U "$SUPERUSER" -d "$TARGET_DB" -c "CREATE DATABASE privileges"
else
  echo "Database privileges already exists"
fi

# Выдаем права
echo "Granting privileges..."
psql -h postgres -U "$SUPERUSER" -d "$TARGET_DB" <<EOSQL
GRANT ALL PRIVILEGES ON DATABASE tickets TO $APP_USER;
GRANT ALL PRIVILEGES ON DATABASE flights TO $APP_USER;
GRANT ALL PRIVILEGES ON DATABASE privileges TO $APP_USER;
EOSQL

echo "Databases created successfully"
