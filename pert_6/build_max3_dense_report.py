import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

DIR_PRAKTIKUM_IMG = "/home/desales/sbdt/pert_6/dokumentasi"
DIR_TUGAS_IMG = "/home/desales/sbdt/pert_6/dokumentasi_tugas"
OUTPUT_FILE = "/home/desales/sbdt/pert_6/Laporan_Praktikum_Pertemuan_6.docx"

def set_cell_shading(cell, color_hex):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def set_cell_margins(cell, top=25, bottom=25, left=50, right=50):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def prevent_row_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def add_code_block(doc, code_text, keep_with_next=True):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(7.2)
    cell = tbl.cell(0, 0)
    set_cell_shading(cell, "F6F8FA")
    set_cell_margins(cell, top=25, bottom=25, left=60, right=60)
    prevent_row_split(tbl.rows[0])
    
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="14" w:space="0" w:color="005691"/>'
        f'<w:top w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    cell._tc.get_or_add_tcPr().append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.02
    p.paragraph_format.keep_with_next = keep_with_next
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(7.5)
    run.font.color.rgb = RGBColor(20, 35, 60)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(1)
    p_after.paragraph_format.keep_with_next = keep_with_next

def add_image(doc, img_dir, filename, caption_text, width=Inches(4.1), keep_with_next=True):
    full_path = os.path.join(img_dir, filename)
    if os.path.exists(full_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(1)
        p_img.paragraph_format.space_after = Pt(1)
        p_img.paragraph_format.keep_with_next = True
        run_img = p_img.add_run()
        run_img.add_picture(full_path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(2)
        p_cap.paragraph_format.keep_with_next = keep_with_next
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.name = "Calibri"
        run_cap.font.size = Pt(8.0)
        run_cap.font.italic = True
        run_cap.font.color.rgb = RGBColor(80, 80, 80)
    else:
        print(f"Warning: File not found: {full_path}")

doc = Document()

for section in doc.sections:
    section.top_margin = Inches(0.6)
    section.bottom_margin = Inches(0.6)
    section.left_margin = Inches(0.6)
    section.right_margin = Inches(0.6)

C_PRIMARY = RGBColor(0, 51, 102)     # Deep Navy
C_SECONDARY = RGBColor(40, 80, 120)  # Slate Blue
C_TEXT = RGBColor(35, 35, 35)        # Dark Charcoal

def p_para(text, before=0, after=2, line_spacing=1.03, bold=False, italic=False, color=C_TEXT, keep_with_next=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.keep_with_next = keep_with_next
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(8.5)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return p

def p_eval(text, keep_with_next=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.03
    p.paragraph_format.keep_with_next = keep_with_next
    run_bullet = p.add_run("• ")
    run_bullet.font.name = "Calibri"
    run_bullet.font.size = Pt(8.0)
    run_bullet.font.bold = True
    run_bullet.font.color.rgb = C_PRIMARY
    
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(8.0)
    run.font.italic = True
    run.font.color.rgb = RGBColor(50, 50, 50)
    return p

def p_section_title(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(10.5)
    run.font.bold = True
    run.font.color.rgb = C_PRIMARY
    return p

def p_step_title(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(9.0)
    run.font.bold = True
    run.font.color.rgb = C_SECONDARY
    return p

# ==============================================================================
# HALAMAN 1 (Gambar 1, 2, 3)
# ==============================================================================
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(0)
p_title.paragraph_format.space_after = Pt(1)
p_title.paragraph_format.keep_with_next = True
run = p_title.add_run("LAPORAN PRAKTIKUM SISTEM BASIS DATA TERDISTRIBUSI")
run.font.name = "Calibri"
run.font.size = Pt(12.0)
run.font.bold = True
run.font.color.rgb = C_PRIMARY

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_before = Pt(0)
p_sub.paragraph_format.space_after = Pt(3)
p_sub.paragraph_format.keep_with_next = True
run = p_sub.add_run("Pertemuan 6: Distribusi dan Alokasi Data (Fragmentasi Horizontal & Transparansi Lokasi)")
run.font.name = "Calibri"
run.font.size = Pt(8.5)
run.font.italic = True
run.font.color.rgb = C_SECONDARY

tbl_id = doc.add_table(rows=2, cols=4)
tbl_id.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_id.autofit = False
tbl_id.columns[0].width = Inches(1.2)
tbl_id.columns[1].width = Inches(2.4)
tbl_id.columns[2].width = Inches(1.2)
tbl_id.columns[3].width = Inches(2.4)
prevent_row_split(tbl_id.rows[0])
prevent_row_split(tbl_id.rows[1])

id_grid = [
    [("Nama", "Desales"), ("Mata Kuliah", "Sistem Basis Data Terdistribusi")],
    [("NIM", "[Isi NIM Mahasiswa]"), ("Dosen Pengampu", "Ranny Meilisa, S.Kom., M.Pd.T")]
]

for r_i, row in enumerate(id_grid):
    for c_i, (k, v) in enumerate(row):
        c_k = tbl_id.cell(r_i, c_i * 2)
        c_v = tbl_id.cell(r_i, c_i * 2 + 1)
        set_cell_margins(c_k, top=10, bottom=10, left=25, right=25)
        set_cell_margins(c_v, top=10, bottom=10, left=25, right=25)
        set_cell_shading(c_k, "F0F4F8")
        set_cell_shading(c_v, "FFFFFF")
        
        p_k = c_k.paragraphs[0]
        p_k.paragraph_format.space_before = Pt(1)
        p_k.paragraph_format.space_after = Pt(1)
        p_k.paragraph_format.keep_with_next = True
        rk = p_k.add_run(k)
        rk.font.name = "Calibri"
        rk.font.size = Pt(8.0)
        rk.font.bold = True
        
        p_v = c_v.paragraphs[0]
        p_v.paragraph_format.space_before = Pt(1)
        p_v.paragraph_format.space_after = Pt(1)
        p_v.paragraph_format.keep_with_next = True
        rv = p_v.add_run(v)
        rv.font.name = "Calibri"
        rv.font.size = Pt(8.0)

p_section_title("BAGIAN I. LANGKAH-LANGKAH PRAKTIKUM INTI (BAGIAN F)")
p_step_title("Langkah Awal: Pendaftaran dan Konfigurasi Server di pgAdmin")
p_para("Mendaftarkan server PostgreSQL Local pada pgAdmin (Host: 'postgres', Port: 5432, User: 'postgres', Password: 'postgres123').", keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "konfigurasi 1.png", "Gambar 1: Menu Pendaftaran Server Baru (Tab General)", width=Inches(4.1), keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "konfigurasi 2.png", "Gambar 2: Konfigurasi Parameter Host dan Port Koneksi Server (Tab Connection)", width=Inches(4.1), keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "konfigurasi 3.png", "Gambar 3: Server 'PostgreSQL Local' Berhasil Terhubung pada pgAdmin", width=Inches(4.1), keep_with_next=False)

# ==============================================================================
# HALAMAN 2 (Gambar 4, 5, 6)
# ==============================================================================
doc.add_page_break()
p_step_title("Langkah 1: Membuat Tiga Basis Data (db_barat, db_timur, db_pusat)")
p_para("Membuat basis data db_barat (node barat), db_timur (node timur), dan db_pusat (koordinator FDW).", keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "membuat database 1.png", "Gambar 4: Form Pembuatan Database Baru pada pgAdmin", width=Inches(4.1), keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "membuat database 2.png", "Gambar 5: Proses Penyimpanan Properti Database", width=Inches(4.1), keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "hasil create database. database terbuat.png", "Gambar 6: Tiga Database (db_barat, db_timur, db_pusat) Terdaftar Sukses", width=Inches(4.1), keep_with_next=False)

# ==============================================================================
# HALAMAN 3 (Gambar 7, 8, 9)
# ==============================================================================
doc.add_page_break()
p_step_title("Membuka Query Tool pada Database Target")
p_para("Membuka jendela Query Tool pada masing-masing database untuk mengeksekusi skrip SQL.", keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "membuka query.png", "Gambar 7: Membuka Query Tool pada pgAdmin", width=Inches(4.1), keep_with_next=True)

p_step_title("Langkah 2: Membuat Tabel pada Node Barat (db_barat)")
p_para("Membuat tabel pelanggan_barat dengan constraint CHECK (wilayah = 'Barat') dan memasukkan 3 data sampel (Andi, Bunga, Citra).", keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "membuat table db_barat.png", "Gambar 8: Eksekusi DDL, DML, dan Verifikasi Data Tabel pelanggan_barat pada db_barat", width=Inches(4.1), keep_with_next=True)

p_step_title("Langkah 3: Membuat Tabel pada Node Timur (db_timur)")
p_para("Membuat tabel pelanggan_timur dengan constraint CHECK (wilayah = 'Timur') dan memasukkan 3 data sampel (Dewi, Eko, Fajar).", keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "membuat table db_timur.png", "Gambar 9: Eksekusi DDL, DML, dan Verifikasi Data Tabel pelanggan_timur pada db_timur", width=Inches(4.1), keep_with_next=False)

# ==============================================================================
# HALAMAN 4 (Gambar 10, 11, 12)
# ==============================================================================
doc.add_page_break()
p_step_title("Langkah 4: Mengaktifkan FDW di Koordinator (db_pusat)")
p_para("Mengaktifkan ekstensi postgres_fdw dan membuat Foreign Server server_barat serta server_timur di db_pusat.", keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "mengaktifkan fwd.png", "Gambar 10: Aktivasi Ekstensi postgres_fdw dan Pembuatan Foreign Server", width=Inches(4.1), keep_with_next=True)

p_step_title("Langkah 5: Mengatur Autentikasi Koneksi (User Mapping)")
p_para("Membuat User Mapping untuk CURRENT_USER ke server_barat dan server_timur menggunakan role 'praktikan'.", keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "Atur Autentikasi Koneksi.png", "Gambar 11: Konfigurasi User Mapping di db_pusat", width=Inches(4.1), keep_with_next=True)

p_step_title("Langkah 6: Mendefinisikan Foreign Table")
p_para("Mendefinisikan foreign table ft_pelanggan_barat dan ft_pelanggan_timur di db_pusat serta memverifikasi pembacaan data remote.", keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "Definisikan Foreign Table.png", "Gambar 12: Pembuatan Foreign Table dan Verifikasi Akses Data Lintas Basis Data", width=Inches(4.1), keep_with_next=False)

# ==============================================================================
# HALAMAN 5 (Gambar 13, 14, 15)
# ==============================================================================
doc.add_page_break()
p_step_title("Langkah 7: Membuat Tampilan Data Terdistribusi (View v_pelanggan_semua)")
p_para("Membuat view gabungan transparansi lokasi dengan UNION ALL dan melakukan agregasi jumlah pelanggan per wilayah.", keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "Buat Tampilan Data Terdistribusi.png", "Gambar 13: Eksekusi View Gabungan v_pelanggan_semua dan Hasil Agregasi Wilayah", width=Inches(4.1), keep_with_next=True)

p_step_title("Langkah 8: Verifikasi Fragmentasi dan Alokasi Data (Uji 1 & 2)")
p_para("Uji 1: Kelengkapan data (total 6 baris) dan Uji 2: Rekonstruksi kunci primer (menghasilkan 6 ID unik).", keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "Verifikasi Fragmentasi dan Alokasi 1.png", "Gambar 14: Uji Kelengkapan Data (Total Menghasilkan 6 Baris)", width=Inches(4.1), keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "Verifikasi Fragmentasi dan Alokasi 2.png", "Gambar 15: Uji Rekonstruksi Kunci Primer (Menghasilkan 6 ID Unik)", width=Inches(4.1), keep_with_next=False)

# ==============================================================================
# HALAMAN 6 (Gambar 16, 17, 18)
# ==============================================================================
doc.add_page_break()
p_step_title("Langkah 8: Uji Saling Lepas dan Analisis Rencana Eksekusi Pushdown")
p_para("Uji 3: Saling lepas (0 baris salah wilayah) dan Uji 4: EXPLAIN VERBOSE membuktikan filter pushdown remote SQL.", keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "Verifikasi Fragmentasi dan Alokasi 3.png", "Gambar 16: Uji Saling Lepas (Kedua Kueri Pemeriksaan Menghasilkan 0 Baris)", width=Inches(4.1), keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "Verifikasi Fragmentasi dan Alokasi 4.png", "Gambar 17: Rencana Eksekusi EXPLAIN Menampilkan Foreign Scan dan Remote SQL", width=Inches(4.1), keep_with_next=True)

p_step_title("Langkah 9: Uji Pembaharuan Data di Node Barat")
p_para("Menambahkan baris data Gilang (ID 7) pada tabel pelanggan_barat di db_barat.", keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "Uji Pembaharuan Data di Node 1.png", "Gambar 18: Penambahan Baris Data Gilang (ID 7) pada Database db_barat", width=Inches(4.1), keep_with_next=False)

# ==============================================================================
# HALAMAN 7 (Gambar 19, 20, 21)
# ==============================================================================
doc.add_page_break()
p_step_title("Langkah 9: Verifikasi Real-Time di Pusat & Uji Penolakan Constraint")
p_para("Memverifikasi pembaruan otomatis di db_pusat (total 7 baris) dan menguji penolakan data wilayah Timur oleh CHECK constraint di db_barat.", keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "Uji Pembaharuan Data di Node 2.png", "Gambar 19: db_pusat Menampilkan Gilang dan Total 7 Baris Secara Real-Time", width=Inches(4.1), keep_with_next=True)
add_image(doc, DIR_PRAKTIKUM_IMG, "Uji Pembaharuan Data di Node 3.png", "Gambar 20: Pesan Kesalahan Penolakan Data Wilayah Timur oleh CHECK Constraint", width=Inches(4.1), keep_with_next=True)

p_section_title("BAGIAN II. TUGAS PRAKTIKUM MAHASISWA (BAGIAN H)")
p_para("Studi Kasus: Sistem Distribusi Pesanan Toko Online (Fragmen pesanan_barat dan pesanan_timur).", italic=True, keep_with_next=True)
p_step_title("Langkah 1: Pembuatan Tabel & Data di Node Barat (db_barat)")
p_para("Membuat tabel pesanan_barat (CHECK wilayah='Barat', ID 101-106) dan memuat 6 transaksi sampel.", keep_with_next=True)
add_image(doc, DIR_TUGAS_IMG, "Buat Tabel & Data pada Node Barat.png", "Gambar 21: Pembuatan Tabel pesanan_barat dan Pemuatan 6 Baris Transaksi", width=Inches(4.1), keep_with_next=False)

# ==============================================================================
# HALAMAN 8 (Gambar 22, 23, 24)
# ==============================================================================
doc.add_page_break()
p_step_title("Langkah 2: Pembuatan Tabel & Data di Node Timur (db_timur)")
p_para("Membuat tabel pesanan_timur (CHECK wilayah='Timur', ID 201-206) dan memuat 6 transaksi sampel.", keep_with_next=True)
add_image(doc, DIR_TUGAS_IMG, "Buat Tabel & Data pada Node Timur.png", "Gambar 22: Pembuatan Tabel pesanan_timur dan Pemuatan 6 Baris Transaksi", width=Inches(4.1), keep_with_next=True)

p_step_title("Langkah 3: Konfigurasi FDW & View Terdistribusi di Koordinator (db_pusat)")
p_para("Mendefinisikan foreign table ft_pesanan_barat & ft_pesanan_timur, lalu menggabungkannya dalam view v_pesanan_semua.", keep_with_next=True)
add_image(doc, DIR_TUGAS_IMG, "Konfigurasi FDW & View di Koordinator.png", "Gambar 23: View Gabungan v_pesanan_semua di db_pusat (12 Baris Transaksi)", width=Inches(4.1), keep_with_next=True)

p_step_title("Penyelesaian Soal 1: Seluruh Pesanan dari Dua Node")
p_para("1a. Menampilkan seluruh 12 transaksi pesanan dari Barat dan Timur:", bold=True, keep_with_next=True)
add_code_block(doc, "SELECT id_pesanan, nama_pelanggan, wilayah, total_belanja, tanggal_pesanan FROM v_pesanan_semua ORDER BY wilayah, id_pesanan;", keep_with_next=True)
add_image(doc, DIR_TUGAS_IMG, "Tampilkan Seluruh Pesanan dan Jumlah Pesanan per Wilayah 1.png", "Gambar 24: Hasil Kueri 1a – Menampilkan Seluruh 12 Transaksi Pesanan", width=Inches(4.1), keep_with_next=False)

# ==============================================================================
# HALAMAN 9 (Gambar 25, 26 - Lebar 4.85 in, Padat & Rapi)
# Soal 1b (Agregasi Wilayah) & Soal 2 (Total Nilai Belanja)
# ==============================================================================
doc.add_page_break()
p_step_title("Penyelesaian Soal 1 (Lanjutan): Agregasi Jumlah Pesanan per Wilayah")
p_para("1b. Menghitung jumlah transaksi per wilayah menggunakan fungsi agregasi COUNT:", bold=True, keep_with_next=True)
add_code_block(doc, "SELECT wilayah, COUNT(*) AS jumlah_pesanan\nFROM v_pesanan_semua\nGROUP BY wilayah ORDER BY wilayah;", keep_with_next=True)
add_image(doc, DIR_TUGAS_IMG, "Tampilkan Seluruh Pesanan dan Jumlah Pesanan per Wilayah 2.png", "Gambar 25: Hasil Kueri 1b – Agregasi Jumlah Pesanan per Wilayah (Barat = 6, Timur = 6)", width=Inches(4.85), keep_with_next=True)
p_eval("Evaluasi: Kueri berhasil mengelompokkan 12 pesanan secara seimbang, yaitu 6 transaksi di Barat dan 6 transaksi di Timur.", keep_with_next=True)

p_step_title("Penyelesaian Soal 2: Total Nilai Belanja Setiap Wilayah")
p_para("2. Menghitung total nilai belanja (SUM) dan rata-rata belanja (AVG) per wilayah:", bold=True, keep_with_next=True)
add_code_block(doc, "SELECT wilayah, COUNT(*) AS total_transaksi,\n       SUM(total_belanja) AS total_belanja,\n       ROUND(AVG(total_belanja), 2) AS rata_rata\nFROM v_pesanan_semua\nGROUP BY wilayah ORDER BY wilayah;", keep_with_next=True)
add_image(doc, DIR_TUGAS_IMG, "Hitung Total Nilai Belanja Setiap Wilayah dengan SUM(total_belanja).png", "Gambar 26: Hasil Kueri 2 – Total Belanja (Barat: Rp 3.870.000, Timur: Rp 4.335.000)", width=Inches(4.85), keep_with_next=True)
p_eval("Evaluasi: Total omzet keseluruhan mencapai Rp 8.205.000 dengan rata-rata belanja wilayah Timur (Rp 722.500) melampaui Barat (Rp 645.000).", keep_with_next=False)

# ==============================================================================
# HALAMAN 10 (Gambar 27, 28 - Lebar 4.85 in, Padat & Rapi)
# Soal 3 Kueri (Belanja > 500rb) & Soal 3 Analisis Pushdown (EXPLAIN)
# ==============================================================================
doc.add_page_break()
p_step_title("Penyelesaian Soal 3: Pesanan dengan Total Belanja > 500.000")
p_para("3a. Menampilkan pesanan bernilai di atas Rp 500.000 yang diurutkan dari nilai terbesar:", bold=True, keep_with_next=True)
add_code_block(doc, "SELECT id_pesanan, nama_pelanggan, wilayah, total_belanja, tanggal_pesanan\nFROM v_pesanan_semua\nWHERE total_belanja > 500000\nORDER BY total_belanja DESC;", keep_with_next=True)
add_image(doc, DIR_TUGAS_IMG, "Tampilkan Pesanan dengan Total Belanja  500.000.png", "Gambar 27: Hasil Kueri 3a – 7 Transaksi Terpilih dengan Nilai Belanja > 500.000", width=Inches(4.85), keep_with_next=True)
p_eval("Evaluasi: Dari total 12 pesanan, sistem berhasil menyaring 7 transaksi bernilai tinggi (3 dari wilayah Barat dan 4 dari wilayah Timur).", keep_with_next=True)

p_step_title("Analisis Rencana Eksekusi Pushdown Predikat (EXPLAIN VERBOSE)")
p_para("3b. Memeriksa rencana eksekusi untuk membuktikan optimasi remote pushdown:", bold=True, keep_with_next=True)
add_code_block(doc, "EXPLAIN (VERBOSE)\nSELECT * FROM v_pesanan_semua\nWHERE total_belanja > 500000;", keep_with_next=True)
add_image(doc, DIR_TUGAS_IMG, "Analisis Rencana Eksekusi Pushdown.png", "Gambar 28: Hasil EXPLAIN VERBOSE – Filter Pushdown Remote SQL pada Foreign Scan", width=Inches(4.85), keep_with_next=True)
p_eval("Evaluasi: Terbukti klausul 'Remote SQL' pada Foreign Scan memuat 'WHERE total_belanja > 500000', menyaring data langsung di remote engine.", keep_with_next=False)

# ==============================================================================
# HALAMAN 11 (Gambar 29, 30 - Lebar 4.85 in, Padat & Rapi)
# Soal 4 Rekonstruksi (Jumlah Cocok & ID Unik) & Soal 4 Saling Lepas (Disjointness)
# ==============================================================================
doc.add_page_break()
p_step_title("Penyelesaian Soal 4: Pembuktian Rekonstruksi & Non-Duplikasi ID")
p_para("4a. Menguji bahwa total gabungan (UNION ALL) persis sama dan seluruh ID unik:", bold=True, keep_with_next=True)
add_code_block(doc,
    "SELECT COUNT(*) AS total_gabungan, COUNT(DISTINCT id_pesanan) AS total_id_unik,\n"
    "       (SELECT COUNT(*) FROM ft_pesanan_barat) AS barat,\n"
    "       (SELECT COUNT(*) FROM ft_pesanan_timur) AS timur,\n"
    "       CASE WHEN COUNT(*) = ((SELECT COUNT(*) FROM ft_pesanan_barat) + (SELECT COUNT(*) FROM ft_pesanan_timur))\n"
    "            AND COUNT(*) = COUNT(DISTINCT id_pesanan)\n"
    "            THEN 'TERBUKTI: Jumlah Cocok (12) & Tidak Ada ID Duplikat' ELSE 'GAGAL' END AS status\n"
    "FROM v_pesanan_semua;",
    keep_with_next=True
)
add_image(doc, DIR_TUGAS_IMG, "Buktikan Jumlah Gabungan Sama dengan Kedua Fragmen & ID Tidak Duplikat.png", "Gambar 29: Validasi Rekonstruksi – Status 'TERBUKTI: Jumlah Cocok (12) & Tidak Ada ID Duplikat'", width=Inches(4.85), keep_with_next=True)
p_eval("Evaluasi: 12 baris di view persis sama dengan 6 (Barat) + 6 (Timur) dan COUNT(DISTINCT id_pesanan) bernilai 12 tanpa duplikasi.", keep_with_next=True)

p_step_title("Pembuktian Sifat Saling Lepas (Disjointness)")
p_para("4b. Memeriksa keberadaan data anomali (wilayah silang) pada masing-masing fragmen:", bold=True, keep_with_next=True)
add_code_block(doc,
    "SELECT * FROM ft_pesanan_barat WHERE wilayah <> 'Barat';\n"
    "SELECT * FROM ft_pesanan_timur WHERE wilayah <> 'Timur';",
    keep_with_next=True
)
add_image(doc, DIR_TUGAS_IMG, "Kueri Pembuktian Saling Lepas (Disjointness).png", "Gambar 30: Validasi Saling Lepas – Menghasilkan 0 Baris (Tidak Ada Data Silang)", width=Inches(4.85), keep_with_next=True)
p_eval("Evaluasi: Kedua kueri verifikasi menghasilkan 0 rows, membuktikan bahwa fragmen Barat dan Timur saling lepas secara mutlak.", keep_with_next=False)

# ==============================================================================
# HALAMAN 12 (Soal 5 - Teks Analisis Mendalam & Tabel Ringkasan)
# ==============================================================================
doc.add_page_break()
p_step_title("Penyelesaian Soal 5: Analisis Alokasi, Keuntungan, dan Risiko Kegagalan Node")

p_para("a. Alasan Pilihan Alokasi (Horizontal Fragmentation berdasarkan 'wilayah'):", bold=True, color=C_PRIMARY)
p_para(
    "Fragmentasi horizontal berdasarkan kolom 'wilayah' dipilih karena sesuai dengan prinsip Locality of Reference (lokalitas referensi data). "
    "Pada operasional toko online/e-commerce, pesanan pelanggan di wilayah Barat akan diproses, dikemas, dan dikirimkan oleh gudang regional Barat, "
    "begitu pula sebaliknya untuk wilayah Timur. Penempatan data pada node lokal meminimalkan kebutuhan transmisi data melintasi jaringan WAN.\n"
    "Desain alokasi ini secara formal memenuhi tiga aturan kebenaran fragmentasi:\n"
    "• Completeness (Kelengkapan): Setiap pesanan pasti memiliki atribut wilayah ('Barat' atau 'Timur') sehingga tidak ada data yang tercecer.\n"
    "• Reconstruction (Rekonstruksi): Relasi global dapat dipulihkan secara utuh tanpa kehilangan data melalui operator UNION ALL.\n"
    "• Disjointness (Saling Lepas): Penerapan constraint CHECK pada tabel lokal menjamin tidak ada duplikasi data transaksi antar-node."
)

p_para("b. Keuntungan Desain Terdistribusi:", bold=True, color=C_PRIMARY)
p_para(
    "1. Peningkatan Throughput & Paralelisme: Operasi penulisan (INSERT/UPDATE pesanan) diproses secara paralel oleh dua DBMS engine independen, "
    "menghilangkan beban bottleneck terpusat.\n"
    "2. Latensi Kueri Sangat Rendah: Staf operasional cabang dapat membaca dan mengelola pesanan lokal dengan latensi minimal tanpa terhambat trafik pusat.\n"
    "3. Transparansi Lokasi: Lapisan aplikasi dan manajemen cukup mengakses satu view terpadu (v_pesanan_semua) di db_pusat seolah berada pada single-node database."
)

p_para("c. Risiko jika Salah Satu Node Tidak Tersedia (Node Failure) & Rekomendasi Solusi Produksi:", bold=True, color=C_PRIMARY)
p_para(
    "1. Kerapuhan Single Point of Failure (SPOF) pada View Terdistribusi:\n"
    "Karena view v_pesanan_semua merujuk langsung ke Foreign Table fisik melalui operator UNION ALL, kegagalan salah satu node (misalnya db_timur down atau putus jaringan) "
    "akan menyebabkan seluruh kueri yang mengakses view gabungan di db_pusat langsung gagal (mengalami exception error connection refused/timeout). "
    "Dampaknya, data pesanan wilayah Barat yang sebenarnya aktif normal tetap tidak bisa ditampilkan melalui antarmuka pusat.\n\n"
    "2. Rekomendasi Solusi & Mitigasi di Lingkungan Produksi:\n"
    "• Replikasi Data (Streaming Replication / Read Replica): Mengonfigurasi replika standby pada setiap cabang dengan mekanisme auto-failover agar node selalu tersedia.\n"
    "• Materialized View dengan Refresh Terjadwal (Caching Layer): Menggunakan snapshot data lokal di db_pusat yang di-refresh berkala. Ketika salah satu cabang padam, "
    "koordinator tetap dapat melayani kueri agregasi manajemen menggunakan data terakhir yang tersimpan (prinsip eventual consistency)."
)

# Tambahkan Tabel Ringkasan Arsitektur Distribusi di Halaman 12
p_para("Tabel Ringkasan Desain Fragmentasi dan Alokasi Sistem Toko Online:", bold=True, color=C_SECONDARY, keep_with_next=True)
tbl_sum = doc.add_table(rows=4, cols=4)
tbl_sum.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_sum.autofit = False
tbl_sum.columns[0].width = Inches(1.3)
tbl_sum.columns[1].width = Inches(1.9)
tbl_sum.columns[2].width = Inches(1.9)
tbl_sum.columns[3].width = Inches(2.1)

headers = ["Node / Basis Data", "Peran Arsitektur", "Objek & Fragmentasi", "Mekanisme Integritas / Failover"]
for i, h in enumerate(headers):
    c = tbl_sum.cell(0, i)
    set_cell_margins(c, top=20, bottom=20, left=40, right=40)
    set_cell_shading(c, "003366")
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(h)
    r.font.name = "Calibri"
    r.font.size = Pt(7.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)

data_sum = [
    ["db_barat (Node Barat)", "Pemrosesan Transaksi Regional", "Tabel pesanan_barat (6 baris, ID 101-106)", "CHECK (wilayah='Barat') / Standby Replica"],
    ["db_timur (Node Timur)", "Pemrosesan Transaksi Regional", "Tabel pesanan_timur (6 baris, ID 201-206)", "CHECK (wilayah='Timur') / Standby Replica"],
    ["db_pusat (Koordinator)", "Konsolidasi Global & Analitik", "Foreign Table + View v_pesanan_semua", "postgres_fdw / Materialized View Snapshot"]
]

for r_idx, row in enumerate(data_sum, start=1):
    prevent_row_split(tbl_sum.rows[r_idx])
    for c_idx, val in enumerate(row):
        c = tbl_sum.cell(r_idx, c_idx)
        set_cell_margins(c, top=15, bottom=15, left=40, right=40)
        set_cell_shading(c, "F6F8FA" if r_idx % 2 == 1 else "FFFFFF")
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(val)
        r.font.name = "Calibri"
        r.font.size = Pt(7.5)
        r.font.color.rgb = C_TEXT

doc.save(OUTPUT_FILE)
print(f"File successfully created: {OUTPUT_FILE}")
