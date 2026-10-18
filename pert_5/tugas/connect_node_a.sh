#!/bin/bash
# Script untuk terhubung langsung ke Node A (db_multimaster) via psql di dalam Docker container

DB_NAME="db_multimaster"

# Periksa apakah db_multimaster sudah dibuat, jika belum fallback ke postgres
if docker exec node_a psql -U postgres -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    TARGET_DB="$DB_NAME"
else
    TARGET_DB="postgres"
fi

echo "=================================================="
echo "  🚀 Menghubungkan ke Node A (Database: $TARGET_DB)..."
echo "=================================================="
docker exec -it node_a psql -U postgres -d "$TARGET_DB"
