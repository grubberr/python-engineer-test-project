#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER centralnicgroup WITH PASSWORD 'centralnicgroup';
    CREATE DATABASE centralnicgroup;
    GRANT ALL PRIVILEGES ON DATABASE centralnicgroup TO centralnicgroup;
EOSQL
