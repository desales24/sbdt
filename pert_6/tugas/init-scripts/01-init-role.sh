#!/bin/bash
set -e

echo "=== [SBDT INIT] Menyiapkan role praktikan untuk simulasi postgres_fdw ==="

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'praktikan') THEN
            CREATE ROLE praktikan WITH LOGIN SUPERUSER CREATEDB PASSWORD 'praktikan123';
        END IF;
    END
    \$\$;
EOSQL

echo "=== [SBDT INIT] Role praktikan siap. Database db_barat, db_timur, db_pusat TIDAK dibuat otomatis. ==="
