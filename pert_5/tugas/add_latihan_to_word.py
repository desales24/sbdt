import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image

# 1. Pastikan folder cropped_ss dan cropped_latihan sudah siap
praktikum_folder = '/home/desales/sbdt/pert_5/dokumentasi praktikum'
latihan_folder = '/home/desales/sbdt/pert_5/dokumentasi latihan mandiri'
cropped_p_folder = '/home/desales/sbdt/pert_5/tugas/cropped_ss'
cropped_l_folder = '/home/desales/sbdt/pert_5/tugas/cropped_latihan'
os.makedirs(cropped_p_folder, exist_ok=True)
os.makedirs(cropped_l_folder, exist_ok=True)

# Cropping seragam untuk dokumentasi praktikum
for fname in os.listdir(praktikum_folder):
    if fname.endswith('.png'):
        im = Image.open(os.path.join(praktikum_folder, fname))
        c = im.crop((0, 0, 1300, 460))
        c.save(os.path.join(cropped_p_folder, fname))

# Cropping khusus sesuai bounds untuk dokumentasi latihan mandiri
latihan_crops = {
    'latihan insert a.png': (0, 0, 1300, 610),
    'latihan insert b.png': (0, 0, 1300, 630),
    'update latihan a.png': (0, 0, 1300, 770),
    'update latihan b.png': (0, 0, 1300, 800),
    'latihan node b berhenti.png': (0, 0, 1300, 450),
    'latihan node b hidup kembali.png': (0, 0, 1300, 380),
    'eksekusi a.png': (0, 0, 1300, 280),
    'eksekusi b.png': (0, 0, 1300, 320),
}
for fname, bbox in latihan_crops.items():
    p = os.path.join(latihan_folder, fname)
    if os.path.exists(p):
        im = Image.open(p)
        c = im.crop(bbox)
        c.save(os.path.join(cropped_l_folder, fname))

# Helper styling
def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=120, right=120):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="B0BEC5", sz="4", val="single"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = OxmlElement('w:tblBorders')
        for b_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
            b = OxmlElement(f'w:{b_name}')
            b.set(qn('w:val'), val)
            b.set(qn('w:sz'), sz)
            b.set(qn('w:space'), '0')
            b.set(qn('w:color'), color)
            borders.append(b)
        tblPr[0].append(borders)

doc = Document()

# Layout: Landscape A4 / Letter
section = doc.sections[0]
section.orientation = WD_ORIENT.LANDSCAPE
section.page_width = Inches(11.0)
section.page_height = Inches(8.5)
section.left_margin = Inches(0.5)
section.right_margin = Inches(0.5)
section.top_margin = Inches(0.5)
section.bottom_margin = Inches(0.5)

# ==============================================================================
# BAGIAN E: TABEL PENGAMATAN
# ==============================================================================

p_title = doc.add_paragraph()
p_title.paragraph_format.space_before = Pt(0)
p_title.paragraph_format.space_after = Pt(2)
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_t = p_title.add_run("E. Tabel Pengamatan")
r_t.font.name = "Calibri"
r_t.font.size = Pt(14)
r_t.font.bold = True
r_t.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

p_sub = doc.add_paragraph()
p_sub.paragraph_format.space_after = Pt(8)
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_sub = p_sub.add_run("Praktikum Sistem Basis Data Terdistribusi - Replikasi Multi-Master (Two-Way)")
r_sub.font.name = "Calibri"
r_sub.font.size = Pt(9.5)
r_sub.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

headers_e = ["Uji", "Perubahan", "Hasil Node A", "Hasil Node B"]
col_widths_e = [Inches(0.6), Inches(1.8), Inches(3.8), Inches(3.8)]

rows_config_e = [
    {
        "uji": "1",
        "perubahan": "INSERT 101 dari A",
        "node_a_desc": "Data 101 di-insert di Node A:",
        "node_a_img": "insert a.png",
        "node_b_desc": "Data 101 tersinkron di Node B:",
        "node_b_img": "data dari b.png"
    },
    {
        "uji": "2",
        "perubahan": "INSERT 102 dari B",
        "node_a_desc": "Data 102 tersinkron di Node A:",
        "node_a_img": "data dari a.png",
        "node_b_desc": "Data 102 di-insert di Node B:",
        "node_b_img": "insert b.png"
    },
    {
        "uji": "3",
        "perubahan": "UPDATE 101 dari A",
        "node_a_desc": "Stok 101 diupdate (20 ➔ 25) di Node A:",
        "node_a_img": "update a.png",
        "node_b_desc": "Stok 101 tersinkron (25) di Node B:",
        "node_b_img": "data update b.png"
    },
    {
        "uji": "4",
        "perubahan": "UPDATE 102 dari B",
        "node_a_desc": "Stok 102 tersinkron (12) di Node A:",
        "node_a_img": "data update a.png",
        "node_b_desc": "Stok 102 diupdate (10 ➔ 12) di Node B:",
        "node_b_img": "update b.png"
    },
    {
        "uji": "5",
        "perubahan": "DELETE 104 dari B",
        "node_a_desc": "ID 104 otomatis terhapus di Node A:",
        "node_a_img": "data delete a.png",
        "node_b_desc": "ID 104 dihapus di Node B:",
        "node_b_img": "delete b.png"
    }
]

table_e = doc.add_table(rows=len(rows_config_e) + 1, cols=4)
table_e.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(table_e)

hdr_cells_e = table_e.rows[0].cells
for i, title in enumerate(headers_e):
    hdr_cells_e[i].text = title
    hdr_cells_e[i].width = col_widths_e[i]
    set_cell_background(hdr_cells_e[i], "1B365D")
    set_cell_margins(hdr_cells_e[i], top=100, bottom=100, left=100, right=100)
    p = hdr_cells_e[i].paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

for r_idx, row_item in enumerate(rows_config_e):
    row_cells = table_e.rows[r_idx + 1].cells
    bg_color = "F9FAFC" if r_idx % 2 == 1 else "FFFFFF"

    # Col 0: Uji
    row_cells[0].width = col_widths_e[0]
    set_cell_background(row_cells[0], bg_color)
    set_cell_margins(row_cells[0], top=80, bottom=80, left=50, right=50)
    p0 = row_cells[0].paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r0 = p0.add_run(row_item["uji"])
    r0.font.name = "Calibri"
    r0.font.size = Pt(10)
    r0.font.bold = True

    # Col 1: Perubahan
    row_cells[1].width = col_widths_e[1]
    set_cell_background(row_cells[1], bg_color)
    set_cell_margins(row_cells[1], top=80, bottom=80, left=80, right=80)
    p1 = row_cells[1].paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r1 = p1.add_run(row_item["perubahan"])
    r1.font.name = "Calibri"
    r1.font.size = Pt(9.5)
    r1.font.bold = True

    # Col 2: Hasil Node A
    row_cells[2].width = col_widths_e[2]
    set_cell_background(row_cells[2], bg_color)
    set_cell_margins(row_cells[2], top=60, bottom=60, left=80, right=80)
    p2 = row_cells[2].paragraphs[0]
    p2.paragraph_format.space_after = Pt(2)
    p2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r2_desc = p2.add_run(row_item["node_a_desc"] + "\n")
    r2_desc.font.name = "Calibri"
    r2_desc.font.size = Pt(8.5)
    r2_desc.font.bold = True
    r2_desc.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    img_a_path = os.path.join(cropped_p_folder, row_item["node_a_img"])
    if os.path.exists(img_a_path):
        p2.add_run().add_picture(img_a_path, width=Inches(3.6))

    # Col 3: Hasil Node B
    row_cells[3].width = col_widths_e[3]
    set_cell_background(row_cells[3], bg_color)
    set_cell_margins(row_cells[3], top=60, bottom=60, left=80, right=80)
    p3 = row_cells[3].paragraphs[0]
    p3.paragraph_format.space_after = Pt(2)
    p3.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r3_desc = p3.add_run(row_item["node_b_desc"] + "\n")
    r3_desc.font.name = "Calibri"
    r3_desc.font.size = Pt(8.5)
    r3_desc.font.bold = True
    r3_desc.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    img_b_path = os.path.join(cropped_p_folder, row_item["node_b_img"])
    if os.path.exists(img_b_path):
        p3.add_run().add_picture(img_b_path, width=Inches(3.6))

# ==============================================================================
# PAGE BREAK UNTUK BAGIAN G: LATIHAN MANDIRI
# ==============================================================================
doc.add_page_break()

p_lm_title = doc.add_paragraph()
p_lm_title.paragraph_format.space_before = Pt(4)
p_lm_title.paragraph_format.space_after = Pt(2)
p_lm_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_lmt = p_lm_title.add_run("G. Latihan Mandiri")
r_lmt.font.name = "Calibri"
r_lmt.font.size = Pt(14)
r_lmt.font.bold = True
r_lmt.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

p_lm_sub = doc.add_paragraph()
p_lm_sub.paragraph_format.space_after = Pt(12)
p_lm_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_lms = p_lm_sub.add_run("Dokumentasi Pengujian, Bukti Eksekusi, Diagram Visual, dan Analisis Replikasi Multi-Master")
r_lms.font.name = "Calibri"
r_lms.font.size = Pt(9.5)
r_lms.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

# Helper untuk membuat section soal latihan mandiri
def add_soal_header(number_str, title_str):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    run_num = p.add_run(number_str + " ")
    run_num.font.name = "Calibri"
    run_num.font.size = Pt(11)
    run_num.font.bold = True
    run_num.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    run_txt = p.add_run(title_str)
    run_txt.font.name = "Calibri"
    run_txt.font.size = Pt(10.5)
    run_txt.font.bold = True
    run_txt.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

def add_two_column_ss_table(header_a, img_a_name, header_b, img_b_name, img_width=Inches(4.8)):
    tbl = doc.add_table(rows=2, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)
    
    col_w = Inches(4.9)
    # Header Row
    c0 = tbl.rows[0].cells[0]
    c1 = tbl.rows[0].cells[1]
    c0.width = col_w
    c1.width = col_w
    c0.text = header_a
    c1.text = header_b
    set_cell_background(c0, "2C3E50")
    set_cell_background(c1, "2C3E50")
    set_cell_margins(c0, top=80, bottom=80, left=100, right=100)
    set_cell_margins(c1, top=80, bottom=80, left=100, right=100)
    for c in [c0, c1]:
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            
    # Body Row (Images)
    b0 = tbl.rows[1].cells[0]
    b1 = tbl.rows[1].cells[1]
    b0.width = col_w
    b1.width = col_w
    set_cell_background(b0, "FAFAFA")
    set_cell_background(b1, "FAFAFA")
    set_cell_margins(b0, top=60, bottom=60, left=60, right=60)
    set_cell_margins(b1, top=60, bottom=60, left=60, right=60)
    
    p0 = b0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    path_a = os.path.join(cropped_l_folder, img_a_name)
    if os.path.exists(path_a):
        p0.add_run().add_picture(path_a, width=img_width)
        
    p1 = b1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    path_b = os.path.join(cropped_l_folder, img_b_name)
    if os.path.exists(path_b):
        p1.add_run().add_picture(path_b, width=img_width)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

# ------------------------------------------------------------------------------
# SOAL 1
# ------------------------------------------------------------------------------
add_soal_header("1.", "Penambahan Minimal 3 Produk Baru dari Node A (ID Ganjil) dan 3 Produk dari Node B (ID Genap)")
p_desc1 = doc.add_paragraph(
    "Pada Node A ditambahkan ID ganjil (105, 107, 109), dan pada Node B ditambahkan ID genap (106, 108, 110). "
    "Hasil eksekusi membuktikan kedua node saling menerima data baru secara lengkap (total 9 baris data identik)."
)
p_desc1.paragraph_format.space_after = Pt(6)
p_desc1.runs[0].font.name = "Calibri"
p_desc1.runs[0].font.size = Pt(9)

add_two_column_ss_table(
    "Node A (Port 5432) - INSERT ID Ganjil & Hasil SELECT",
    "latihan insert a.png",
    "Node B (Port 5433) - INSERT ID Genap & Hasil SELECT",
    "latihan insert b.png"
)

# ------------------------------------------------------------------------------
# SOAL 2
# ------------------------------------------------------------------------------
add_soal_header("2.", "Dua UPDATE dari Node Berbeda pada Baris Berbeda & Dokumentasi Waktu Propagasi")
p_desc2 = doc.add_paragraph(
    "Node A melakukan UPDATE ID 106 (stok = 18), dan Node B melakukan UPDATE ID 105 (stok = 10). "
    "Waktu propagasi dipantau melalui katalog pg_stat_subscription pada kolom latest_end_time:"
)
p_desc2.paragraph_format.space_after = Pt(4)
p_desc2.runs[0].font.name = "Calibri"
p_desc2.runs[0].font.size = Pt(9)

add_two_column_ss_table(
    "Node A - UPDATE ID 106 & Status pg_stat_subscription",
    "update latihan a.png",
    "Node B - UPDATE ID 105 & Status pg_stat_subscription",
    "update latihan b.png"
)

p_prop_analisis = doc.add_paragraph()
p_prop_analisis.paragraph_format.space_after = Pt(6)
p_prop_analisis.paragraph_format.line_spacing = 1.15
r_pa1 = p_prop_analisis.add_run("Dokumentasi Waktu Propagasi: ")
r_pa1.bold = True
r_pa1.font.size = Pt(9)
r_pa2 = p_prop_analisis.add_run(
    "Berdasarkan tangkapan layar monitoring pg_stat_subscription, latest_end_time pada Node B tercatat 08:11:53.794333 "
    "dan pada Node A tercatat 08:11:54.686049 (selisih ~0.89 detik). Data tersinkronisasi di kedua node secara near real-time (< 1 detik)."
)
r_pa2.font.size = Pt(9)
r_pa2.font.italic = True

# ------------------------------------------------------------------------------
# SOAL 3
# ------------------------------------------------------------------------------
add_soal_header("3.", "Simulasi Node B Berhenti Sementara, INSERT pada Node A, Hidupkan Node B, dan Amati Penyusulan Data")
p_desc3 = doc.add_paragraph(
    "Container Node B dimatikan sementara (docker stop node_b). Selama Node B mati, Node A melakukan INSERT produk ID 111 ('Smartwatch Fitness'). "
    "Replication slot pada Node A menahan WAL (active = f). Saat Node B dihidupkan kembali, proses apply worker langsung menyusul data yang tertinggal."
)
p_desc3.paragraph_format.space_after = Pt(6)
p_desc3.runs[0].font.name = "Calibri"
p_desc3.runs[0].font.size = Pt(9)

add_two_column_ss_table(
    "Node A saat Node B Berhenti - INSERT ID 111 & Slot active = f",
    "latihan node b berhenti.png",
    "Node B saat Dihidupkan Kembali - Data ID 111 Berhasil Tersusul",
    "latihan node b hidup kembali.png"
)

# ------------------------------------------------------------------------------
# SOAL 4
# ------------------------------------------------------------------------------
add_soal_header("4.", "Penjelasan Pemilihan copy_data = false untuk Tabel Awal Kosong dan Risikonya Bila Tabel Berisi Data")
p_soal4 = doc.add_paragraph()
p_soal4.paragraph_format.space_after = Pt(6)
p_soal4.paragraph_format.line_spacing = 1.15

r_s4_1 = p_soal4.add_run("a. Mengapa copy_data = false dipilih saat tabel awal kosong:\n")
r_s4_1.bold = True
r_s4_1.font.size = Pt(9)
r_s4_1_txt = p_soal4.add_run(
    "Pada saat inisialisasi awal, tabel produk pada kedua node masih kosong sehingga tidak ada data historis yang perlu disalin "
    "(initial table copy phase). Dengan menetapkan copy_data = false, subscription langsung aktif memasuki fase streaming CDC "
    "(Change Data Capture) dari WAL tanpa membuang resource komputasi dan I/O disk untuk memindai tabel kosong.\n\n"
)
r_s4_1_txt.font.size = Pt(9)

r_s4_2 = p_soal4.add_run("b. Risiko bila tabel sudah terisi data dan menggunakan copy_data = true pada replikasi dua arah:\n")
r_s4_2.bold = True
r_s4_2.font.size = Pt(9)
r_s4_2_txt = p_soal4.add_run(
    "1. Konflik Primary Key (Duplicate Key Violation): Jika kedua node sudah memiliki baris data yang sama, proses COPY awal akan gagal "
    "karena melanggar batasan unik primary key.\n"
    "2. Kerusakan Apply Worker (Crash Loop): Saat terjadi duplicate key pada fase copy_data, worker background subscription akan terus crash "
    "dan restart berulang kali, mengakibatkan replikasi macet total.\n"
    "3. Potensi Loop Data Historis: Opsi origin = none hanya menyaring streaming WAL transaksi baru, bukan operasi bulk COPY awal. "
    "Jika kedua node saling menyalin data yang sudah ada, timbul anomali penggandaan data dan konflik konsistensi."
)
r_s4_2_txt.font.size = Pt(9)

# ------------------------------------------------------------------------------
# SOAL 5 (LENGKAP DENGAN DIAGRAM VISUAL DAN SCREENSHOT)
# ------------------------------------------------------------------------------
add_soal_header("5.", "Analisis Skenario Kedua Node Menulis ID 200 Secara Bersamaan (Konflik Multi-Master)")
p_desc5 = doc.add_paragraph(
    "Uji coba riil dilakukan dengan memasukkan ID 200 di Node A ('Laptop Gaming ROG') dan ID 200 di Node B ('Laptop Gaming Legion'). "
    "Hasil eksekusi membuktikan terjadinya konflik benturan primary key secara langsung:"
)
p_desc5.paragraph_format.space_after = Pt(4)
p_desc5.runs[0].font.name = "Calibri"
p_desc5.runs[0].font.size = Pt(9)

# PENJELASAN VISUAL: DIAGRAM SEQUENCE MERMAID
p_diag_title = doc.add_paragraph()
p_diag_title.paragraph_format.space_before = Pt(4)
p_diag_title.paragraph_format.space_after = Pt(4)
r_dt = p_diag_title.add_run("Diagram Alur Konflik Penulisan Simultan (Sequence Diagram):")
r_dt.font.name = "Calibri"
r_dt.font.size = Pt(9.5)
r_dt.font.bold = True
r_dt.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

diag_path = "/home/desales/sbdt/pert_5/tugas/diagram_konflik_mermaid.png"
if os.path.exists(diag_path):
    p_diag_img = doc.add_paragraph()
    p_diag_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_diag_img.paragraph_format.space_after = Pt(8)
    p_diag_img.add_run().add_picture(diag_path, width=Inches(7.2))

# SCREENSHOT PEMBUKTIAN EKSEKUSI RIIL
p_ss_title = doc.add_paragraph()
p_ss_title.paragraph_format.space_before = Pt(4)
p_ss_title.paragraph_format.space_after = Pt(4)
r_sst = p_ss_title.add_run("Tangkapan Layar Bukti Eksekusi Riil di Terminal:")
r_sst.font.name = "Calibri"
r_sst.font.size = Pt(9.5)
r_sst.font.bold = True
r_sst.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

add_two_column_ss_table(
    "Node A - INSERT ID 200 ('Laptop Gaming ROG') [SUKSES COMMIT]",
    "eksekusi a.png",
    "Node B - INSERT ID 200 ('Laptop Gaming Legion') [ERROR: DUPLICATE KEY]",
    "eksekusi b.png"
)

p_analisis_s5 = doc.add_paragraph()
p_analisis_s5.paragraph_format.space_after = Pt(6)
p_analisis_s5.paragraph_format.line_spacing = 1.15
r_an_s5_title = p_analisis_s5.add_run("Analisis Kegagalan & Solusi Produksi:\n")
r_an_s5_title.bold = True
r_an_s5_title.font.size = Pt(9)
r_an_s5_txt = p_analisis_s5.add_run(
    "• Bukti Error: Node B menolak penulisan dengan pesan:\n"
    "  ERROR: duplicate key value violates unique constraint \"produk_pkey\"\n"
    "  DETAIL: Key (id)=(200) already exists.\n"
    "• Penyebab: PostgreSQL logical replication bawaan bersifat asinkron dan tidak dilengkapi Distributed Lock Manager (DLM) atau konsensus (seperti Raft/Paxos). "
    "Kedua node tidak saling mengunci baris saat eksekusi lokal berlangsung.\n"
    "• Solusi Produksi (Best Practice Senior DB Engineer):\n"
    "  1. UUIDv7 / Snowflake ID: Menggunakan ID acak berurutan berbasis waktu dan node identity sehingga tidak akan pernah bertabrakan lintas node.\n"
    "  2. Partisi Kepemilikan Data (Ownership Partitioning): Membatasi hak tulis berdasarkan domain/wilayah (Node A hanya menulis cabang barat, Node B cabang timur).\n"
    "  3. Mesin Active-Active Enterprise: Mengadopsi teknologi khusus seperti pgEdge/Spock atau BDR (Bi-Directional Replication) dengan resolusi konflik otomatis."
)
r_an_s5_txt.font.size = Pt(9)

output_path = "/home/desales/sbdt/pert_5/tugas/tabel_pengamatan_bagian_e.docx"
doc.save(output_path)
print("File berhasil diperbarui dengan Diagram & Latihan Mandiri:", output_path)
