#!/bin/bash
# Script untuk terhubung langsung ke Node B (db_multimaster) via psql di dalam Docker container

DB_NAME="db_multimaster"

# Periksa apakah db_multimaster sudah dibuat, jika belum fallback ke postgres
if docker exec node_b psql -U postgres -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    TARGET_DB="$DB_NAME"
else
    TARGET_DB="postgres"
fi

echo "=================================================="
echo "  🚀 Menghubungkan ke Node B (Database: $TARGET_DB)..."
echo "=================================================="
docker exec -it node_b psql -U postgres -d "$TARGET_DB"
