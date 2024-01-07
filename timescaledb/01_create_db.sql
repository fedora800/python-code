
-- below needs to be run as the postgres user

\echo "Creating database dbs_invest"
CREATE DATABASE dbs_invest;

-- connect to our database
\echo "Connecting to dbs_invest"
\c dbs_invest;

-- add the timescaledb extension
\echo "Creating the timescaledb extension"
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- verify that this extension has been successfully installed
\echo "Listing all extensions, timescaledb needs to be in here"
\dx
-- output should show 1 row like - 
--    Name     | Version |   Schema   |                            Description
-- -------------+---------+------------+-------------------------------------------------------------------
-- plpgsql     | 1.0     | pg_catalog | PL/pgSQL procedural language
-- timescaledb | 2.7.0   | public     | Enables scalable inserts and complex queries for time-series data

