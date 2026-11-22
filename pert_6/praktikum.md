# Panduan Praktikum Sistem Basis Data Terdistribusi (Pertemuan 6)

Panduan ini disusun secara berurutan dan terperinci, dimulai dari **pembuatan/pendaftaran server di pgAdmin**, dilanjutkan **Langkah 1 sampai 9 pada Bagian F**, hingga **Bagian G (Troubleshooting)** sesuai dokumen modul praktikum.

---

## 🛠️ Langkah Awal: Membuat / Mendaftarkan Server di pgAdmin

Sebelum membuat database, daftarkan terlebih dahulu instance PostgreSQL ke dalam pgAdmin:

1. Buka browser: [**http://localhost:5050**](http://localhost:5050)
   * **Email:** `admin@sbdt.com`
   * **Password:** `admin123`
2. Pada panel navigasi kiri, klik kanan pada **Servers** $\rightarrow$ pilih **Register** $\rightarrow$ **Server...**  
   *(Atau klik ikon **Add New Server** di dashboard utama).*
3. Pada tab **General**:
   * **Name:** `PostgreSQL Local` (atau nama lain yang Anda inginkan)
4. Pada tab **Connection**:
   * **Host name/address:** `postgres` *(karena pgAdmin dan PostgreSQL berjalan bersama dalam jaringan Docker)*
   * **Port:** `5432`
   * **Maintenance database:** `postgres`
   * **Username:** `postgres`
   * **Password:** `postgres123`
   * Centang opsi **Save password?**
5. Klik **Save**.
6. Server sekarang telah dibuat dan terhubung. Anda dapat mengklik tanda panah di samping nama server untuk membukanya.

---

## F. Langkah-langkah Praktikum

### Langkah 1 – Buat Tiga Database
Setelah server terbuka di panel kiri:
* **Cara Melalui GUI pgAdmin:**
  1. Klik kanan pada **Databases** di bawah server yang baru dibuat $\rightarrow$ pilih **Create** $\rightarrow$ **Database...**
  2. Pada kolom **Database**, masukkan `db_barat`, lalu klik **Save**.
  3. Ulangi langkah di atas untuk membuat `db_timur`.
  4. Ulangi langkah di atas untuk membuat `db_pusat`.

* **Alternatif Menggunakan Query Tool (pada database `postgres`):**
  *(Catatan: `CREATE DATABASE` tidak boleh dijalankan di dalam transaksi).*
  ```sql
  CREATE DATABASE db_barat;
  CREATE DATABASE db_timur;
  CREATE DATABASE db_pusat;
  ```

---

### Langkah 2 – Buat Tabel pada Node Barat
1. Di panel kiri pgAdmin, buka database **`db_barat`**.
2. Klik kanan pada `db_barat` $\rightarrow$ pilih **Query Tool** (pastikan jendela kueri aktif di `db_barat`).
3. Jalankan perintah SQL berikut:

```sql
CREATE TABLE pelanggan_barat (
    id_pelanggan INT PRIMARY KEY,
    nama VARCHAR(80) NOT NULL,
    wilayah VARCHAR(10) NOT NULL CHECK (wilayah = 'Barat'),
    kota VARCHAR(50) NOT NULL
);

INSERT INTO pelanggan_barat VALUES 
(1, 'Andi', 'Barat', 'Jakarta Barat'),
(2, 'Bunga', 'Barat', 'Tangerang'),
(3, 'Citra', 'Barat', 'Serang');

SELECT * FROM pelanggan_barat ORDER BY id_pelanggan;
```

---

### Langkah 3 – Buat Tabel pada Node Timur
1. Di panel kiri pgAdmin, buka database **`db_timur`**.
2. Klik kanan pada `db_timur` $\rightarrow$ pilih **Query Tool**.
3. Jalankan perintah SQL berikut:

```sql
CREATE TABLE pelanggan_timur (
    id_pelanggan INT PRIMARY KEY,
    nama VARCHAR(80) NOT NULL,
    wilayah VARCHAR(10) NOT NULL CHECK (wilayah = 'Timur'),
    kota VARCHAR(50) NOT NULL
);

INSERT INTO pelanggan_timur VALUES
(4, 'Dewi', 'Timur', 'Surabaya'),
(5, 'Eko', 'Timur', 'Malang'),
(6, 'Fajar', 'Timur', 'Denpasar');

SELECT * FROM pelanggan_timur ORDER BY id_pelanggan;
```

---

### Langkah 4 – Aktifkan FDW di Koordinator
1. Di panel kiri pgAdmin, buka database **`db_pusat`**.
2. Klik kanan pada `db_pusat` $\rightarrow$ pilih **Query Tool**.
3. Ekstensi `postgres_fdw` tersedia pada instalasi PostgreSQL standar. Jalankan perintah berikut untuk mengaktifkan ekstensi serta **membuat foreign server** (`server_barat` dan `server_timur`):

```sql
CREATE EXTENSION IF NOT EXISTS postgres_fdw;

CREATE SERVER server_barat FOREIGN DATA WRAPPER postgres_fdw 
    OPTIONS (host '127.0.0.1', port '5432', dbname 'db_barat');

CREATE SERVER server_timur FOREIGN DATA WRAPPER postgres_fdw 
    OPTIONS (host '127.0.0.1', port '5432', dbname 'db_timur');
```

---

### Langkah 5 – Atur Autentikasi Koneksi
Masih di **Query Tool** database **`db_pusat`**, buat pemetaan pengguna (*User Mapping*) ke masing-masing server node:

```sql
CREATE USER MAPPING FOR CURRENT_USER SERVER server_barat 
    OPTIONS (user 'praktikan', password 'praktikan123');

CREATE USER MAPPING FOR CURRENT_USER SERVER server_timur 
    OPTIONS (user 'praktikan', password 'praktikan123');
```

> [!NOTE]
> * Role `praktikan` dengan password `praktikan123` sudah dibuatkan di awal dan memiliki izin akses ke `db_barat` dan `db_timur`.
> * Jangan menampilkan password pada tangkapan layar laporan; hindari menggunakan akun superuser untuk sistem nyata.

---

### Langkah 6 – Definisikan Foreign Table
Masih di **Query Tool** database **`db_pusat`**, definisikan foreign table untuk mengakses tabel fisik yang berada di `db_barat` dan `db_timur`:

```sql
CREATE FOREIGN TABLE ft_pelanggan_barat (
    id_pelanggan INT,
    nama VARCHAR(80),
    wilayah VARCHAR(10),
    kota VARCHAR(50)
) SERVER server_barat OPTIONS (schema_name 'public', table_name 'pelanggan_barat');

CREATE FOREIGN TABLE ft_pelanggan_timur (
    id_pelanggan INT,
    nama VARCHAR(80),
    wilayah VARCHAR(10),
    kota VARCHAR(50)
) SERVER server_timur OPTIONS (schema_name 'public', table_name 'pelanggan_timur');

-- Uji pembacaan foreign table:
SELECT * FROM ft_pelanggan_barat;
SELECT * FROM ft_pelanggan_timur;
```

---

### Langkah 7 – Buat Tampilan Data Terdistribusi
`UNION ALL` menyatukan seluruh baris tanpa penghapusan duplikat; strategi ini tepat karena fragmen dirancang saling lepas (*disjoint*).

Masih di **Query Tool** database **`db_pusat`**, jalankan:

```sql
CREATE OR REPLACE VIEW v_pelanggan_semua AS
SELECT * FROM ft_pelanggan_barat
UNION ALL
SELECT * FROM ft_pelanggan_timur;

-- Tampilkan data gabungan:
SELECT * FROM v_pelanggan_semua ORDER BY id_pelanggan;

-- Tampilkan agregasi per wilayah:
SELECT wilayah, COUNT(*) AS jumlah 
FROM v_pelanggan_semua 
GROUP BY wilayah 
ORDER BY wilayah;
```

---

### Langkah 8 – Verifikasi Fragmentasi dan Alokasi
Jalankan rangkaian kueri pengujian berikut di **`db_pusat`**:

```sql
-- 1. Uji Kelengkapan (Hasil yang diharapkan: total 6 baris)
SELECT COUNT(*) AS total FROM v_pelanggan_semua;

-- 2. Uji Integritas Kunci (Hasil yang diharapkan: 6 ID unik)
SELECT COUNT(DISTINCT id_pelanggan) AS id_unik FROM v_pelanggan_semua;

-- 3. Uji Saling Lepas (Disjointness) - Kedua query harus menghasilkan 0 baris
SELECT * FROM ft_pelanggan_barat WHERE wilayah <> 'Barat';
SELECT * FROM ft_pelanggan_timur WHERE wilayah <> 'Timur';

-- 4. Uji Rencana Eksekusi Pushdown Predikat
EXPLAIN (VERBOSE) SELECT * FROM v_pelanggan_semua WHERE wilayah = 'Barat';
```

* **Hasil yang diharapkan:**
  * Total: `6` baris.
  * ID unik: `6`.
  * Pemeriksaan salah lokasi menghasilkan `0` baris.
  * `EXPLAIN` menampilkan akses *Foreign Scan* (kueri langsung diteruskan ke node fragmen terkait).

---

### Langkah 9 – Uji Pembaharuan Data di Node

1. **Jalankan di Query Tool `db_barat`:**
   ```sql
   INSERT INTO pelanggan_barat VALUES (7, 'Gilang', 'Barat', 'Cilegon');
   ```

2. **Kembali ke Query Tool `db_pusat` dan jalankan:**
   ```sql
   SELECT * FROM v_pelanggan_semua WHERE id_pelanggan = 7;
   SELECT COUNT(*) FROM v_pelanggan_semua;
   ```
   *Hasil yang diharapkan:* Gilang muncul dan total baris menjadi `7`.

3. **Uji Penolakan CHECK Constraint di `db_barat`:**
   Coba masukkan data yang tidak sesuai dengan predikat wilayah:
   ```sql
   INSERT INTO pelanggan_barat VALUES (8, 'Hadi', 'Timur', 'Surabaya');
   ```
   *Hasil yang diharapkan:* Percobaan INSERT dengan `wilayah = 'Timur'` ke `pelanggan_barat` ditolak oleh `CHECK constraint`.

---

## G. Troubleshooting

| Masalah | Penyebab / Solusi |
| :--- | :--- |
| `connection refused` | Pastikan service PostgreSQL aktif, host (`127.0.0.1`) dan port (`5432`) benar. |
| `password authentication failed` | Periksa user mapping, password, dan aturan `pg_hba.conf`. |
| `permission denied for table` | Berikan `SELECT` pada tabel node kepada role remote (`praktikan`). |
| `server already exists` | Objek server pernah dibuat; gunakan nama baru atau jalankan `DROP SERVER IF EXISTS ... CASCADE`. |
| `relation does not exist` | Periksa database yang aktif pada Query Tool, schema `public`, serta nama tabel. |
| `duplicate key value` | Gunakan ID pelanggan yang berbeda pada kedua fragmen agar unik secara global. |
