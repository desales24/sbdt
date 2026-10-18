# 🔄 Praktikum Sistem Basis Data Terdistribusi - Pertemuan 5
## Topik: Replikasi Multi-Master (Two-Way Logical Replication) PostgreSQL 16

Dokumentasi dan panduan praktikum ini disusun berdasarkan **Bagian D (Langkah Kerja Praktikum)** dari modul *Bahan Ajar Praktikum Sistem Basis Data Terdistribusi - Universitas Esa Unggul*. 

Project ini telah disiapkan menggunakan **Docker Compose** dengan dua node PostgreSQL 16 (`node_a` dan `node_b`) serta **pgAdmin 4**.

---

## 🏗️ 1. Arsitektur dan Pemetaan Port

Replikasi multi-master dua arah memungkinkan kedua node menerima operasi tulis (*write*) secara lokal, kemudian menyinkronkannya ke node pasangan.

```
       +-----------------------+              +-----------------------+
       |   Node A (Port 5432)  | <=========>  |   Node B (Port 5433)  |
       |  (pub_a / sub_from_b) |  Logical     |  (pub_b / sub_from_a) |
       +-----------------------+  Replication +-----------------------+
                   ^                                      ^
                   |                                      |
                   +------------------+-------------------+
                                      |
                            +--------------------+
                            | pgAdmin (Port 8080)|
                            +--------------------+
```

### Rincian Koneksi

| Komponen | Node A | Node B | pgAdmin |
| :--- | :--- | :--- | :--- |
| **Container Name** | `node_a` | `node_b` | `pgadmin_pert5` |
| **Port Host (Lokal)** | `5432` | `5433` | `8080` |
| **Port Internal Docker** | `5432` | `5432` | `80` |
| **Superuser Default** | `postgres` / `postgres` | `postgres` / `postgres` | `admin@admin.com` / `admin` |
| **User Replikasi** | `repl_user` / `GantiPasswordLab!` | `repl_user` / `GantiPasswordLab!` | - |
| **Database Praktikum** | `db_multimaster` | `db_multimaster` | - |

> [!IMPORTANT]
> **Catatan Jaringan Internal Docker:**
> Pada modul tertulis `host=127.0.0.1 port=5433`. Karena kita menggunakan Docker Compose, antar-kontainer terhubung melalui jaringan virtual internal (`db_network`).
> - Dari **Node A** ke Node B menggunakan: `host=node_b port=5432`
> - Dari **Node B** ke Node A menggunakan: `host=node_a port=5432`
>
> Jika Anda mengakses dari aplikasi luar di komputer Anda (misal DBeaver atau pgAdmin di komputer lokal), gunakan port luar: Node A di `localhost:5432` dan Node B di `localhost:5433`.

---

## ⚙️ 2. Konfigurasi Parameter Mesin (Otomatis)

Pada `docker-compose.yml`, kedua instance PostgreSQL 16 sudah dikonfigurasi dengan parameter wajib sesuai modul:

```yaml
wal_level = logical
max_replication_slots = 10
max_wal_senders = 10
max_logical_replication_workers = 8
max_worker_processes = 16
```
Parameter ini langsung aktif begitu container dijalankan tanpa perlu mengedit `postgresql.conf` secara manual.

---

## 🚀 3. Langkah Kerja Praktikum (Sesuai Modul Bagian D)

### Langkah 1: Menjalankan Container
Buka terminal di dalam folder `tugas/`, lalu jalankan:

```bash
docker compose up -d
```

Pastikan semua kontainer berstatus `healthy` / `running`:
```bash
docker compose ps
```

---

### Langkah 2: Membuat Database dan Role pada Kedua Node

Jalankan perintah SQL ini pada database administratif bawaan (`postgres`) di **kedua node**.

#### Cara Eksekusi:
Buka dua terminal terpisah:
- **Terminal 1 (Node A):**
  ```bash
  docker exec -it node_a psql -U postgres -d postgres
  ```
- **Terminal 2 (Node B):**
  ```bash
  docker exec -it node_b psql -U postgres -d postgres
  ```

#### SQL yang Dijalankan (di Node A dan Node B):
```sql
CREATE ROLE repl_user WITH LOGIN REPLICATION PASSWORD 'GantiPasswordLab!';
CREATE DATABASE db_multimaster;
```

Setelah database dibuat, hubungkan sesi `psql` ke database baru `db_multimaster`:
```sql
\c db_multimaster
```

Kemudian berikan izin akses ke `repl_user`:
```sql
GRANT CONNECT ON DATABASE db_multimaster TO repl_user;
GRANT USAGE ON SCHEMA public TO repl_user;
```

---

### Langkah 3: Membuat Skema Identik pada Kedua Node

Jalankan query DDL berikut di **Node A** dan **Node B** (pastikan sudah berada di dalam database `db_multimaster`):

```sql
CREATE TABLE produk (
    id BIGINT PRIMARY KEY,
    nama_produk VARCHAR(100) NOT NULL,
    stok INTEGER NOT NULL CHECK (stok >= 0),
    asal_node VARCHAR(10) NOT NULL
);

GRANT SELECT ON TABLE produk TO repl_user;
```

> [!NOTE]
> *Primary key* wajib ada untuk operasi `UPDATE` dan `DELETE` pada logical replication agar PostgreSQL dapat mengidentifikasi baris yang diubah (*replica identity*). DDL/skema **tidak** otomatis direplikasi antar node, sehingga harus dibuat manual di kedua sisi.

---

### Langkah 4: Membuat Publication pada Masing-Masing Node

#### Di Terminal Node A (`db_multimaster`):
```sql
CREATE PUBLICATION pub_a FOR TABLE produk
WITH (publish = 'insert, update, delete');
```

#### Di Terminal Node B (`db_multimaster`):
```sql
CREATE PUBLICATION pub_b FOR TABLE produk
WITH (publish = 'insert, update, delete');
```

---

### Langkah 5: Membuat Subscription Silang

> [!WARNING]
> Opsi `origin = none` adalah fitur **PostgreSQL 16+** yang sangat krusial! Opsi ini mencegah terjadinya replikasi melingkar (*looping*), sehingga data yang diterima dari replikasi tidak akan diteruskan kembali ke pengirim aslinya.

#### Di Terminal Node A (Mengambil perubahan dari Node B):
```sql
CREATE SUBSCRIPTION sub_from_b
CONNECTION 'host=node_b port=5432 dbname=db_multimaster user=repl_user password=GantiPasswordLab!'
PUBLICATION pub_b
WITH (copy_data = false, origin = none);
```

#### Di Terminal Node B (Mengambil perubahan dari Node A):
```sql
CREATE SUBSCRIPTION sub_from_a
CONNECTION 'host=node_a port=5432 dbname=db_multimaster user=repl_user password=GantiPasswordLab!'
PUBLICATION pub_a
WITH (copy_data = false, origin = none);
```

---

### Langkah 6: Menguji INSERT Dua Arah

Untuk menghindari tabrakan primary key:
- **Node A:** gunakan ID ganjil (101, 103, ...)
- **Node B:** gunakan ID genap (102, 104, ...)

#### 1. Jalankan di Node A:
```sql
INSERT INTO produk VALUES (101, 'Keyboard', 20, 'A');
INSERT INTO produk VALUES (103, 'Mouse', 35, 'A');
```

#### 2. Jalankan di Node B:
```sql
INSERT INTO produk VALUES (102, 'Monitor', 10, 'B');
INSERT INTO produk VALUES (104, 'Headset', 15, 'B');
```

#### 3. Periksa Hasil di KEDUA Node:
Tunggu 1-2 detik, lalu jalankan query ini di **Node A** dan **Node B**:
```sql
SELECT id, nama_produk, stok, asal_node FROM produk ORDER BY id;
```

**Hasil yang diharapkan di KEDUA node:**
```text
 id  | nama_produk | stok | asal_node 
-----+-------------+------+-----------
 101 | Keyboard    |   20 | A
 102 | Monitor     |   10 | B
 103 | Mouse       |   35 | A
 104 | Headset     |   15 | B
(4 rows)
```

---

### Langkah 7: Menguji UPDATE dan DELETE Dua Arah

#### 1. Jalankan di Node A (Ubah data milik Node A):
```sql
UPDATE produk SET stok = 25 WHERE id = 101;
```

#### 2. Jalankan di Node B (Ubah dan hapus data milik Node B):
```sql
UPDATE produk SET stok = 12 WHERE id = 102;
DELETE FROM produk WHERE id = 104;
```

#### 3. Periksa Hasil Akhir di KEDUA Node:
```sql
SELECT * FROM produk ORDER BY id;
```

**Hasil yang diharapkan di KEDUA node:**
```text
 id  | nama_produk | stok | asal_node 
-----+-------------+------+-----------
 101 | Keyboard    |   25 | A
 102 | Monitor     |   12 | B
 103 | Mouse       |   35 | A
(3 rows)
```
*(Stok ID 101 terupdate menjadi 25, stok ID 102 menjadi 12, dan baris ID 104 telah terhapus).*

---

### Langkah 8: Memantau Status Replikasi

Jalankan perintah monitoring berikut pada masing-masing node untuk memverifikasi proses replikasi:

#### A. Cek Status Subscription Lokal:
```sql
SELECT subname, pid, received_lsn, latest_end_lsn, latest_end_time
FROM pg_stat_subscription;
```
*Interpretasi:* Kolom `pid` yang terisi menandakan background apply worker sedang aktif.

#### B. Cek Status Sender (Aktivitas Pengirim):
```sql
SELECT application_name, state, sent_lsn, replay_lsn
FROM pg_stat_replication;
```
*Interpretasi:* Kolom `state` biasanya menunjukkan `streaming` bila node pengirim sedang aktif mereplikasi data.

---

## 📊 4. Tabel Pengamatan Praktikum (Bagian E Modul)

Salin tabel ini ke laporan praktikum Anda dan isi dengan hasil tangkapan layar/hasil query Anda:

| Uji | Perubahan | Hasil Node A | Hasil Node B |
| :---: | :--- | :--- | :--- |
| **1** | `INSERT 101 dari A` | Sukses tersimpan (asal_node 'A') | Tersinkron otomatis ke Node B |
| **2** | `INSERT 102 dari B` | Tersinkron otomatis ke Node A | Sukses tersimpan (asal_node 'B') |
| **3** | `UPDATE 101 dari A` | Nilai stok berubah menjadi 25 | Nilai stok tersinkron menjadi 25 |
| **4** | `UPDATE 102 dari B` | Nilai stok tersinkron menjadi 12 | Nilai stok berubah menjadi 12 |
| **5** | `DELETE 104 dari B` | Baris 104 terhapus | Baris 104 terhapus |

---

## 🛠️ 5. Troubleshooting Cepat (Bagian F Modul)

| Gejala Masalah | Penyebab Umum | Solusi |
| :--- | :--- | :--- |
| **Connection refused** | Port salah atau kontainer tujuan belum aktif. | Pastikan `host=node_b` (bukan 127.0.0.1 dari dalam container) dan port `5432`. |
| **Logical decoding requires wal_level logical** | Konfigurasi PostgreSQL belum diset `logical`. | Sudah ditangani oleh flag `-c wal_level=logical` pada `docker-compose.yml`. |
| **Duplicate key / apply worker berhenti** | Ada benturan primary key (misal ID 101 di-insert di kedua node). | Periksa log `docker compose logs -f node_a`, selesaikan konflik atau sesuaikan data secara manual. |
| **Data tidak muncul di node lawan** | `copy_data = false` hanya mereplikasi perubahan *setelah* subscription aktif. | Pastikan urutan: Buat tabel → Buat publication & subscription → Baru lakukan INSERT. |

---

## 💡 6. Script Bantuan Cepat

Tersedia file script untuk mempermudah akses terminal langsung ke database:
- `./connect_node_a.sh` : Langsung membuka sesi `psql` ke Node A.
- `./connect_node_b.sh` : Langsung membuka sesi `psql` ke Node B.
- `modul_langkah_kerja.sql` : Berisi seluruh skrip SQL lengkap siap pakai.

---

## 🛑 7. Mematikan Container

Bila praktikum telah selesai:
```bash
docker compose down
```
Untuk membersihkan volume data jika ingin mengulang dari awal:
```bash
docker compose down -v
```
