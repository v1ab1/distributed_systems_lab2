-- Создание пользователя
CREATE ROLE program WITH PASSWORD 'test';
ALTER ROLE program WITH LOGIN;

-- Создание баз данных
CREATE DATABASE tickets;
GRANT ALL PRIVILEGES ON DATABASE tickets TO program;

CREATE DATABASE flights;
GRANT ALL PRIVILEGES ON DATABASE flights TO program;

CREATE DATABASE privileges;
GRANT ALL PRIVILEGES ON DATABASE privileges TO program;
