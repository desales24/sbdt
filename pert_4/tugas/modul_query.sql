-- ==========================================
-- LANGKAH 1: Membuat dua schema simulasi
-- ==========================================
CREATE SCHEMA IF NOT EXISTS cabang_jakarta;
CREATE SCHEMA IF NOT EXISTS cabang_bandung;


-- ==========================================
-- LANGKAH 2: Membuat tabel pelanggan terfragmentasi
-- ==========================================
CREATE TABLE IF NOT EXISTS cabang_jakarta.pelanggan (
    id_pelanggan INT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    kota VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS cabang_bandung.pelanggan (
    id_pelanggan INT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    kota VARCHAR(50) NOT NULL
);


-- ==========================================
-- LANGKAH 3: Mengisi data contoh
-- ==========================================
INSERT INTO cabang_jakarta.pelanggan (id_pelanggan, nama, kota) VALUES
(1, 'Alya Putri', 'Jakarta'),
(2, 'Bima Pratama', 'Jakarta'),
(3, 'Citra Lestari', 'Jakarta')
ON CONFLICT (id_pelanggan) DO NOTHING;

INSERT INTO cabang_bandung.pelanggan (id_pelanggan, nama, kota) VALUES
(4, 'Deni Saputra', 'Bandung'),
(5, 'Eka Wulandari', 'Bandung'),
(6, 'Farhan Akbar', 'Bandung')
ON CONFLICT (id_pelanggan) DO NOTHING;

-- Cek hasil:
SELECT * FROM cabang_jakarta.pelanggan ORDER BY id_pelanggan;
SELECT * FROM cabang_bandung.pelanggan ORDER BY id_pelanggan;


-- ==========================================
-- LANGKAH 4: Membuat query gabungan (UNION ALL)
-- ==========================================
SELECT id_pelanggan, nama, kota, 'Jakarta' AS lokasi_sumber
FROM cabang_jakarta.pelanggan
UNION ALL
SELECT id_pelanggan, nama, kota, 'Bandung' AS lokasi_sumber
FROM cabang_bandung.pelanggan
ORDER BY id_pelanggan;


-- ==========================================
-- LANGKAH 5: Simulasi replikasi katalog buku
-- ==========================================
CREATE TABLE IF NOT EXISTS cabang_jakarta.katalog_buku (
    id_buku INT PRIMARY KEY,
    judul VARCHAR(150) NOT NULL,
    penulis VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS cabang_bandung.katalog_buku (
    id_buku INT PRIMARY KEY,
    judul VARCHAR(150) NOT NULL,
    penulis VARCHAR(100) NOT NULL
);

-- Isi katalog di Jakarta
INSERT INTO cabang_jakarta.katalog_buku VALUES
(101, 'Basis Data Modern', 'N. Rahman'),
(102, 'Sistem Terdistribusi', 'D. Prasetyo')
ON CONFLICT (id_buku) DO NOTHING;

-- Replikasi (Copy) data dari Jakarta ke Bandung
INSERT INTO cabang_bandung.katalog_buku
SELECT * FROM cabang_jakarta.katalog_buku
ON CONFLICT (id_buku) DO NOTHING;

-- Cek hasil replikasi:
SELECT * FROM cabang_jakarta.katalog_buku ORDER BY id_buku;
SELECT * FROM cabang_bandung.katalog_buku ORDER BY id_buku;
