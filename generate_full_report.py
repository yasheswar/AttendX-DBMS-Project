import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import re

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=80, bottom=80, left=110, right=110):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def generate_full_35_page_report():
    doc = docx.Document()
    
    # Standard 1.0 inch margins
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        s.page_width = Inches(8.5)
        s.page_height = Inches(11.0)

    # Styles
    normal = doc.styles['Normal']
    normal.font.name = 'Times New Roman'
    normal.font.size = Pt(12)
    normal.paragraph_format.line_spacing = 1.25
    normal.paragraph_format.space_after = Pt(6)

    # 1. Title Cover Page
    p_cov = doc.add_paragraph()
    p_cov.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_cov.add_run("Woxsen University\n")
    r1.font.size = Pt(24)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(160, 20, 30)

    r2 = p_cov.add_run("School of Technology\nDEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\n\n\n")
    r2.font.size = Pt(14)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(70, 70, 70)

    r3 = p_cov.add_run("PROJECT BASED LEARNING REPORT\n")
    r3.font.size = Pt(16)
    r3.font.bold = True
    r3.font.underline = True

    r4 = p_cov.add_run("Course: Database Management Systems\nAcademic Year: 2026–27\n\n\n")
    r4.font.size = Pt(13)
    r4.font.italic = True

    p_t = doc.add_paragraph()
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t.paragraph_format.space_before = Pt(10)
    p_t.paragraph_format.space_after = Pt(30)
    r_t1 = p_t.add_run("PROJECT TITLE:\n")
    r_t1.font.size = Pt(13)
    r_t1.font.bold = True
    r_t2 = p_t.add_run("DESIGN AND IMPLEMENTATION OF A DATABASE MANAGEMENT SYSTEM FOR STUDENT ATTENDANCE AND LEAVE APPROVAL MANAGEMENT SYSTEM (AttendX)")
    r_t2.font.size = Pt(16)
    r_t2.font.bold = True
    r_t2.font.color.rgb = RGBColor(160, 20, 30)

    t_cov = doc.add_table(rows=1, cols=2)
    t_cov.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_cov.columns[0].width = Inches(3.2)
    t_cov.columns[1].width = Inches(3.2)
    
    cl = t_cov.cell(0, 0).paragraphs[0]
    cl.add_run("Submitted by:\n").bold = True
    cl.add_run("Name: Yasheswar Kataria\n")
    cl.add_run("Roll Number: 25WU0101156\n")
    cl.add_run("Program: B.Tech – CSE\n")
    cl.add_run("Section: CSE - Panthers\n")
    
    cr = t_cov.cell(0, 1).paragraphs[0]
    cr.add_run("Under the Guidance of:\n").bold = True
    cr.add_run("Faculty Guide:\n")
    cr.add_run("Dr. Sahithi Chennamadhavuni\n").bold = True
    cr.add_run("Associate Professor\n")
    cr.add_run("Dept. of Computer Science and Engineering\n")

    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.space_before = Pt(80)
    p_foot.add_run("October, 2026\nWoxsen University, Hyderabad").bold = True

    doc.add_page_break()

    # 2. Certificate
    p_ch = doc.add_paragraph()
    p_ch.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ch = p_ch.add_run("CERTIFICATE")
    r_ch.font.size = Pt(18)
    r_ch.font.bold = True
    r_ch.font.underline = True

    p_cb = doc.add_paragraph()
    p_cb.paragraph_format.space_before = Pt(24)
    p_cb.paragraph_format.line_spacing = 1.3
    p_cb.add_run("This is to certify that the Project-Based Learning report entitled ")
    p_cb.add_run("“DESIGN AND IMPLEMENTATION OF A DATABASE MANAGEMENT SYSTEM FOR STUDENT ATTENDANCE AND LEAVE APPROVAL MANAGEMENT SYSTEM (AttendX)”").bold = True
    p_cb.add_run(" is a bonafide work carried out by ")
    p_cb.add_run("Mr. Yasheswar Kataria (Roll No: 25WU0101156)").bold = True
    p_cb.add_run(", student of B.Tech in Computer Science and Engineering at Woxsen University, during the Academic Year 2026–27, in partial fulfillment of the academic requirements for the course ")
    p_cb.add_run("Database Management Systems (DBMS)").bold = True
    p_cb.add_run(" under my supervision and guidance.\n\n\n\n\n\n")
    p_cb.add_run("_________________________________________\n(Dr. Sahithi Chennamadhavuni)\nAssociate Professor\nDepartment of Computer Science and Engineering\nSchool of Technology, Woxsen University").bold = True

    doc.add_page_break()

    # 3. Declaration
    p_dh = doc.add_paragraph()
    p_dh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_dh = p_dh.add_run("DECLARATION")
    r_dh.font.size = Pt(18)
    r_dh.font.bold = True
    r_dh.font.underline = True

    p_db = doc.add_paragraph()
    p_db.paragraph_format.space_before = Pt(24)
    p_db.paragraph_format.line_spacing = 1.3
    p_db.add_run("I hereby declare that the project entitled ")
    p_db.add_run("“DESIGN AND IMPLEMENTATION OF A DATABASE MANAGEMENT SYSTEM FOR STUDENT ATTENDANCE AND LEAVE APPROVAL MANAGEMENT SYSTEM (AttendX)”").bold = True
    p_db.add_run(", submitted to the School of Technology, Woxsen University, Hyderabad, for the Project-Based Learning evaluation in the course Database Management Systems, is an authentic record of original work carried out by me under the guidance of ")
    p_db.add_run("Dr. Sahithi Chennamadhavuni").bold = True
    p_db.add_run(".\n\nI confirm that this work has not been previously submitted in part or full for the award of any other degree, diploma, or academic certificate in this or any other institution. All technical concepts, algorithms, literature references, and datasets used have been properly acknowledged and cited in accordance with university academic standards.\n\n\n")
    p_db.add_run("Place: Hyderabad\nDate: 12th October 2026\n\n\n\n_________________________________________\nSignature of the Candidate\nName: Yasheswar Kataria\nRoll Number: 25WU0101156\nProgram: B.Tech – Computer Science and Engineering").bold = True

    doc.add_page_break()

    # Read markdown file
    with open("docs/PROJECT_REPORT.md", "r", encoding="utf-8") as f:
        md_text = f.read()

    lines = md_text.split("\n")
    
    # Locate Acknowledgement
    start_idx = 0
    for idx, l in enumerate(lines):
        if "## ACKNOWLEDGEMENT" in l:
            start_idx = idx
            break

    in_table = False
    table_lines = []
    in_code = False
    code_lines = []

    def flush_table(t_lines):
        if not t_lines: return
        rows = [row.strip().strip('|').split('|') for row in t_lines if '---' not in row]
        if not rows: return
        num_cols = max(len(r) for r in rows)
        t = doc.add_table(rows=len(rows), cols=num_cols)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.style = 'Table Grid'
        
        for r_i, row in enumerate(rows):
            is_header = (r_i == 0)
            for c_i in range(num_cols):
                cell = t.cell(r_i, c_i)
                text = row[c_i].strip() if c_i < len(row) else ""
                cell.text = text
                set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
                if is_header:
                    set_cell_background(cell, "E0E7FF") # Clean Academic Tint
                    for p in cell.paragraphs:
                        p.paragraph_format.space_after = Pt(2)
                        for r in p.runs:
                            r.font.name = 'Times New Roman'
                            r.font.bold = True
                            r.font.size = Pt(10)
                else:
                    if r_i % 2 == 1:
                        set_cell_background(cell, "F8FAFC")
                    for p in cell.paragraphs:
                        p.paragraph_format.space_after = Pt(2)
                        for r in p.runs:
                            r.font.name = 'Times New Roman'
                            r.font.size = Pt(9.5)
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(2)
        p_sp.paragraph_format.space_after = Pt(4)

    def flush_code(c_lines):
        if not c_lines: return
        p_c = doc.add_paragraph()
        p_c.paragraph_format.space_before = Pt(6)
        p_c.paragraph_format.space_after = Pt(6)
        p_c.paragraph_format.line_spacing = 1.05
        r_c = p_c.add_run("\n".join(c_lines))
        r_c.font.name = 'Consolas'
        r_c.font.size = Pt(9)
        r_c.font.color.rgb = RGBColor(30, 41, 59)

    for l in lines[start_idx:]:
        line = l.rstrip()

        # Handle page breaks
        if "\\pagebreak" in line or line.strip() == "---":
            if in_table:
                flush_table(table_lines)
                in_table = False
                table_lines = []
            if in_code:
                flush_code(code_lines)
                in_code = False
                code_lines = []
            if "\\pagebreak" in line:
                doc.add_page_break()
            continue

        # Handle Code blocks
        if line.strip().startswith("```"):
            if in_code:
                flush_code(code_lines)
                in_code = False
                code_lines = []
            else:
                if in_table:
                    flush_table(table_lines)
                    in_table = False
                    table_lines = []
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        # Handle Tables
        if line.strip().startswith("|") and line.strip().endswith("|"):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
            continue
        elif in_table:
            flush_table(table_lines)
            in_table = False
            table_lines = []

        # Handle Headings
        if line.startswith("# "):
            h = doc.add_paragraph()
            h.paragraph_format.space_before = Pt(18)
            h.paragraph_format.space_after = Pt(8)
            r = h.add_run(line[2:].strip())
            r.font.name = 'Times New Roman'
            r.font.size = Pt(16)
            r.font.bold = True
            r.font.color.rgb = RGBColor(160, 20, 30)
        elif line.startswith("## "):
            h = doc.add_paragraph()
            h.paragraph_format.space_before = Pt(14)
            h.paragraph_format.space_after = Pt(6)
            r = h.add_run(line[3:].strip())
            r.font.name = 'Times New Roman'
            r.font.size = Pt(13.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(30, 58, 138)
        elif line.startswith("### "):
            h = doc.add_paragraph()
            h.paragraph_format.space_before = Pt(10)
            h.paragraph_format.space_after = Pt(4)
            r = h.add_run(line[4:].strip())
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            r.font.bold = True
            r.font.color.rgb = RGBColor(55, 65, 81)
        elif line.startswith("#### "):
            h = doc.add_paragraph()
            h.paragraph_format.space_before = Pt(8)
            h.paragraph_format.space_after = Pt(3)
            r = h.add_run(line[5:].strip())
            r.font.name = 'Times New Roman'
            r.font.size = Pt(11.5)
            r.font.bold = True
            r.font.italic = True
        elif line.strip().startswith("- ") or line.strip().startswith("* "):
            p_bullet = doc.add_paragraph(style='List Bullet')
            p_bullet.paragraph_format.space_after = Pt(3)
            text = line.strip()[2:]
            parts = re.split(r'(\*\*.*?\*\*)', text)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    p_bullet.add_run(part[2:-2]).bold = True
                else:
                    p_bullet.add_run(part)
        elif line.strip() == "":
            pass
        else:
            p_text = doc.add_paragraph()
            p_text.paragraph_format.line_spacing = 1.25
            p_text.paragraph_format.space_after = Pt(6)
            parts = re.split(r'(\*\*.*?\*\*)', line)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    p_text.add_run(part[2:-2]).bold = True
                else:
                    p_text.add_run(part)

    # Save to dedicated 35-page target document
    out_file = "docs/AttendX_PBL_Report_Complete_35_Pages.docx"
    doc.save(out_file)
    print(f"Generated 35-page document at: {out_file}")

if __name__ == "__main__":
    generate_full_35_page_report()
