#!/bin/bash

# Mengatur variabel environment agar psql tidak meminta password
export PGPASSWORD="postgres"

echo "Memulai sistem monitoring dan auto-connect ke Node Surabaya..."

while true; do
    # Mengecek apakah database merespon (ping sederhana)
    if docker exec node_surabaya psql -U postgres -d penjualan -c "SELECT 1;" > /dev/null 2>&1; then
        echo "======================================================"
        echo "[STATUS: HIDUP] Berhasil terhubung ke Node Surabaya!"
        echo "Membuka terminal database..."
        echo "======================================================"
        
        # Masuk ke terminal interaktif
        docker exec -it node_surabaya psql -U postgres -d penjualan
        EXIT_CODE=$?
        
        # Jika pengguna sengaja keluar (\q), exit code akan bernilai 0
        if [ $EXIT_CODE -eq 0 ]; then
            echo "Keluar dari database. Menghentikan script."
            break
        fi
    else
        # Jika gagal terhubung, tampilkan peringatan
        echo "======================================================"
        echo "[PERINGATAN] Server Surabaya sedang MATI atau tidak dapat diakses!"
        echo "Mencoba menghubungkan kembali dalam 3 detik..."
        echo "======================================================"
        sleep 3
    fi
done
