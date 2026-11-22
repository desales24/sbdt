# Panduan Langkah Pengerjaan Bagian H: Tugas Praktikum Mahasiswa
**Mata Kuliah:** Sistem Basis Data Terdistribusi (Pertemuan 6)  
**Studi Kasus:** Sistem Distribusi Pesanan Toko Online  
**Target Lingkungan:** pgAdmin 4 & PostgreSQL (Database: `db_barat`, `db_timur`, `db_pusat`)

---

## 📌 Deskripsi Tugas Bagian H
Pada tugas ini, Anda diminta merancang dan mengimplementasikan distribusi horizontal untuk data pesanan toko online:
1. **Node Barat (`db_barat`)**: Tabel `pesanan_barat` dengan constraint `CHECK (wilayah = 'Barat')` (minimal 5 baris).
2. **Node Timur (`db_timur`)**: Tabel `pesanan_timur` dengan constraint `CHECK (wilayah = 'Timur')` (minimal 5 baris).
3. **Koordinator (`db_pusat`)**: Foreign Table `ft_pesanan_barat`, `ft_pesanan_timur`, dan View `v_pesanan_semua`.
4. **Menjawab 5 Butir Pertanyaan Analisis & Evaluasi**.

---

## 🚀 Langkah 1: Buat Tabel & Data pada Node Barat (`db_barat`)

1. Di pgAdmin, klik kanan database **`db_barat`** $\rightarrow$ pilih **Query Tool**.
2. Salin dan jalankan skrip SQL berikut:

```sql
-- 1. Buat tabel fragmen horizontal pesanan_barat
DROP TABLE IF EXISTS pesanan_barat CASCADE;

CREATE TABLE pesanan_barat (
    id_pesanan INT PRIMARY KEY,
    nama_pelanggan VARCHAR(100) NOT NULL,
    wilayah VARCHAR(10) NOT NULL CHECK (wilayah = 'Barat'),
    total_belanja NUMERIC(12, 2) NOT NULL,
    tanggal_pesanan DATE NOT NULL
);

-- 2. Masukkan data sampel wilayah Barat (6 baris, minimal 5)
INSERT INTO pesanan_barat (id_pesanan, nama_pelanggan, wilayah, total_belanja, tanggal_pesanan) VALUES
(101, 'Andi Pratama', 'Barat', 750000.00, '2026-10-01'),
(102, 'Budi Santoso', 'Barat', 320000.00, '2026-10-02'),
(103, 'Citra Lestari', 'Barat', 1250000.00, '2026-10-04'),
(104, 'Deni Firmansyah', 'Barat', 450000.00, '2026-10-05'),
(105, 'Eka Wijaya', 'Barat', 890000.00, '2026-10-08'),
(106, 'Farhan Maulana', 'Barat', 210000.00, '2026-10-10');

-- 3. Verifikasi data lokal
SELECT * FROM pesanan_barat ORDER BY id_pesanan;
```

> [!TIP]
> 📸 **Screenshot Tugas 1:** Ambil tangkapan layar hasil query `SELECT * FROM pesanan_barat` yang menampilkan 6 baris data transaksi wilayah Barat.

---

## 🚀 Langkah 2: Buat Tabel & Data pada Node Timur (`db_timur`)

1. Di pgAdmin, klik kanan database **`db_timur`** $\rightarrow$ pilih **Query Tool**.
2. Salin dan jalankan skrip SQL berikut:

```sql
-- 1. Buat tabel fragmen horizontal pesanan_timur
DROP TABLE IF EXISTS pesanan_timur CASCADE;

CREATE TABLE pesanan_timur (
    id_pesanan INT PRIMARY KEY,
    nama_pelanggan VARCHAR(100) NOT NULL,
    wilayah VARCHAR(10) NOT NULL CHECK (wilayah = 'Timur'),
    total_belanja NUMERIC(12, 2) NOT NULL,
    tanggal_pesanan DATE NOT NULL
);

-- 2. Masukkan data sampel wilayah Timur (6 baris, ID unik global 201-206)
INSERT INTO pesanan_timur (id_pesanan, nama_pelanggan, wilayah, total_belanja, tanggal_pesanan) VALUES
(201, 'Gita Gutawa', 'Timur', 650000.00, '2026-10-01'),
(202, 'Hendra Saputra', 'Timur', 480000.00, '2026-10-03'),
(203, 'Intan Permata', 'Timur', 1500000.00, '2026-10-04'),
(204, 'Joko Widodo', 'Timur', 275000.00, '2026-10-06'),
(205, 'Kartika Sari', 'Timur', 920000.00, '2026-10-07'),
(206, 'Lukman Hakim', 'Timur', 510000.00, '2026-10-09');

-- 3. Verifikasi data lokal
SELECT * FROM pesanan_timur ORDER BY id_pesanan;
```

> [!TIP]
> 📸 **Screenshot Tugas 2:** Ambil tangkapan layar hasil query `SELECT * FROM pesanan_timur` yang menampilkan 6 baris data transaksi wilayah Timur.

---

## 🚀 Langkah 3: Konfigurasi FDW & View di Koordinator (`db_pusat`)

1. Di pgAdmin, klik kanan database **`db_pusat`** $\rightarrow$ pilih **Query Tool**.
2. Salin dan jalankan skrip SQL berikut untuk membuat Foreign Table dan View Gabungan:

```sql
-- 1. Pastikan ekstensi postgres_fdw aktif
CREATE EXTENSION IF NOT EXISTS postgres_fdw;

-- 2. Buat Foreign Table untuk menghubungkan ke tabel fisik remote
DROP FOREIGN TABLE IF EXISTS ft_pesanan_barat CASCADE;
CREATE FOREIGN TABLE ft_pesanan_barat (
    id_pesanan INT,
    nama_pelanggan VARCHAR(100),
    wilayah VARCHAR(10),
    total_belanja NUMERIC(12, 2),
    tanggal_pesanan DATE
)
SERVER server_barat
OPTIONS (schema_name 'public', table_name 'pesanan_barat');

DROP FOREIGN TABLE IF EXISTS ft_pesanan_timur CASCADE;
CREATE FOREIGN TABLE ft_pesanan_timur (
    id_pesanan INT,
    nama_pelanggan VARCHAR(100),
    wilayah VARCHAR(10),
    total_belanja NUMERIC(12, 2),
    tanggal_pesanan DATE
)
SERVER server_timur
OPTIONS (schema_name 'public', table_name 'pesanan_timur');

-- 3. Buat View Gabungan Transparansi Lokasi (v_pesanan_semua)
CREATE OR REPLACE VIEW v_pesanan_semua AS
SELECT * FROM ft_pesanan_barat
UNION ALL
SELECT * FROM ft_pesanan_timur;

-- 4. Verifikasi pembacaan view terdistribusi
SELECT * FROM v_pesanan_semua ORDER BY id_pesanan;
```

> [!TIP]
> 📸 **Screenshot Tugas 3:** Ambil tangkapan layar hasil query `SELECT * FROM v_pesanan_semua` di `db_pusat` (harus menampilkan 12 baris gabungan data dari Barat dan Timur).

---

## 🎯 Langkah 4: Penyelesaian 5 Butir Evaluasi Soal Bagian H

Jalankan kueri-kueri evaluasi berikut pada **Query Tool `db_pusat`**:

### Soal 1: Tampilkan Seluruh Pesanan dan Jumlah Pesanan per Wilayah

* **Kueri 1a (Seluruh Pesanan):**
  ```sql
  SELECT id_pesanan, nama_pelanggan, wilayah, total_belanja, tanggal_pesanan
  FROM v_pesanan_semua
  ORDER BY wilayah, id_pesanan;
  ```
* **Kueri 1b (Jumlah Pesanan per Wilayah):**
  ```sql
  SELECT wilayah, COUNT(*) AS jumlah_pesanan
  FROM v_pesanan_semua
  GROUP BY wilayah
  ORDER BY wilayah;
  ```
  *Ekspektasi Hasil:* Barat = 6, Timur = 6.

---

### Soal 2: Hitung Total Nilai Belanja Setiap Wilayah dengan SUM(total_belanja)

```sql
SELECT 
    wilayah,
    COUNT(*) AS total_transaksi,
    SUM(total_belanja) AS total_nilai_belanja,
    ROUND(AVG(total_belanja), 2) AS rata_rata_belanja
FROM v_pesanan_semua
GROUP BY wilayah
ORDER BY wilayah;
```
*Ekspektasi Hasil:*
* **Barat:** Total transaksi = 6, Total nilai belanja = Rp 3.870.000,00
* **Timur:** Total transaksi = 6, Total nilai belanja = Rp 4.335.000,00

---

### Soal 3: Tampilkan Pesanan dengan Total Belanja > 500.000

```sql
SELECT id_pesanan, nama_pelanggan, wilayah, total_belanja, tanggal_pesanan
FROM v_pesanan_semua
WHERE total_belanja > 500000
ORDER BY total_belanja DESC;
```
*Ekspektasi Hasil:* Menampilkan 6 transaksi yang memiliki nilai di atas Rp 500.000 (Andi, Citra, Eka dari Barat; Gita, Intan, Kartika, Lukman dari Timur).

* **Analisis Rencana Eksekusi Pushdown:**
  ```sql
  EXPLAIN (VERBOSE)
  SELECT * FROM v_pesanan_semua WHERE total_belanja > 500000;
  ```
  *(Perhatikan klausul `Remote SQL` pada hasil EXPLAIN menunjukkan bahwa kondisi `total_belanja > 500000` difilter langsung di node cabang).*

---

### Soal 4: Buktikan Jumlah Gabungan Sama dengan Kedua Fragmen & ID Tidak Duplikat

* **Kueri Pembuktian Kelengkapan & Rekonstruksi:**
  ```sql
  SELECT 
      COUNT(*) AS total_gabungan,
      COUNT(DISTINCT id_pesanan) AS total_id_unik,
      (SELECT COUNT(*) FROM ft_pesanan_barat) AS baris_node_barat,
      (SELECT COUNT(*) FROM ft_pesanan_timur) AS baris_node_timur,
      CASE 
          WHEN COUNT(*) = ((SELECT COUNT(*) FROM ft_pesanan_barat) + (SELECT COUNT(*) FROM ft_pesanan_timur)) 
               AND COUNT(*) = COUNT(DISTINCT id_pesanan)
          THEN 'TERBUKTI: Jumlah Cocok (12) & Tidak Ada ID Duplikat'
          ELSE 'GAGAL: Ditemukan Inkonsistensi'
      END AS status_validasi
  FROM v_pesanan_semua;
  ```

* **Kueri Pembuktian Saling Lepas (Disjointness):**
  ```sql
  -- Kedua query wajib menghasilkan 0 baris
  SELECT * FROM ft_pesanan_barat WHERE wilayah <> 'Barat';
  SELECT * FROM ft_pesanan_timur WHERE wilayah <> 'Timur';
  ```

---

### Soal 5: Penjelasan Pilihan Alokasi, Keuntungan, dan Risiko jika Salah Satu Node Tidak Tersedia

*(Bagian ini dapat disalin langsung ke lembar laporan praktikum Anda):*

#### 1. Alasan Pilihan Alokasi (Horizontal Fragmentation berdasarkan `wilayah`):
* **Prinsip Lokalitas Referensi (*Locality of Reference*):** Pada sistem toko online, pesanan pelanggan wilayah Barat umumnya diproses oleh gudang/cabang logistik Barat, dan sebaliknya. Menempatkan data di node regional yang paling sering mengaksesnya akan meminimalkan lalu lintas transmisi data jaringan luas (WAN).
* **Pemenuhan Aturan Kebenaran:**
  * *Completeness:* Setiap transaksi pasti memiliki wilayah (Barat atau Timur) sehingga tidak ada data yang tercecer.
  * *Reconstruction:* Data global dapat direkonstruksi utuh melalui operator `UNION ALL`.
  * *Disjointness:* Penegakan `CHECK (wilayah = ...)` mencegah terjadinya duplikasi data antar-node.

#### 2. Keuntungan:
* **Paralelisme & Skalabilitas Kueri:** Beban I/O baca dan tulis terbagi seimbang di antara server `db_barat` dan `db_timur`.
* **Latensi Rendah:** Transaksi lokal diproses langsung pada server lokal tanpa membebani koordinator pusat.
* **Transparansi Lokasi:** Aplikasi cukup memanggil view `v_pesanan_semua` tanpa perlu mengetahui alamat IP atau port masing-masing cabang.

#### 3. Risiko jika Salah Satu Node Tidak Tersedia (*Node Outage*):
* **Kegagalan Kueri Terpusat (*Single Point of Failure*):** Karena `v_pesanan_semua` menggunakan `UNION ALL` secara langsung ke foreign table fisik, apabila salah satu node (misal `db_timur`) mati atau jaringan terputus, maka kueri ke view `v_pesanan_semua` di `db_pusat` akan **gagal total** (*error: connection refused* atau *timeout*), sehingga data wilayah Barat yang sebenarnya masih hidup ikut tidak bisa diakses dari view pusat.
* **Rekomendasi Solusi/Mitigasi:**
  1. **Replikasi:** Mengombinasikan fragmentasi horizontal dengan *Read Replica* atau replikasi multi-master pada masing-masing cabang.
  2. **Materialized View / Caching:** Menyimpan cache data terpusat dengan penyegaran berkala (*periodic refresh*) sehingga saat node cabang terputus, sistem koordinator tetap dapat menyajikan data terakhir (*eventual consistency*).
