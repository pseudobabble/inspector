#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE document_store;
    GRANT ALL PRIVILEGES ON DATABASE document_store TO $POSTGRES_USER;
EOSQL
