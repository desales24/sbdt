# 🏢 Praktikum Sistem Basis Data Terdistribusi (Simulasi)

Project ini merupakan lingkungan **Simulasi Basis Data Terdistribusi** menggunakan Docker. 

Alih-alih menggunakan banyak server fisik yang berat, praktikum ini menggunakan **1 buah server PostgreSQL** yang dibagi secara logis menjadi beberapa **Schema** (`cabang_jakarta` dan `cabang_bandung`). Melalui simulasi ini, Anda dapat mempraktikkan konsep *Fragmentasi Horizontal*, *Distributed Query (UNION ALL)*, dan *Replikasi Data* dengan mudah.

---

## 📂 Struktur File Saat Ini

- `docker-compose.yml` : Konfigurasi untuk menjalankan PostgreSQL dan pgAdmin.
- `modul_query.sql` : Kumpulan *script* SQL lengkap (Langkah 1 sampai 5) yang siap dieksekusi.
- `praktikum/Bahan Ajar Praktikum.docx` : Modul panduan asli praktikum Anda.

---

## 🚀 Cara Menjalankan Lingkungan (Docker)

1. Pastikan Docker dan Docker Compose sudah berjalan di komputer Anda.
2. Buka terminal di folder project ini.
3. Jalankan perintah berikut untuk menyalakan server:
   ```bash
   docker compose up -d --build
   ```

---

## 💻 Cara Mengakses Database via pgAdmin

Karena Anda akan menggunakan pgAdmin untuk mengeksekusi semua query, ikuti langkah berikut:

1. Buka browser dan kunjungi: `http://localhost:8080`
2. **Login** menggunakan kredensial berikut:
   - **Email:** `admin@admin.com`
   - **Password:** `admin`
3. Tambahkan koneksi server baru dengan cara: 
   - Klik Kanan pada **Servers** -> **Register** -> **Server**
   - Pada tab **General**, isi *Name* dengan bebas (misal: `Server Praktikum`).
   - Pada tab **Connection**, isi detail berikut:
     - **Host name/address:** `postgres_db`
     - **Port:** `5432`
     - **Maintenance database:** `penjualan`
     - **Username:** `postgres`
     - **Password:** `postgres`
4. Klik **Save**.

---

## 📝 Cara Mengerjakan Modul Praktikum

1. Setelah berhasil terhubung di pgAdmin, rentangkan (expand) menu server di sebelah kiri.
2. Navigasikan ke: `Databases` -> `penjualan`.
3. Klik kanan pada database `penjualan` lalu pilih **Query Tool**.
4. Buka file `modul_query.sql` yang ada di folder ini menggunakan Code Editor Anda (seperti VS Code).
5. **Copy** baris kode SQL sesuai langkah yang sedang Anda kerjakan, lalu **Paste** ke dalam *Query Tool* di pgAdmin.
6. Tekan tombol **Execute / Run** (ikon *play* ▶️ atau tekan `F5`).
7. Amati hasilnya pada panel Data Output di bagian bawah.

---

## 🧹 Cara Mematikan Layanan
Jika Anda sudah selesai melakukan praktikum, Anda bisa mematikan containernya dengan perintah:
```bash
docker compose down
```
