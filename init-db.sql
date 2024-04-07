-- create dbs
CREATE DATABASE api_db;
CREATE DATABASE sonarqube;


-- create user
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_user
        WHERE  usename = 'db_admin') THEN

        CREATE ROLE db_admin LOGIN PASSWORD 'password';
    END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE api_db TO db_admin;
GRANT ALL PRIVILEGES ON DATABASE sonarqube TO db_admin;