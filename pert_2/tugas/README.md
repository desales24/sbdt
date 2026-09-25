# 🏢 Tugas SBDT Pertemuan 2 - Multi Node PostgreSQL

Project ini adalah implementasi dari setup **3 Node PostgreSQL** (Jakarta, Bandung, dan Surabaya) menggunakan Docker Compose. Project ini dilengkapi dengan inisialisasi database otomatis (`penjualan`) beserta tabel `pelanggan` pada masing-masing node.

Selain itu, terdapat fitur **Monitoring & Auto-Reconnect** untuk memastikan konektivitas ke database lebih tangguh dan nyaman digunakan.

---

## 📋 Struktur Node dan Konfigurasi

Semua node berjalan menggunakan kredensial database yang sama, namun diakses dari host menggunakan port yang berbeda-beda.

**Kredensial Database:**

- **Database:** `penjualan`
- **Username:** `postgres`
- **Password:** `postgres`

### 🔗 Pemetaan Port (Akses dari Host Lokal)

| Nama Node          | Container Name    | Host Port | Internal Database Port |
| :----------------- | :---------------- | :-------- | :--------------------- |
| **Jakarta**  | `node_jakarta`  | `5432`  | `5432`               |
| **Bandung**  | `node_bandung`  | `5433`  | `5432`               |
| **Surabaya** | `node_surabaya` | `5434`  | `5432`               |

*(Note: Internal Database Port adalah port di mana antar container saling berkomunikasi).*

---

## 🚀 Persiapan & Cara Menjalankan

1. Pastikan **Docker** dan **Docker Compose** sudah terinstall di sistem Anda.
2. Buka terminal pada folder project ini.
3. Jalankan perintah berikut untuk membangun dan menghidupkan semua node:
   ```bash
   docker compose up -d
   ```
4. Docker akan mengeksekusi file `init.sql` dan otomatis membuat tabel `pelanggan` di masing-masing node.

---

## 💻 Cara Mengakses Database

Terdapat beberapa metode yang bisa Anda gunakan untuk mengakses database.

### 1. Menggunakan pgAdmin (Bawaan Docker)

Project ini sudah dilengkapi pgAdmin bawaan yang sangat mudah digunakan.

1. Buka browser dan kunjungi: `http://localhost:8080`
2. **Login** menggunakan:
   - **Email:** `admin@admin.com`
   - **Password:** `admin`
3. Tambahkan server (`Right-click Servers` -> `Register` -> `Server`).
4. Pada tab **Connection**, isi sesuai Node:
   - **Host:** `node_jakarta` / `node_bandung` / `node_surabaya`
   - **Port:** `5432` *(tetap 5432 untuk semua node)*
   - **Maintenance database:** `penjualan`
   - **Username:** `postgres`
   - **Password:** `postgres`
5. Klik Save.

### 2. Menggunakan Aplikasi Database Client (DBeaver / DataGrip / VSCode)

Jika Anda menggunakan aplikasi database eksternal yang diinstall di komputer Anda, Anda harus menggunakan **Host Port**:

- **Host:** `localhost`
- **Port:** `5432` (Jakarta), `5433` (Bandung), atau `5434` (Surabaya)
- **Database:** `penjualan`
- **Username:** `postgres`
- **Password:** `postgres`

### 3. Menggunakan Terminal Manual (`docker exec`)

Masuk ke terminal PostgreSQL (`psql`) langsung ke dalam container:

```bash
docker exec -it node_jakarta psql -U postgres -d penjualan
```

*(Ubah `node_jakarta` dengan nama node lain sesuai kebutuhan).*

---

## 🔄 Fitur Auto-Reconnect & Monitoring

Project ini dilengkapi dengan 3 buah *script* otomatis (`auto_connect_jakarta.sh`, `auto_connect_bandung.sh`, dan `auto_connect_surabaya.sh`) untuk memantau masing-masing server.

Jika salah satu server tiba-tiba mati, script tersebut akan menampilkan peringatan dan melakukan percobaan koneksi secara berkala. Ketika server hidup kembali, script akan langsung masuk ke terminal database secara otomatis tanpa meminta password ulang.

**Cara Menjalankan Script:**
Pilih script sesuai node yang ingin Anda akses/pantau:

```bash
./auto_connect_jakarta.sh
# atau
./auto_connect_bandung.sh
# atau
./auto_connect_surabaya.sh
```

**Cara Menguji Fitur:**

1. Jalankan salah satu script (misal: `./auto_connect_jakarta.sh`) di satu terminal.
2. Buka terminal baru, matikan node terkait secara paksa:
   ```bash
   docker stop node_jakarta
   ```
3. Lihat terminal pertama, akan muncul **PERINGATAN** bahwa server mati.
4. Hidupkan kembali node tersebut:
   ```bash
   docker start node_jakarta
   ```
5. Terminal pertama akan secara ajaib terhubung kembali secara otomatis! 🎉

---

## 📡 Komunikasi Antar Node (Cross-Node Query)

Karena seluruh node berada di dalam jaringan Docker yang sama (`db_network`), Anda bisa meremote Node Bandung atau Surabaya **langsung dari dalam** Node Jakarta.

Ketik perintah berikut saat Anda berada di dalam `psql` Jakarta (`penjualan=#`):

```sql
\c "host=node_bandung port=5432 dbname=penjualan user=postgres"
```

*(Masukkan password `postgres` saat diminta. Anda sekarang berada di dalam database Bandung).*

---

## 🛠️ Perintah Dasar PostgreSQL (`psql`)

Ketika Anda berada di dalam prompt `penjualan=#`, Anda bisa mengetik perintah berikut:

- `\dt` : Melihat daftar tabel di dalam database.
- `\d pelanggan` : Melihat struktur kolom dan tipe data dari tabel `pelanggan`.
- `SELECT * FROM pelanggan;` : Melihat isi baris data.
- `INSERT INTO pelanggan (nama_pelanggan, kota) VALUES ('Budi', 'Jakarta');` : Menambahkan data baru.
- `\q` : Keluar dari terminal `psql`.

---

## 🧹 Mematikan Semua Layanan

Jika Anda sudah selesai bereksperimen dan ingin mematikan semua container:

```bash
docker compose down
```

*(Data Anda tetap aman dan tidak akan hilang karena dikonfigurasi untuk disimpan pada Docker Volume secara permanen).*
