#!/bin/bash
set -e

# Подключаемся к PostgreSQL и создаем базы данных, если они не существуют
PGPASSWORD="${POSTGRES_PASSWORD:-test}" psql -h postgres -U "${POSTGRES_USER:-program}" -d postgres <<EOSQL
-- Создаем пользователя, если не существует
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'program') THEN
        CREATE ROLE program WITH PASSWORD 'test';
        ALTER ROLE program WITH LOGIN;
    END IF;
END
\$\$;

-- Создаем базы данных, если они не существуют
SELECT 'CREATE DATABASE tickets'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'tickets')\gexec

SELECT 'CREATE DATABASE flights'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'flights')\gexec

SELECT 'CREATE DATABASE privileges'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'privileges')\gexec

-- Выдаем права
GRANT ALL PRIVILEGES ON DATABASE tickets TO program;
GRANT ALL PRIVILEGES ON DATABASE flights TO program;
GRANT ALL PRIVILEGES ON DATABASE privileges TO program;
EOSQL
