1. Jalankan `docker compose up -d`
2. PostgreSQL bisa diakses di `localhost:5432` (user: `postgres`, password: `postgres`, db: `mydatabase`)
3. pgAdmin dibuka di `http://localhost:8080` (login: `admin@admin.com` / `admin`)
4. Di pgAdmin, tambahkan server baru dengan host `postgres` (nama service, bukan `localhost`), port `5432`, dan kredensial di atas
