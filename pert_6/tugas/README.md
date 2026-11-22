# Konfigurasi Lingkungan Praktikum SBDT Pertemuan 6 (Docker & pgAdmin)

Folder ini berisi konfigurasi lingkungan **PostgreSQL 16** dan **pgAdmin 4** berbasis Docker Compose untuk menjalankan simulasi Sistem Basis Data Terdistribusi (Pertemuan 6).

---

## 📁 Struktur Direktori

```text
tugas/
├── docker-compose.yml            # Konfigurasi container PostgreSQL & pgAdmin 4
├── .env                          # Kredensial & variabel lingkungan
├── .env.example                  # Template variabel lingkungan
├── init-scripts/
│   └── 01-init-role.sh           # Menyiapkan role praktikan (database dibuat manual oleh mahasiswa)
└── README.md                     # Panduan penggunaan
```

---

## 🔑 Kredensial Default

### 1. PostgreSQL Cluster
* **Host**: `localhost` (atau `127.0.0.1`)
* **Port**: `5432`
* **Superuser**: `postgres` / `postgres123`
* **Role Praktikan**: `praktikan` / `praktikan123`
* **Database bawaan**: `postgres` (database `db_barat`, `db_timur`, dan `db_pusat` dibuat manual oleh mahasiswa sesuai panduan praktikum)

### 2. pgAdmin 4 (Web Interface)
* **URL**: [http://localhost:5050](http://localhost:5050)
* **Email**: `admin@sbdt.com`
* **Password**: `admin123`

---

## 🚀 Panduan Menjalankan Lingkungan Docker

Masuk ke direktori `tugas`, lalu jalankan:

```bash
cd /home/desales/sbdt/pert_6/tugas
docker compose up -d
```

Untuk memverifikasi kedua container telah berjalan:
```bash
docker compose ps
```

---

## 🖥️ Mengakses pgAdmin 4

1. Buka browser dan arahkan ke [**http://localhost:5050**](http://localhost:5050).
2. Masukkan email `admin@sbdt.com` dan password `admin123`.
3. pgAdmin sekarang kosong tanpa server otomatis. Anda dapat mendaftarkan server secara manual mengikuti panduan di [**`../praktikum.md`**](../praktikum.md).

---

## 🛑 Menghentikan Layanan Docker

Jika praktikum telah selesai, matikan container dengan perintah:

```bash
docker compose down
```
