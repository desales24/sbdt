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

# 1. Folder path
praktikum_folder = '/home/desales/sbdt/pert_5/dokumentasi praktikum'
latihan_folder = '/home/desales/sbdt/pert_5/dokumentasi latihan mandiri'
cropped_p_folder = '/home/desales/sbdt/pert_5/tugas/cropped_ss'
cropped_l_folder = '/home/desales/sbdt/pert_5/tugas/cropped_latihan'
os.makedirs(cropped_p_folder, exist_ok=True)
os.makedirs(cropped_l_folder, exist_ok=True)

# Crop images praktikum
for fname in os.listdir(praktikum_folder):
    if fname.endswith('.png'):
        im = Image.open(os.path.join(praktikum_folder, fname))
        c = im.crop((0, 0, 1300, 460))
        c.save(os.path.join(cropped_p_folder, fname))

# Crop images latihan mandiri
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

diag_seq_path = '/home/desales/sbdt/pert_5/tugas/diagram_konflik_mermaid.png'
diag_arch_path = '/home/desales/sbdt/pert_5/tugas/diagram_arsitektur_mermaid.png'

# Helper styling
def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="BDC3C7", sz="4", val="single"):
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

# Layout: Landscape A4 / Letter (11.0 x 8.5 in)
section = doc.sections[0]
section.orientation = WD_ORIENT.LANDSCAPE
section.page_width = Inches(11.0)
section.page_height = Inches(8.5)
section.left_margin = Inches(0.5)
section.right_margin = Inches(0.5)
section.top_margin = Inches(0.6)
section.bottom_margin = Inches(0.6)

# HAPUS HEADER DAN FOOTER (Sesuai instruksi: tidak usah di berikan footer dan juga header)
section.header.is_linked_to_previous = False
for p in section.header.paragraphs:
    p.text = ""
section.footer.is_linked_to_previous = False
for p in section.footer.paragraphs:
    p.text = ""

# Helper penomoran lurus dan sejajar (True Tab-Stop Hanging Indent)
def add_aligned_list_item(doc, marker_str, title_str, body_str):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.50)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    p.paragraph_format.tab_stops.add_tab_stop(Inches(0.50))
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    
    r_n = p.add_run(marker_str + "\t")
    r_n.font.name = "Calibri"
    r_n.font.size = Pt(9.5)
    r_n.font.bold = True
    r_n.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    if title_str:
        sep = " " if title_str.endswith(":") else ": "
        r_t = p.add_run(title_str + sep)
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(9.5)
        r_t.font.bold = True
        r_t.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        
    r_b = p.add_run(body_str)
    r_b.font.name = "Calibri"
    r_b.font.size = Pt(9)
    r_b.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    return p

# ==============================================================================
# COVER & IDENTITAS LAPORAN
# ==============================================================================
p_inst = doc.add_paragraph()
p_inst.paragraph_format.space_before = Pt(4)
p_inst.paragraph_format.space_after = Pt(2)
p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_ins = p_inst.add_run("UNIVERSITAS ESA UNGGUL\nFAKULTAS ILMU KOMPUTER — PROGRAM STUDI TEKNIK INFORMATIKA")
r_ins.font.name = "Calibri"
r_ins.font.size = Pt(11)
r_ins.font.bold = True
r_ins.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

p_main_title = doc.add_paragraph()
p_main_title.paragraph_format.space_before = Pt(4)
p_main_title.paragraph_format.space_after = Pt(2)
p_main_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_mt = p_main_title.add_run("LAPORAN PRAKTIKUM BASIS DATA TERDISTRIBUSI")
r_mt.font.name = "Calibri"
r_mt.font.size = Pt(16)
r_mt.font.bold = True
r_mt.font.color.rgb = RGBColor(0x0E, 0x3A, 0x6C)

p_sub_title = doc.add_paragraph()
p_sub_title.paragraph_format.space_before = Pt(0)
p_sub_title.paragraph_format.space_after = Pt(8)
p_sub_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_st = p_sub_title.add_run("PERTEMUAN 5: REPLIKASI MULTI-MASTER (TWO-WAY LOGICAL REPLICATION) POSTGRESQL 16")
r_st.font.name = "Calibri"
r_st.font.size = Pt(12)
r_st.font.bold = True
r_st.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)

tbl_meta = doc.add_table(rows=1, cols=2)
tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(tbl_meta, color="BDC3C7", sz="4")

col_w_m = Inches(5.0)
c_m0 = tbl_meta.rows[0].cells[0]
c_m1 = tbl_meta.rows[0].cells[1]
c_m0.width = col_w_m
c_m1.width = col_w_m
set_cell_background(c_m0, "F8F9FA")
set_cell_background(c_m1, "F8F9FA")
set_cell_margins(c_m0, top=90, bottom=90, left=110, right=110)
set_cell_margins(c_m1, top=90, bottom=90, left=110, right=110)

p_id = c_m0.paragraphs[0]
p_id.paragraph_format.line_spacing = 1.15
r_id_t = p_id.add_run("📋 IDENTITAS MATA KULIAH & PRAKTIKAN\n")
r_id_t.bold = True
r_id_t.font.size = Pt(9.5)
r_id_t.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
r_id_c = p_id.add_run(
    "• Mata Kuliah : Sistem Basis Data Terdistribusi\n"
    "• Program Studi: S1 Teknik Informatika\n"
    "• Dosen Pengampu: Ranny Meilisa, S.Kom., M.Pd.T.\n"
    "• Praktikan    : Desales (sbdt/pert_5)\n"
    "• Semester / TA: Ganjil / 2026"
)
r_id_c.font.size = Pt(9)

p_env = c_m1.paragraphs[0]
p_env.paragraph_format.line_spacing = 1.15
r_env_t = p_env.add_run("⚙️ KONFIGURASI LINGKUNGAN UJI (DOCKER)\n")
r_env_t.bold = True
r_env_t.font.size = Pt(9.5)
r_env_t.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
r_env_c = p_env.add_run(
    "• Engine DBMS  : PostgreSQL 16-alpine (Multi-Container)\n"
    "• Node A       : Port Host 5432 (Internal 5432, db_multimaster)\n"
    "• Node B       : Port Host 5433 (Internal 5432, db_multimaster)\n"
    "• Network      : Docker Bridge (db_network)\n"
    "• Mode Replikasi: Two-Way Logical Replication (origin = none)"
)
r_env_c.font.size = Pt(9)

p_space = doc.add_paragraph()
p_space.paragraph_format.space_before = Pt(0)
p_space.paragraph_format.space_after = Pt(4)

# ==============================================================================
# BAGIAN E: TABEL PENGAMATAN
# ==============================================================================
p_sec_e = doc.add_paragraph()
p_sec_e.paragraph_format.left_indent = Inches(0)
p_sec_e.paragraph_format.space_before = Pt(4)
p_sec_e.paragraph_format.space_after = Pt(2)
r_se = p_sec_e.add_run("E. Tabel Pengamatan Praktikum")
r_se.font.name = "Calibri"
r_se.font.size = Pt(13)
r_se.font.bold = True
r_se.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

p_desc_e = doc.add_paragraph(
    "Tabel di bawah ini merupakan hasil pencatatan dan pembuktian sinkronisasi data dua arah antara Node A dan Node B "
    "sesuai struktur baku tabel Bagian E modul praktikum. Masing-masing sel menyematkan bukti tangkapan layar terminal psql asli."
)
p_desc_e.paragraph_format.left_indent = Inches(0)
p_desc_e.paragraph_format.space_after = Pt(6)
p_desc_e.paragraph_format.line_spacing = 1.15
p_desc_e.runs[0].font.name = "Calibri"
p_desc_e.runs[0].font.size = Pt(9.5)

headers_e = ["Uji", "Perubahan", "Hasil Node A", "Hasil Node B"]
col_widths_e = [Inches(0.6), Inches(1.8), Inches(3.8), Inches(3.8)]

rows_config_e = [
    {
        "uji": "1",
        "perubahan": "INSERT 101 dari A\n(101, 'Keyboard', 20, 'A')",
        "node_a_desc": "Data 101 di-insert di Node A:",
        "node_a_img": "insert a.png",
        "node_b_desc": "Data 101 tersinkron di Node B:",
        "node_b_img": "data dari b.png"
    },
    {
        "uji": "2",
        "perubahan": "INSERT 102 dari B\n(102, 'Monitor', 10, 'B')",
        "node_a_desc": "Data 102 tersinkron di Node A:",
        "node_a_img": "data dari a.png",
        "node_b_desc": "Data 102 di-insert di Node B:",
        "node_b_img": "insert b.png"
    },
    {
        "uji": "3",
        "perubahan": "UPDATE 101 dari A\n(Stok 101 diubah jadi 25)",
        "node_a_desc": "Stok 101 diupdate (20 ➔ 25) di Node A:",
        "node_a_img": "update a.png",
        "node_b_desc": "Stok 101 tersinkron (25) di Node B:",
        "node_b_img": "data update b.png"
    },
    {
        "uji": "4",
        "perubahan": "UPDATE 102 dari B\n(Stok 102 diubah jadi 12)",
        "node_a_desc": "Stok 102 tersinkron (12) di Node A:",
        "node_a_img": "data update a.png",
        "node_b_desc": "Stok 102 diupdate (10 ➔ 12) di Node B:",
        "node_b_img": "update b.png"
    },
    {
        "uji": "5",
        "perubahan": "DELETE 104 dari B\n(Hapus produk ID 104)",
        "node_a_desc": "ID 104 otomatis terhapus di Node A:",
        "node_a_img": "data delete a.png",
        "node_b_desc": "ID 104 dihapus di Node B:",
        "node_b_img": "delete b.png"
    }
]

tbl_e = doc.add_table(rows=len(rows_config_e) + 1, cols=4)
tbl_e.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(tbl_e, color="BDC3C7", sz="4")

for idx, text in enumerate(headers_e):
    c = tbl_e.rows[0].cells[idx]
    c.width = col_widths_e[idx]
    c.text = text
    set_cell_background(c, "1B365D")
    set_cell_margins(c, top=80, bottom=80, left=80, right=80)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

for row_idx, rcfg in enumerate(rows_config_e, start=1):
    row_cells = tbl_e.rows[row_idx].cells
    for i in range(4):
        row_cells[i].width = col_widths_e[i]
        set_cell_margins(row_cells[i], top=50, bottom=50, left=50, right=50)
        row_cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    # Kolom 0: Uji
    c0 = row_cells[0]
    c0.text = rcfg["uji"]
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.runs[0].font.name = "Calibri"
    p0.runs[0].font.size = Pt(10)
    p0.runs[0].font.bold = True
    p0.runs[0].font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    # Kolom 1: Perubahan
    c1 = row_cells[1]
    c1.text = rcfg["perubahan"]
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for r in p1.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.bold = True

    # Kolom 2: Hasil Node A
    c2 = row_cells[2]
    p2 = c2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_after = Pt(2)
    r2_t = p2.add_run(rcfg["node_a_desc"])
    r2_t.font.name = "Calibri"
    r2_t.font.size = Pt(8.5)
    r2_t.font.italic = True
    r2_t.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    img_a_path = os.path.join(cropped_p_folder, rcfg["node_a_img"])
    if os.path.exists(img_a_path):
        p2_img = c2.add_paragraph()
        p2_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2_img.paragraph_format.space_after = Pt(0)
        p2_img.add_run().add_picture(img_a_path, width=Inches(3.6))

    # Kolom 3: Hasil Node B
    c3 = row_cells[3]
    p3 = c3.paragraphs[0]
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.paragraph_format.space_after = Pt(2)
    r3_t = p3.add_run(rcfg["node_b_desc"])
    r3_t.font.name = "Calibri"
    r3_t.font.size = Pt(8.5)
    r3_t.font.italic = True
    r3_t.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    img_b_path = os.path.join(cropped_p_folder, rcfg["node_b_img"])
    if os.path.exists(img_b_path):
        p3_img = c3.add_paragraph()
        p3_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p3_img.paragraph_format.space_after = Pt(0)
        p3_img.add_run().add_picture(img_b_path, width=Inches(3.6))

# ==============================================================================
# BAGIAN G: LATIHAN MANDIRI
# ==============================================================================
doc.add_page_break()

p_sec_g = doc.add_paragraph()
p_sec_g.paragraph_format.left_indent = Inches(0)
p_sec_g.paragraph_format.space_before = Pt(4)
p_sec_g.paragraph_format.space_after = Pt(2)
r_sg = p_sec_g.add_run("G. Latihan Mandiri")
r_sg.font.name = "Calibri"
r_sg.font.size = Pt(13)
r_sg.font.bold = True
r_sg.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

p_desc_g = doc.add_paragraph(
    "Bagian ini mendokumentasikan pelaksanaan 5 skenario latihan mandiri mencakup penambahan data lintas node, "
    "pengukuran latensi propagasi, uji ketahanan node mati (failover/catch-up), analisis parameter, dan pengujian konflik penulisan simultan."
)
p_desc_g.paragraph_format.left_indent = Inches(0)
p_desc_g.paragraph_format.space_after = Pt(8)
p_desc_g.paragraph_format.line_spacing = 1.15
p_desc_g.runs[0].font.name = "Calibri"
p_desc_g.runs[0].font.size = Pt(9.5)

# DIAGRAM ARSITEKTUR
if os.path.exists(diag_arch_path):
    p_arch_box = doc.add_paragraph()
    p_arch_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_arch_box.paragraph_format.space_before = Pt(2)
    p_arch_box.paragraph_format.space_after = Pt(4)
    r_ab_t = p_arch_box.add_run("Gambar 1: Diagram Arsitektur Jaringan Replikasi Dua Arah (Node A ⇄ Node B)")
    r_ab_t.font.name = "Calibri"
    r_ab_t.font.size = Pt(9.5)
    r_ab_t.font.bold = True
    r_ab_t.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_arch_img = doc.add_paragraph()
    p_arch_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_arch_img.paragraph_format.space_after = Pt(8)
    p_arch_img.add_run().add_picture(diag_arch_path, width=Inches(8.5))

def add_soal_header(number_str, title_str):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
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

def add_two_column_ss_table(header_a, img_a_name, header_b, img_b_name, img_width=Inches(4.88)):
    tbl = doc.add_table(rows=2, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, color="BDC3C7", sz="4")
    
    col_w = Inches(5.0)
    # Header Row
    c0 = tbl.rows[0].cells[0]
    c1 = tbl.rows[0].cells[1]
    c0.width = col_w
    c1.width = col_w
    c0.text = header_a
    c1.text = header_b
    set_cell_background(c0, "2C3E50")
    set_cell_background(c1, "2C3E50")
    set_cell_margins(c0, top=60, bottom=60, left=80, right=80)
    set_cell_margins(c1, top=60, bottom=60, left=80, right=80)
    for c in [c0, c1]:
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            
    # Body Row (Images)
    b0 = tbl.rows[1].cells[0]
    b1 = tbl.rows[1].cells[1]
    b0.width = col_w
    b1.width = col_w
    set_cell_background(b0, "FAFAFA")
    set_cell_background(b1, "FAFAFA")
    set_cell_margins(b0, top=40, bottom=40, left=40, right=40)
    set_cell_margins(b1, top=40, bottom=40, left=40, right=40)
    
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
        
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

# SOAL 1
add_soal_header("1.", "Penambahan Minimal 3 Produk Baru dari Node A (ID Ganjil) dan Node B (ID Genap)")
p_desc1 = doc.add_paragraph(
    "Pada Node A ditambahkan ID ganjil (105: Webcam, 107: Microphone, 109: Speaker). "
    "Pada Node B ditambahkan ID genap (106: Mechanical Keyboard, 108: Mousepad, 110: USB Hub). "
    "Tangkapan layar di bawah ini membuktikan kedua node saling menerima seluruh data tersebut:"
)
p_desc1.paragraph_format.left_indent = Inches(0)
p_desc1.paragraph_format.space_after = Pt(4)
p_desc1.paragraph_format.line_spacing = 1.15
p_desc1.runs[0].font.name = "Calibri"
p_desc1.runs[0].font.size = Pt(9.5)

add_two_column_ss_table(
    "Node A — INSERT ID 105, 107, 109 (Menerima ID 106, 108, 110 dari B)",
    "latihan insert a.png",
    "Node B — INSERT ID 106, 108, 110 (Menerima ID 105, 107, 109 dari A)",
    "latihan insert b.png"
)

# SOAL 2
add_soal_header("2.", "Dua UPDATE dari Node Berbeda pada Baris Berbeda & Dokumentasi Latensi Propagasi")
p_desc2 = doc.add_paragraph(
    "Node A mengupdate stok ID 106 (20 ➔ 18), dan Node B mengupdate stok ID 105 (15 ➔ 10). "
    "Waktu commit dan propagasi diverifikasi melalui kueri pg_stat_subscription_stats:"
)
p_desc2.paragraph_format.left_indent = Inches(0)
p_desc2.paragraph_format.space_after = Pt(4)
p_desc2.paragraph_format.line_spacing = 1.15
p_desc2.runs[0].font.name = "Calibri"
p_desc2.runs[0].font.size = Pt(9.5)

add_two_column_ss_table(
    "Node A — UPDATE ID 106 Stok 18 & Sinkronisasi ID 105 Stok 10",
    "update latihan a.png",
    "Node B — UPDATE ID 105 Stok 10 & Sinkronisasi ID 106 Stok 18",
    "update latihan b.png"
)

p_an2 = doc.add_paragraph()
p_an2.paragraph_format.left_indent = Inches(0)
p_an2.paragraph_format.space_before = Pt(2)
p_an2.paragraph_format.space_after = Pt(6)
p_an2.paragraph_format.line_spacing = 1.15
r_pa1 = p_an2.add_run("Dokumentasi Latensi Propagasi: ")
r_pa1.font.bold = True
r_pa1.font.size = Pt(9)
r_pa1.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
r_pa2 = p_an2.add_run(
    "Nilai latest_end_time pada Node B tercatat 08:11:53.794333 dan Node A pada 08:11:54.606992 (selisih ~0.81 detik). "
    "Hal ini menunjukkan bahwa replikasi asinkron berjalan secara near real-time (< 1 detik) di jaringan lokal Docker."
)
r_pa2.font.size = Pt(9)
r_pa2.font.italic = True

# SOAL 3
add_soal_header("3.", "Simulasi Node B Berhenti Sementara, INSERT pada Node A, Hidupkan Node B, dan Amati Penyusulan Data")
p_desc3 = doc.add_paragraph(
    "Container Node B dihentikan (docker stop node_b). Selama Node B mati, Node A melakukan INSERT produk ID 111 ('Smartwatch Fitness'). "
    "Replication slot pada Node A menahan berkas WAL (active = f). Saat Node B dihidupkan kembali, proses catch-up berhasil menyusul data:"
)
p_desc3.paragraph_format.left_indent = Inches(0)
p_desc3.paragraph_format.space_after = Pt(4)
p_desc3.paragraph_format.line_spacing = 1.15
p_desc3.runs[0].font.name = "Calibri"
p_desc3.runs[0].font.size = Pt(9.5)

add_two_column_ss_table(
    "Node A saat Node B Berhenti — INSERT ID 111 & Slot active = f",
    "latihan node b berhenti.png",
    "Node B saat Dihidupkan Kembali — Data ID 111 Berhasil Tersusul",
    "latihan node b hidup kembali.png"
)

# SOAL 4
add_soal_header("4.", "Penjelasan Pemilihan copy_data = false untuk Tabel Awal Kosong dan Risikonya Bila Tabel Berisi Data")

p_s4_head_a = doc.add_paragraph()
p_s4_head_a.paragraph_format.left_indent = Inches(0)
p_s4_head_a.paragraph_format.space_before = Pt(3)
p_s4_head_a.paragraph_format.space_after = Pt(2)
r_s4_ha = p_s4_head_a.add_run("a. Mengapa copy_data = false Dipilih Saat Tabel Awal Kosong:")
r_s4_ha.bold = True
r_s4_ha.font.size = Pt(9.5)
r_s4_ha.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

p_s4_txt_a = doc.add_paragraph(
    "Karena kedua tabel pada awalnya kosong, tidak ada data historis yang perlu disalin awal (initial table copy). "
    "Opsi copy_data = false membuat subscription langsung aktif memasuki fase streaming CDC (Change Data Capture) "
    "dari transaksi baru WAL, menghemat resource I/O dan mempercepat inisialisasi."
)
p_s4_txt_a.paragraph_format.left_indent = Inches(0)
p_s4_txt_a.paragraph_format.space_after = Pt(4)
p_s4_txt_a.paragraph_format.line_spacing = 1.15
p_s4_txt_a.runs[0].font.name = "Calibri"
p_s4_txt_a.runs[0].font.size = Pt(9)

p_s4_head_b = doc.add_paragraph()
p_s4_head_b.paragraph_format.left_indent = Inches(0)
p_s4_head_b.paragraph_format.space_before = Pt(4)
p_s4_head_b.paragraph_format.space_after = Pt(2)
r_s4_hb = p_s4_head_b.add_run("b. Risiko Bila Tabel Sudah Terisi Data dan Diset copy_data = true pada Replikasi Dua Arah:")
r_s4_hb.bold = True
r_s4_hb.font.size = Pt(9.5)
r_s4_hb.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

add_aligned_list_item(
    doc,
    "1.",
    "Pelanggaran Batasan Kunci (Duplicate Key Violation)",
    "Jika kedua node sudah memiliki data dengan ID yang sama, proses COPY massal awal akan gagal bentrok."
)
add_aligned_list_item(
    doc,
    "2.",
    "Kerusakan Apply Worker (Crash Loop)",
    "Saat terjadi duplicate key pada fase copy_data, worker background subscription akan terus crash dan restart, menghentikan seluruh proses replikasi."
)
add_aligned_list_item(
    doc,
    "3.",
    "Potensi Loop Data Historis",
    "Opsi origin = none hanya menyaring transaksi streaming WAL baru, bukan proses bulk COPY awal, sehingga berisiko terjadi duplikasi data timbal balik."
)

# SOAL 5
add_soal_header("5.", "Analisis Skenario Kedua Node Menulis ID 200 Secara Bersamaan (Konflik Multi-Master)")
p_desc5 = doc.add_paragraph(
    "Uji coba riil dilakukan dengan menuliskan ID 200 di Node A ('Laptop Gaming ROG') dan ID 200 di Node B ('Laptop Gaming Legion'). "
    "Hasil eksekusi membuktikan terjadinya konflik benturan primary key secara langsung:"
)
p_desc5.paragraph_format.left_indent = Inches(0)
p_desc5.paragraph_format.space_after = Pt(4)
p_desc5.paragraph_format.line_spacing = 1.15
p_desc5.runs[0].font.name = "Calibri"
p_desc5.runs[0].font.size = Pt(9.5)

if os.path.exists(diag_seq_path):
    p_diag_box = doc.add_paragraph()
    p_diag_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_diag_box.paragraph_format.space_before = Pt(2)
    p_diag_box.paragraph_format.space_after = Pt(4)
    r_db_t = p_diag_box.add_run("Gambar 2: Diagram Urutan (Sequence Diagram) Alur Benturan Penulisan Simultan ID 200")
    r_db_t.font.name = "Calibri"
    r_db_t.font.size = Pt(9.5)
    r_db_t.font.bold = True
    r_db_t.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_diag_img = doc.add_paragraph()
    p_diag_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_diag_img.paragraph_format.space_after = Pt(8)
    p_diag_img.add_run().add_picture(diag_seq_path, width=Inches(8.5))

add_two_column_ss_table(
    "Node A — INSERT ID 200 ('Laptop Gaming ROG') [SUKSES COMMIT]",
    "eksekusi a.png",
    "Node B — INSERT ID 200 ('Laptop Gaming Legion') [ERROR: DUPLICATE KEY]",
    "eksekusi b.png"
)

p_an_s5_head = doc.add_paragraph()
p_an_s5_head.paragraph_format.left_indent = Inches(0)
p_an_s5_head.paragraph_format.space_before = Pt(4)
p_an_s5_head.paragraph_format.space_after = Pt(2)
r_ash = p_an_s5_head.add_run("Analisis Kegagalan & Solusi Produksi:")
r_ash.bold = True
r_ash.font.size = Pt(9.5)
r_ash.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

add_aligned_list_item(
    doc,
    "1.",
    "Bukti Error di Node B",
    "ERROR: duplicate key value violates unique constraint \"produk_pkey\" DETAIL: Key (id)=(200) already exists."
)
add_aligned_list_item(
    doc,
    "2.",
    "Akar Penyebab",
    "Replikasi logis PostgreSQL bekerja secara asinkron tanpa Distributed Lock Manager (DLM) atau protokol konsensus (Raft/Paxos). Transaksi lokal di-commit secara independen tanpa koordinasi instan ke node lain."
)
add_aligned_list_item(
    doc,
    "3.",
    "Solusi Rekayasa di Industri",
    "1) Mengadopsi UUIDv7 (kunci unik 128-bit berurutan waktu); 2) Partisi kepemilikan data (Data Ownership) per cabang wilayah; atau 3) Mengadopsi mesin active-active enterprise seperti pgEdge/Spock atau EDB BDR."
)

# ==============================================================================
# BAGIAN H: EVALUASI
# ==============================================================================
doc.add_page_break()

p_sec_h = doc.add_paragraph()
p_sec_h.paragraph_format.left_indent = Inches(0)
p_sec_h.paragraph_format.space_before = Pt(4)
p_sec_h.paragraph_format.space_after = Pt(2)
r_sh = p_sec_h.add_run("H. Evaluasi")
r_sh.font.name = "Calibri"
r_sh.font.size = Pt(13)
r_sh.font.bold = True
r_sh.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

p_desc_h = doc.add_paragraph(
    "Bagian ini berisi jawaban komprehensif atas 5 pertanyaan evaluasi konseptual mengenai karakteristik, mekanisme kerja, "
    "dan batasan arsitektural replikasi multi-master pada PostgreSQL 16+."
)
p_desc_h.paragraph_format.left_indent = Inches(0)
p_desc_h.paragraph_format.space_after = Pt(8)
p_desc_h.paragraph_format.line_spacing = 1.15
p_desc_h.runs[0].font.name = "Calibri"
p_desc_h.runs[0].font.size = Pt(9.5)

def add_eval_header(number_str, title_str):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
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

# EVALUASI 1
add_eval_header("1.", "Apa Perbedaan Replikasi Primary–Replica dengan Replikasi Two-Way?")

p_ev1_intro = doc.add_paragraph(
    "Perbandingan komprehensif antara arsitektur replikasi konvensional (Primary-Replica) "
    "dengan replikasi dua arah (Two-Way / Multi-Master) dirangkum pada tabel berikut:"
)
p_ev1_intro.paragraph_format.left_indent = Inches(0)
p_ev1_intro.paragraph_format.space_after = Pt(4)
p_ev1_intro.paragraph_format.line_spacing = 1.15
p_ev1_intro.runs[0].font.name = "Calibri"
p_ev1_intro.runs[0].font.size = Pt(9.5)

tbl_ev1 = doc.add_table(rows=6, cols=3)
tbl_ev1.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(tbl_ev1, color="BDC3C7", sz="4")

ev1_widths = [Inches(2.0), Inches(4.0), Inches(4.0)]
ev1_headers = ["Kriteria Perbandingan", "Replikasi Primary–Replica (Satu Arah)", "Replikasi Two-Way (Dua Arah / Multi-Master)"]

for idx, text in enumerate(ev1_headers):
    c = tbl_ev1.rows[0].cells[idx]
    c.width = ev1_widths[idx]
    c.text = text
    set_cell_background(c, "1B365D")
    set_cell_margins(c, top=80, bottom=80, left=90, right=90)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

ev1_rows_data = [
    [
        "Arah Aliran Replikasi",
        "Satu arah (Unidirectional): Data hanya mengalir dari Primary ke Replica.",
        "Dua arah (Bidirectional): Kedua node saling bertindak sebagai publisher sekaligus subscriber."
    ],
    [
        "Hak Operasi Tulis (Write)",
        "Terpusat: Hanya node Primary yang menerima INSERT, UPDATE, DELETE. Replica berstatus Read-Only.",
        "Terdistribusi: Kedua node (Node A & Node B) sama-sama dapat menerima operasi tulis lokal."
    ],
    [
        "Risiko Konflik Data",
        "Nol: Karena hanya ada satu sumber kebenaran tulis, tidak ada konflik tabrakan data.",
        "Tinggi: Rentan terjadi tabrakan primary key dan benturan update jika baris yang sama diubah simultan."
    ],
    [
        "Pencegahan Looping Data",
        "Tidak diperlukan, karena aliran data tidak pernah memantul kembali.",
        "Wajib: Memerlukan mekanisme pemutus perulangan tak terbatas (seperti opsi origin = none)."
    ],
    [
        "Kasus Penggunaan Ideal",
        "Beban kerja Read-Heavy, pelaporan analitik terpisah, dan ketersediaan tinggi (High Availability failover).",
        "Sistem multi-cabang regional yang menuntut transaksi tulis lokal instan tanpa menunggu latensi WAN."
    ]
]

for r_i, r_data in enumerate(ev1_rows_data):
    cells = tbl_ev1.rows[r_i + 1].cells
    bg = "F9FAFC" if r_i % 2 == 1 else "FFFFFF"
    for c_i, val in enumerate(r_data):
        cells[c_i].width = ev1_widths[c_i]
        cells[c_i].text = val
        set_cell_background(cells[c_i], bg)
        set_cell_margins(cells[c_i], top=50, bottom=50, left=70, right=70)
        p = cells[c_i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(8.5)
            if c_i == 0:
                run.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(4)

# EVALUASI 2
add_eval_header("2.", "Jelaskan Fungsi Publication, Subscription, dan Replication Slot!")

add_aligned_list_item(
    doc,
    "a.",
    "PUBLICATION (di sisi Publisher / Node Pengirim)",
    "Komponen yang mendefinisikan himpunan tabel dan perubahan data yang akan diekspor/dipublikasikan ke node luar. "
    "Publication menyaring operasi SQL yang diizinkan (publish = 'insert, update, delete') langsung dari aliran Write-Ahead Log (WAL) "
    "sebelum ditransmisikan oleh proses sender worker."
)
add_aligned_list_item(
    doc,
    "b.",
    "SUBSCRIPTION (di sisi Subscriber / Node Penerima)",
    "Komponen di node penerima yang berlangganan ke publication pada node pengirim. Subscription menyimpan informasi koneksi jaringan "
    "(host, port, kredensial autentikasi), menginisialisasi proses background apply worker, menerima stream data perubahan, "
    "dan mengeksekusikannya ke tabel lokal penerima sesuai urutan transaksi."
)
add_aligned_list_item(
    doc,
    "c.",
    "REPLICATION SLOT (di sisi Publisher)",
    "Fitur keandalan pada publisher yang mencatat posisi Log Sequence Number (LSN) terakhir yang telah dikonfirmasi diterima oleh subscriber. "
    "Replication slot menjamin bahwa segmen berkas WAL yang belum dikonsumsi oleh subscriber tidak akan pernah dihapus oleh checkpoint publisher, "
    "sehingga mencegah kehilangan data (zero data loss) saat subscriber mengalami downtime atau gangguan jaringan."
)

doc.add_paragraph().paragraph_format.space_after = Pt(4)

# EVALUASI 3
add_eval_header("3.", "Mengapa Opsi origin = none Relevan untuk Replikasi Dua Arah pada PostgreSQL 16+?")

add_aligned_list_item(
    doc,
    "a.",
    "Masalah Circular Looping Replikasi",
    "Pada arsitektur replikasi multi-master dua arah tanpa penanda asal transaksi, terjadi masalah fatal: saat Node A mengirim data ke Node B, "
    "apply worker di Node B memasukkan data tersebut ke tabel lokal. Mesin PostgreSQL Node B secara default menganggap operasi tersebut sebagai "
    "transaksi lokal baru, lalu memublikasikannya kembali ke Node A. Node A kemudian menerimanya dan memantulkannya kembali ke Node B, "
    "menciptakan infinite circular loop yang menyebabkan pemborosan bandwidth, lonjakan CPU, dan crash pada database."
)
add_aligned_list_item(
    doc,
    "b.",
    "Peran Solutif origin = none (Fitur Baru PostgreSQL 16+)",
    "Opsi WITH (origin = none) pada perintah CREATE SUBSCRIPTION menginstruksikan PostgreSQL untuk hanya mereplikasi transaksi yang murni "
    "berasal dari node lokal publisher (transaksi yang tidak memiliki replication origin luar). Ketika Node B menerima data dari Node A, "
    "transaksi tersebut otomatis diberi label origin 'sub_from_a'. Akibatnya, subscription Node A (yang mengambil data dari Node B) "
    "akan otomatis mengabaikan transaksi tersebut karena origin-nya bukan murni lokal Node B. Ini secara elegan memutus rantai looping."
)

doc.add_paragraph().paragraph_format.space_after = Pt(4)

# EVALUASI 4: STRUKTUR PENOMORAN RAPI, LURUS DAN SEJAJAR
add_eval_header("4.", "Apa Penyebab Konflik Primary Key dan Bagaimana Strategi Pencegahannya?")

p_ev4_intro = doc.add_paragraph()
p_ev4_intro.paragraph_format.left_indent = Inches(0)
p_ev4_intro.paragraph_format.space_before = Pt(2)
p_ev4_intro.paragraph_format.space_after = Pt(2)
r_ev4_in = p_ev4_intro.add_run("Akar Penyebab Konflik:")
r_ev4_in.bold = True
r_ev4_in.font.size = Pt(9.5)
r_ev4_in.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

p_ev4_cause = doc.add_paragraph(
    "Replikasi logis PostgreSQL bersifat asinkron (asynchronous). Node A dan Node B memproses transaksi secara independen tanpa distributed lock instan. "
    "Jika Node A dan Node B memasukkan baris baru dengan nilai primary key yang sama (misalnya ID 200) secara bersamaan, transaksi di kedua node sukses "
    "commit lokal. Namun, begitu aliran WAL tiba di node lawan, apply worker akan menabrak constraint unik tabel dan melempar error duplicate key, "
    "yang menyebabkan apply worker berhenti (halt)."
)
p_ev4_cause.paragraph_format.left_indent = Inches(0)
p_ev4_cause.paragraph_format.space_after = Pt(4)
p_ev4_cause.paragraph_format.line_spacing = 1.15
p_ev4_cause.runs[0].font.name = "Calibri"
p_ev4_cause.runs[0].font.size = Pt(9.5)

p_ev4_sol_head = doc.add_paragraph()
p_ev4_sol_head.paragraph_format.left_indent = Inches(0)
p_ev4_sol_head.paragraph_format.space_before = Pt(4)
p_ev4_sol_head.paragraph_format.space_after = Pt(2)
r_ev4_sh = p_ev4_sol_head.add_run("Strategi Pencegahan Terbaik (Engineering Best Practices):")
r_ev4_sh.bold = True
r_ev4_sh.font.size = Pt(9.5)
r_ev4_sh.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

# Poin 1-4 disusun rapih, lurus, dan sejajar
add_aligned_list_item(
    doc,
    "1.",
    "Skema Partisi ID Kunci (Key Partitioning / Odd-Even)",
    "Seperti pada modul praktikum, Node A hanya menulis ID ganjil (101, 103, ...) dan Node B menulis ID genap (102, 104, ...), "
    "atau menggunakan alokasi blok range terpisah (Node A: 1–1.000.000, Node B: 1.000.001–2.000.000)."
)

add_aligned_list_item(
    doc,
    "2.",
    "UUID Global (UUIDv7)",
    "Mengadopsi UUIDv7 (time-ordered UUID) yang menghasilkan kunci unik 128-bit berurutan waktu. "
    "Probabilitas tabrakan UUID secara matematis mendekati nol tanpa memerlukan koordinasi antar-node."
)

add_aligned_list_item(
    doc,
    "3.",
    "Distributed Snowflake ID",
    "Menggunakan algoritma sequence berbasis 64-bit yang menyematkan Node ID unik ke dalam bit-bit identifier "
    "(seperti pola Twitter/Discord Snowflake)."
)

add_aligned_list_item(
    doc,
    "4.",
    "Partisi Kepemilikan Data (Data Ownership)",
    "Membagi wewenang penulisan berdasarkan entitas atau wilayah (misal Node A hanya memiliki wewenang menulis transaksi Cabang Jakarta, "
    "Node B untuk Cabang Bandung). Node lain hanya berhak membaca (Read Replica)."
)

doc.add_paragraph().paragraph_format.space_after = Pt(4)

# EVALUASI 5: LURUS DAN SEJAJAR
add_eval_header("5.", "Mengapa Logical Replication Bawaan Tidak Otomatis Menjadi Sistem Multi-Master Siap Produksi?")

p_ev5_intro = doc.add_paragraph(
    "Meskipun PostgreSQL mendukung replikasi logis dua arah, fitur bawaan ini dirancang sebagai alat pertukaran data fleksibel "
    "dan BUKAN merupakan mesin Active-Active Multi-Master Enterprise siap produksi karena 5 batasan kritikal berikut:"
)
p_ev5_intro.paragraph_format.left_indent = Inches(0)
p_ev5_intro.paragraph_format.space_after = Pt(4)
p_ev5_intro.paragraph_format.line_spacing = 1.15
p_ev5_intro.runs[0].font.name = "Calibri"
p_ev5_intro.runs[0].font.size = Pt(9.5)

add_aligned_list_item(
    doc,
    "1.",
    "Ketiadaan Distributed Lock Manager (DLM) & Konsensus Terdistribusi",
    "Tidak ada mekanisme koordinasi instan (seperti 2-Phase Commit, Raft, atau Paxos) saat penulisan lokal dieksekusi. "
    "Node tidak mengetahui apakah data yang diubah sedang diubah juga di node lawan."
)

add_aligned_list_item(
    doc,
    "2.",
    "Tidak Ada Resolusi Konflik Otomatis (Automatic Conflict Resolution)",
    "Bila terjadi tabrakan update bersamaan pada baris yang sama atau duplicate key, PostgreSQL bawaan tidak memiliki strategi otomatis "
    "seperti Last-Write-Wins (LWW) atau CRDT (Conflict-free Replicated Data Types). Apply worker justru akan crash/halt dan antrean replikasi macet "
    "hingga diperbaiki manual oleh administrator database."
)

add_aligned_list_item(
    doc,
    "3.",
    "DDL Skema Tidak Direplikasi Otomatis",
    "Operasi DDL (CREATE TABLE, ALTER TABLE, ADD COLUMN, CREATE INDEX) tidak ditransmisikan via logical replication. "
    "Perubahan skema harus dijalankan secara manual dan sinkron di semua node produksi."
)

add_aligned_list_item(
    doc,
    "4.",
    "Adanya Replication Lag (Eventual Consistency)",
    "Replikasi asinkron memiliki jeda waktu propagasi, sehingga pembaca di node lain berpotensi membaca data yang belum mutakhir (stale reads)."
)

add_aligned_list_item(
    doc,
    "5.",
    "Sequence Terdistribusi Tidak Tersinkron",
    "Objek SEQUENCE (seperti SERIAL / BIGSERIAL) bersifat lokal per node dan nilainya tidak saling bertukar otomatis, memicu risiko duplikasi nomor urut transaksi."
)

p_ev5_rec = doc.add_paragraph()
p_ev5_rec.paragraph_format.left_indent = Inches(0)
p_ev5_rec.paragraph_format.space_before = Pt(4)
p_ev5_rec.paragraph_format.space_after = Pt(4)
p_ev5_rec.paragraph_format.line_spacing = 1.15
r_rec_t = p_ev5_rec.add_run("💡 Rekomendasi Solusi Produksi: ")
r_rec_t.bold = True
r_rec_t.font.size = Pt(9.5)
r_rec_t.font.color.rgb = RGBColor(0x0E, 0x62, 0x51)
r_rec_c = p_ev5_rec.add_run(
    "Untuk lingkungan produksi active-active multi-master yang tangguh, industri menggunakan ekstensi khusus seperti pgEdge / Spock, "
    "EDB BDR (Bi-Directional Replication), atau mengadopsi platform Distributed SQL native seperti CockroachDB atau YugabyteDB."
)
r_rec_c.font.size = Pt(9.5)
r_rec_c.font.italic = True

output_path = "/home/desales/sbdt/pert_5/tugas/tabel_pengamatan_bagian_e.docx"
doc.save(output_path)
print("File Word berhasil diperbarui secara sempurna tanpa header/footer dan dengan perataan lurus sejajar:", output_path)
