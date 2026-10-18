-- ==============================================================================
-- PRAKTIKUM SISTEM BASIS DATA TERDISTRIBUSI - PERTEMUAN 5
-- TOPIK: REPLIKASI MULTI-MASTER (TWO-WAY LOGICAL REPLICATION)
-- ==============================================================================

-- ==============================================================================
-- LANGKAH 2: MEMBUAT DATABASE DAN ROLE PADA KEDUA NODE
-- ==============================================================================

-- [Jalankan di Node A DAN Node B pada database 'postgres']
CREATE ROLE repl_user WITH LOGIN REPLICATION PASSWORD 'GantiPasswordLab!';
CREATE DATABASE db_multimaster;

-- [Pindah koneksi ke database 'db_multimaster' di masing-masing node]
-- Jika di psql: \c db_multimaster
GRANT CONNECT ON DATABASE db_multimaster TO repl_user;
GRANT USAGE ON SCHEMA public TO repl_user;


-- ==============================================================================
-- LANGKAH 3: MEMBUAT SKEMA IDENTIK PADA KEDUA NODE
-- ==============================================================================

-- [Jalankan di Node A DAN Node B pada database 'db_multimaster']
CREATE TABLE produk (
    id BIGINT PRIMARY KEY,
    nama_produk VARCHAR(100) NOT NULL,
    stok INTEGER NOT NULL CHECK (stok >= 0),
    asal_node VARCHAR(10) NOT NULL
);

GRANT SELECT ON TABLE produk TO repl_user;


-- ==============================================================================
-- LANGKAH 4: MEMBUAT PUBLICATION PADA MASING-MASING NODE
-- ==============================================================================

-- [Jalankan HANYA di Node A (db_multimaster)]
CREATE PUBLICATION pub_a FOR TABLE produk
WITH (publish = 'insert, update, delete');

-- [Jalankan HANYA di Node B (db_multimaster)]
CREATE PUBLICATION pub_b FOR TABLE produk
WITH (publish = 'insert, update, delete');


-- ==============================================================================
-- LANGKAH 5: MEMBUAT SUBSCRIPTION SILANG
-- Catatan Jaringan:
-- Di Docker internal network, Node A menghubungi host 'node_b' port 5432,
-- dan Node B menghubungi host 'node_a' port 5432.
-- Opsi 'origin = none' wajib pada PostgreSQL 16+ agar tidak terjadi infinite loop.
-- ==============================================================================

-- [Jalankan di Node A (db_multimaster) - Mengambil data dari Node B]
CREATE SUBSCRIPTION sub_from_b
CONNECTION 'host=node_b port=5432 dbname=db_multimaster user=repl_user password=GantiPasswordLab!'
PUBLICATION pub_b
WITH (copy_data = false, origin = none);

-- [Jalankan di Node B (db_multimaster) - Mengambil data dari Node A]
CREATE SUBSCRIPTION sub_from_a
CONNECTION 'host=node_a port=5432 dbname=db_multimaster user=repl_user password=GantiPasswordLab!'
PUBLICATION pub_a
WITH (copy_data = false, origin = none);


-- ==============================================================================
-- LANGKAH 6: MENGUJI INSERT DUA ARAH
-- ==============================================================================

-- [Jalankan di Node A (db_multimaster) - ID GANJIL]
INSERT INTO produk VALUES (101, 'Keyboard', 20, 'A');
INSERT INTO produk VALUES (103, 'Mouse', 35, 'A');

-- [Jalankan di Node B (db_multimaster) - ID GENAP]
INSERT INTO produk VALUES (102, 'Monitor', 10, 'B');
INSERT INTO produk VALUES (104, 'Headset', 15, 'B');

-- [Verifikasi di KEDUA Node (Node A dan Node B)]
-- Tunggu beberapa detik, lalu jalankan:
SELECT id, nama_produk, stok, asal_node FROM produk ORDER BY id;
-- Ekspektasi: Muncul 4 baris (101, 102, 103, 104) di KEDUA node!


-- ==============================================================================
-- LANGKAH 7: MENGUJI UPDATE DAN DELETE DUA ARAH
-- ==============================================================================

-- [Jalankan di Node A - Ubah data dari A]
UPDATE produk SET stok = 25 WHERE id = 101;

-- [Jalankan di Node B - Ubah data dari B dan Hapus 104]
UPDATE produk SET stok = 12 WHERE id = 102;
DELETE FROM produk WHERE id = 104;

-- [Verifikasi di KEDUA Node setelah sinkron]
SELECT * FROM produk ORDER BY id;
-- Ekspektasi: 
-- Stok ID 101 = 25
-- Stok ID 102 = 12
-- Baris ID 104 terhapus di kedua node.


-- ==============================================================================
-- LANGKAH 8: MEMANTAU STATUS REPLIKASI
-- ==============================================================================

-- [Cek status Subscription lokal (Jalankan di masing-masing node)]
SELECT subname, pid, received_lsn, latest_end_lsn, latest_end_time 
FROM pg_stat_subscription;

-- [Cek aktivitas proses pengirim / Sender (Jalankan di masing-masing node)]
SELECT application_name, state, sent_lsn, replay_lsn 
FROM pg_stat_replication;
