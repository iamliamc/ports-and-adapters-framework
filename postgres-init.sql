-- Create development database
CREATE DATABASE dev_db;

-- Connect to dev_db
\c dev_db

-- Create dev_user and grant privileges
CREATE USER dev_user WITH PASSWORD 'dev_password';
GRANT ALL PRIVILEGES ON DATABASE dev_db TO dev_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dev_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO dev_user;

-- Create test database
CREATE DATABASE test_db;

-- Connect to test_db
\c test_db

-- Create test_user and grant privileges
CREATE USER test_user WITH PASSWORD 'test_password';
GRANT ALL PRIVILEGES ON DATABASE test_db TO test_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO test_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO test_user;

-- You can add more initialization commands here, such as:
-- - Creating tables
-- - Inserting initial data
-- - Setting up indexes