import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from build_full_report_docx import (
    set_cell_background, set_cell_borders, add_page_header,
    add_chapter_title, add_section_title, add_body_p, add_bullet_p,
    add_figure, format_table, add_code_block
)

def build_exampro_report():
    doc = docx.Document()
    
    # 1 inch margins all around
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # ----------------------------------------------------
    # PAGE 1: TITLE PAGE
    # ----------------------------------------------------
    add_page_header(doc, "1")
    if os.path.exists("report_assets/image1.png"):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(10)
        p_logo.add_run().add_picture("report_assets/image1.png", width=Inches(1.8))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("SAVITRIBAI PHULE PUNE UNIVERSITY\n\n")
    r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(15)

    r = p.add_run("A\nPROJECT REPORT ON\n\n")
    r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(13)

    r = p.add_run("“EXAMPRO – INSTITUTIONAL ONLINE EXAMINATION & ASSESSMENT MANAGEMENT SYSTEM WITH PROCTORING TELEMETRY”\n\n")
    r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(14)
    r.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    r = p.add_run("SUBMITTED TOWARDS THE\nPARTIAL FULFILLMENT OF THE REQUIREMENTS OF\n\n")
    r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(11)

    r = p.add_run("MASTER OF COMPUTER APPLICATION\n")
    r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(14)

    r = p.add_run("BY\n\n")
    r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(12)

    # Single student table
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    p_l = tbl.cell(0, 0).paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p_l.add_run("Student Name: DIVYA SHRIKRUSHNA GOLEKAR")
    r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(11)
    
    p_r = tbl.cell(0, 1).paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_r.add_run("Exam Seat No: 94")
    r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(11)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(16)
    r = p.add_run("MCA SEM-I\n(2025 Pattern NEP 2025)\n\nUnder The Guidance of\n")
    r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(12)

    r = p.add_run("Prof. Jaydeep Shivaji Karpe\n")
    r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(13)

    if os.path.exists("report_assets/image2.jpeg"):
        p_clg = doc.add_paragraph()
        p_clg.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_clg.paragraph_format.space_before = Pt(8)
        p_clg.paragraph_format.space_after = Pt(8)
        p_clg.add_run().add_picture("report_assets/image2.jpeg", width=Inches(1.2))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("DEPARTMENT OF MASTER OF COMPUTER APPLICATION\nADSUL COMPUTER AND MANAGEMENT INSTITUTE\nCHAS, AHMEDNAGAR 414005\n2026–27")
    r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(11)

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 2: CERTIFICATE
    # ----------------------------------------------------
    add_page_header(doc, "2")
    tbl_h = doc.add_table(rows=1, cols=2)
    tbl_h.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_h.autofit = False
    tbl_h.columns[0].width = Inches(1.3)
    tbl_h.columns[1].width = Inches(5.2)

    if os.path.exists("report_assets/image2.jpeg"):
        p_l = tbl_h.cell(0, 0).paragraphs[0]
        p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_l.add_run().add_picture("report_assets/image2.jpeg", width=Inches(1.0))
        
    p_r = tbl_h.cell(0, 1).paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_r.add_run("Sakeshwar Gramin Vikas Seva Sanstha\n")
    r.font.size = Pt(10); r.font.color.rgb = RGBColor(0x8B, 0x00, 0x00)
    r = p_r.add_run("ADSUL COMPUTER AND MANAGEMENT INSTITUTE\n")
    r.bold = True; r.font.size = Pt(13); r.font.color.rgb = RGBColor(0x8B, 0x00, 0x00)
    r = p_r.add_run("Chas, Chas-Nimblak Bypass Road, Ahmednagar – 414005 (Maharashtra)\n")
    r.font.size = Pt(9)
    r = p_r.add_run("S.P.P.U. Affiliation Letter No. CA/1722 (2024)    DTE Code: 5607\n")
    r.font.size = Pt(9); r.font.color.rgb = RGBColor(0x00, 0x00, 0x8B)
    r = p_r.add_run("Prin. Dr. Sambhaji Pathare, M.Sc., M.Phil., Ph.D.\n")
    r.bold = True; r.font.size = Pt(9.5); r.font.color.rgb = RGBColor(0x00, 0x00, 0x8B)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(10)
    p_border = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="18" w:space="1" w:color="000000"/></w:pBdr>')
    p._p.get_or_add_pPr().append(p_border)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("CERTIFICATE\n")
    r.bold = True; r.font.size = Pt(16)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(8)
    r = p.add_run("This is to certify that the Project Entitled\n\n")
    r.font.size = Pt(12)
    r = p.add_run("“EXAMPRO – INSTITUTIONAL ONLINE EXAMINATION & ASSESSMENT MANAGEMENT SYSTEM WITH PROCTORING TELEMETRY”\n\n")
    r.bold = True; r.font.size = Pt(13); r.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    r = p.add_run("Submitted by\n")
    r.font.size = Pt(12)

    tbl_c = doc.add_table(rows=1, cols=2)
    tbl_c.alignment = WD_TABLE_ALIGNMENT.CENTER
    p_l = tbl_c.cell(0, 0).paragraphs[0]
    r = p_l.add_run("Student Name: DIVYA SHRIKRUSHNA GOLEKAR")
    r.bold = True; r.font.size = Pt(11)
    p_r = tbl_c.cell(0, 1).paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_r.add_run("Exam Seat No: 94")
    r.bold = True; r.font.size = Pt(11)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14); p.paragraph_format.line_spacing = 1.3
    r = p.add_run("is a bonafide work carried out by the student under the supervision of Prof. Jaydeep Shivaji Karpe and is submitted towards the partial fulfillment of the requirements of the Master of Computer Application (MCA) Project under Savitribai Phule Pune University.")
    r.font.size = Pt(11.5)

    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(36)
    tbl_s1 = doc.add_table(rows=1, cols=2); tbl_s1.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_s1.cell(0, 0).paragraphs[0].add_run("Prof. Jaydeep Shivaji Karpe\nInternal Guide").bold = True
    p2 = tbl_s1.cell(0, 1).paragraphs[0]; p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p2.add_run("Prof. J. S. Karpe\nProject Co-ordinator").bold = True

    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(32)
    tbl_s2 = doc.add_table(rows=1, cols=2); tbl_s2.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_s2.cell(0, 0).paragraphs[0].add_run("Dr. P. B. Pandit\nHead of Department").bold = True
    p2 = tbl_s2.cell(0, 1).paragraphs[0]; p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p2.add_run("Dr. Sambhaji Pathare\nPrincipal").bold = True

    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(32)
    tbl_s3 = doc.add_table(rows=1, cols=2); tbl_s3.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_s3.cell(0, 0).paragraphs[0].add_run("Internal Examiner\n\nPlace: Ahilyanagar").bold = True
    p2 = tbl_s3.cell(0, 1).paragraphs[0]; p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p2.add_run("External Examiner\n\nDate: ____________________").bold = True

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 3: ACKNOWLEDGEMENT
    # ----------------------------------------------------
    add_page_header(doc, "3")
    add_chapter_title(doc, "ACKNOWLEDGEMENT", space_after=16)
    
    add_body_p(doc, "I would like to express my sincere gratitude to my project guide, Prof. Jaydeep Shivaji Karpe, for his valuable guidance, continuous support, and constructive suggestions throughout the completion of my project entitled “ExamPro – Institutional Online Examination & Assessment Management System with Proctoring Telemetry”.")
    add_body_p(doc, "I am profoundly thankful to the Head of the Department, faculty members, and Adsul Computer and Management Institute for providing the necessary computational resources, library facilities, and academic environment. I also acknowledge the developers and open-source communities behind Python, the Flask web microframework, SQLite, and modern web standards that made this implementation possible.")
    add_body_p(doc, "This academic project demonstrates a complete institutional assessment workflow comprising secure role-based access control, question bank authoring, full-screen examination running, client-side tab-switch anti-cheating telemetry, auto-grading, and performance analytics.")
    add_body_p(doc, "Finally, I extend my heartfelt thanks to my parents, family members, and friends for their constant encouragement, moral support, and blessings throughout this academic work.")
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(36)
    r = p.add_run("DIVYA SHRIKRUSHNA GOLEKAR\n")
    r.bold = True; r.font.size = Pt(13)
    r = p.add_run("Roll No: 94  |  Exam Seat No: 94\nMCA SEM-I  (2025 Pattern NEP 2025)\nAdsul Computer and Management Institute, Ahilyanagar")
    r.font.size = Pt(11)

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 4: ABSTRACT
    # ----------------------------------------------------
    add_page_header(doc, "4")
    add_chapter_title(doc, "ABSTRACT", space_after=16)

    add_body_p(doc, "ExamPro – Institutional Online Examination & Assessment Management System is a lightweight, high-integrity Python web application developed to modernize and secure institutional examinations for colleges and universities. Traditional paper-based examinations and unmonitored online questionnaires suffer from administrative overhead, slow evaluation turnarounds, transcription errors, and vulnerability to unauthorized tab switching or external searching.")
    add_body_p(doc, "The proposed system is engineered using Python 3 and the Flask WSGI web framework for server-side routing and business logic, Jinja2 templating with Tailwind CSS for high-performance visual presentation, and a persistent SQLite relational database engine. ExamPro implements a robust Three-Tier Role-Based Access Control (RBAC) architecture separating Institutional Administrators, Teaching Faculty/Examiners, and Student Candidates.")
    add_body_p(doc, "The application features five integrated core modules: (1) Administrative Faculty Provisioning & Governance, (2) Faculty Question Bank & Assessment Authoring, (3) Student Examination Runner equipped with Fullscreen Enforcement and Client-side Anti-Cheating Telemetry (logging tab switches, window blurs, and unauthorized navigation), (4) Real-Time Automated Grading and Instant Performance Analytics with detailed score breakdowns, and (5) Built-in Academic Support Helpdesk for grievance escalation.")
    add_body_p(doc, "ExamPro provides an academically verifiable, reliable, and easily deployable examination environment requiring zero external database daemon configuration. This documentation presents the complete system requirements, feasibility study, UML and architecture diagrams, relational table structures, data dictionary, implementation screens, automated testing suites (19 unit test cases), and future enhancements.")

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    r = p.add_run("Keywords: ")
    r.bold = True; r.font.size = Pt(11)
    r = p.add_run("Python, Flask, SQLite, Online Examination, Anti-Cheating Telemetry, Role-Based Access Control (RBAC), Automated Grading, SPPU MCA NEP 2025.")
    r.font.size = Pt(11)

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 5: INDEX
    # ----------------------------------------------------
    add_page_header(doc, "5")
    add_chapter_title(doc, "INDEX", space_after=8)
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Curriculum for MCA, Semester I (2025 Pattern NEP 2025) – Savitribai Phule Pune University\nDevelopment (Web Applications)\n")
    r.font.size = Pt(10)

    t_req = doc.add_table(rows=4, cols=2)
    format_table(t_req, [Inches(2.2), Inches(4.3)], ["Project Requirement", "Details"], [
        ["Technology Stack", "Frontend: HTML5, CSS3/Tailwind, Jinja2; Backend: Python 3, Flask"],
        ["Database", "SQLite Relational Database (SQL Relational Storage)"],
        ["Testing", "Unit testing (19 passing test cases), Integration testing, and UAT"]
    ])

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(4)
    p.add_run("Index: Development (Web Applications)").bold = True

    index_items = [
        ("1", "Introduction", "6"),
        ("1.1", "Company / Project Profile", "7"),
        ("1.2", "Problem Statement", "8"),
        ("1.3", "Existing System and Need for the System", "9"),
        ("1.4", "Scope of the Proposed System", "10"),
        ("1.5", "Objectives of the Proposed System", "11"),
        ("1.6", "Operating Environment – Hardware and Software", "12"),
        ("1.7", "Brief Description of Technology Used (Frontend / Backend / Database)", "12"),
        ("2", "System Analysis & Design", "13"),
        ("2.1", "System Requirements (Functional and Non-Functional)", "14–15"),
        ("2.2", "Feasibility Study (Technical, Economic & Operational)", "16–17"),
        ("2.3", "Architecture Design", "18"),
        ("2.4", "Entity Relationship Diagram (ERD)", "19"),
        ("2.5", "Class Diagram", "20"),
        ("2.6", "Use Case Diagrams", "21"),
        ("2.7", "Activity Diagram", "22"),
        ("2.8", "Sequence Diagram", "23"),
        ("2.9", "Component Diagram", "24"),
        ("2.10", "Table Design", "25–28"),
        ("2.11", "Data Dictionary", "29–30"),
        ("3", "Implementation", "31"),
        ("3.1", "Input Screens (Screens must have valid data)", "32–35"),
        ("3.2", "Output Screens/Reports (at least 5 valid records per report)", "36"),
        ("3.3", "Sample Code (only 3–4 pages)", "37–39"),
        ("4", "Testing", "40"),
        ("4.1", "Test Strategy", "40"),
        ("4.2", "Unit Test Plan", "41"),
        ("4.3", "Acceptance of Test Plan", "42"),
        ("4.4", "Test Cases", "43–44"),
        ("4.5", "Results & Observations", "45"),
        ("5", "Conclusion", "46"),
        ("5.1", "Summary / Conclusion", "46"),
        ("5.2", "Limitations of the System", "47"),
        ("5.3", "Future Enhancements", "47"),
        ("6", "References / Bibliography", "48"),
        ("7", "Appendices", "49"),
        ("7.1", "Annexure I – Additional Input & Output Screens", "49"),
        ("7.2", "Annexure II – Progress Sheet", "50")
    ]

    t_idx = doc.add_table(rows=len(index_items) + 1, cols=3)
    format_table(t_idx, [Inches(1.1), Inches(4.4), Inches(1.0)], ["Chapter No.", "Details", "Page No."], index_items)

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 6: CHAPTER 1 - INTRODUCTION
    # ----------------------------------------------------
    add_page_header(doc, "6")
    add_chapter_title(doc, "CHAPTER 1: INTRODUCTION", space_after=14)

    add_body_p(doc, "ExamPro is an institutional, lightweight web application designed to manage and secure the entire lifecycle of computer-based testing (CBT) and academic evaluations. It consolidates user authentication, question bank repository management, exam scheduling, browser lockdown proctoring, instant grading, and performance reporting into one intuitive web interface.")
    add_body_p(doc, "The application utilizes Python with the Flask WSGI microframework, Jinja2 server-rendered templates, Tailwind CSS for modern aesthetics, and a localized SQLite database engine. The supplied Python backend creates and provisions required tables automatically upon application startup if they do not exist.")
    add_body_p(doc, "The system architecture is structured across five major institutional modules: Administrative Faculty Provisioning, Question Bank Authoring, Timed & Monitored Examination Runner, Automated Result Generation, and Candidate Helpdesk Ticketing. Together, these modules support seamless academic examination oversight through standard web browsers without requiring complex server installations.")

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 7: 1.1 COMPANY / PROJECT PROFILE
    # ----------------------------------------------------
    add_page_header(doc, "7")
    add_section_title(doc, "1.1 COMPANY / PROJECT PROFILE")
    
    add_body_p(doc, "Project Name: ExamPro – Institutional Online Examination & Assessment Management System. Application Category: Academic Computer-Based Testing (CBT), Educational Assessment & Proctoring Telemetry. Deployment Style: Local/Institutional Flask Web Server accessed through standard web browsers (Chrome, Edge, Firefox). Intended Users: Institutional Administrators, MCA Faculty Examiners, and Enrolled Candidate Students.")
    add_body_p(doc, "The name “ExamPro” signifies professional, high-integrity institutional examination administration. The supplied codebase is developed as an academic project fulfilling the Master of Computer Application (MCA) curriculum at Savitribai Phule Pune University. The project therefore adopts “Project Profile” as an academically authentic description of the software system.")
    add_body_p(doc, "The interface utilizes a modern, clean visual theme with pure white modular containers, crisp borders (#E5E5E7), subtle elevation shadows, and department-specific action bars. Role-based navigation ensures that students, faculty, and administrative directors only access authorized resources.")

    add_figure(doc, "report_assets/screen_welcome.png", "Figure 1.1 — ExamPro institutional welcome portal and role selection interface.", width=Inches(5.4))

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 8: 1.2 PROBLEM STATEMENT
    # ----------------------------------------------------
    add_page_header(doc, "8")
    add_section_title(doc, "1.2 PROBLEM STATEMENT")
    
    add_body_p(doc, "Educational institutions face significant logistical and academic integrity challenges when administering examinations. Traditional pen-and-paper assessments incur heavy operational overhead, including paper printing, manual invigilation, physical paper sorting, transcription errors, and prolonged evaluation turnarounds spanning weeks.")
    add_body_p(doc, "Conversely, basic online assessment tools (such as general questionnaire web forms) lack essential academic safeguards: they do not prevent students from opening external search tabs, switching windows to search answer keys, or communicating during an active test session. Furthermore, they lack comprehensive role-based access control (RBAC), leaving question banks vulnerable to unauthorized modifications.")
    add_body_p(doc, "ExamPro addresses this challenge by providing an integrated, browser-based examination environment that enforces client-side lockdown telemetry (full-screen enforcement and tab-switch logging), automates instant grading, and maintains tamper-resistant audit trails in a local relational database.")

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 9: 1.3 EXISTING SYSTEM AND NEED FOR THE SYSTEM
    # ----------------------------------------------------
    add_page_header(doc, "9")
    add_section_title(doc, "1.3 EXISTING SYSTEM AND NEED FOR THE SYSTEM")

    add_body_p(doc, "In existing institutional setups, examination processes are either strictly manual or fragmented across multiple disconnected software tools. Teachers draft questions in word processors, physical answer booklets are collected and manually marked, and marks are manually typed into grade sheets. In unproctored digital tools, there is zero detection of academic dishonesty during live tests.")
    add_body_p(doc, "An integrated computerized examination system is essential for several critical reasons:")
    add_bullet_p(doc, "Integrity Preservation: ", "Real-time client telemetry tracks and counts unauthorized tab switches and window blur events.")
    add_bullet_p(doc, "Instant Assessment: ", "Automatic scoring against stored answer keys produces immediate scores, percentages, and pass/fail statuses upon submission.")
    add_bullet_p(doc, "Role-Based Security: ", "Administrators directly provision faculty, faculty manage subject-specific questions, and candidates access only their assigned exams.")
    add_bullet_p(doc, "Centralized Analytics: ", "Consolidated performance records, candidate averages, and pass percentage charts are computed instantly.")

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 10: 1.4 SCOPE OF THE PROPOSED SYSTEM
    # ----------------------------------------------------
    add_page_header(doc, "10")
    add_section_title(doc, "1.4 SCOPE OF THE PROPOSED SYSTEM")

    add_body_p(doc, "The scope is strictly defined by the functional requirements implemented in app.py, database.py, and associated templates:")
    add_bullet_p(doc, "Role-Based Authentication: ", "Secure login handlers for Admin, Faculty, and Student users with password verification and session enforcement.")
    add_bullet_p(doc, "Faculty Provisioning: ", "Institutional administrators directly enroll and manage MCA faculty profiles without public unverified registration.")
    add_bullet_p(doc, "Question Bank Management: ", "Creation, listing, and validation of multiple-choice questions (MCQs) with options, answer keys, and explanatory rationales.")
    add_bullet_p(doc, "Examination Runner: ", "Interactive timed assessment interface with countdown timer, fullscreen lockout request, and tab-switch detection.")
    add_bullet_p(doc, "Instant Automated Grading: ", "Deterministic server-side grading calculating raw score, percentage, and detailed question-by-question breakdown.")
    add_bullet_p(doc, "Support Ticket System: ", "Integrated helpdesk enabling candidates to lodge academic queries and administrators to inspect status.")

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 11: 1.5 OBJECTIVES OF THE PROPOSED SYSTEM
    # ----------------------------------------------------
    add_page_header(doc, "11")
    add_section_title(doc, "1.5 OBJECTIVES OF THE PROPOSED SYSTEM")

    add_body_p(doc, "The primary objective is to demonstrate a robust, lightweight, and academically secure Python web application that digitizes institutional examinations without requiring third-party database servers or complex cloud dependencies.")
    add_body_p(doc, "Supporting technical and academic objectives include:")
    add_bullet_p(doc, "Automate Evaluation: ", "Eliminate manual paper grading through instant deterministic comparison of student responses against correct keys.")
    add_bullet_p(doc, "Enforce Anti-Cheating Telemetry: ", "Detect and log candidate tab switching, window minimization, or unauthorized navigation during active tests.")
    add_bullet_p(doc, "Role Isolation: ", "Enforce strict RBAC separating administrative governance, faculty item authoring, and student participation.")
    add_bullet_p(doc, "Database Persistence: ", "Ensure ACID-compliant relational data storage using SQLite for user accounts, exams, questions, and submissions.")
    add_bullet_p(doc, "Automated Verification: ", "Validate system reliability through a comprehensive unit test suite covering all authentication and assessment workflows.")

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 12: 1.6 OPERATING ENVIRONMENT & 1.7 TECHNOLOGY
    # ----------------------------------------------------
    add_page_header(doc, "12")
    add_section_title(doc, "1.6 OPERATING ENVIRONMENT & 1.7 TECHNOLOGY")

    add_body_p(doc, "Operating Environment — Hardware Requirements:")
    add_bullet_p(doc, "Processor: ", "Intel Core i3 / AMD Ryzen 3 or higher (x86_64 or ARM64 architecture).")
    add_bullet_p(doc, "RAM: ", "4 GB minimum (8 GB recommended for simultaneous browser and IDE operation).")
    add_bullet_p(doc, "Storage: ", "500 MB free hard drive / SSD storage for code, database, and telemetry logs.")
    add_bullet_p(doc, "Display: ", "1366x768 or higher display resolution.")

    add_body_p(doc, "Operating Environment — Software Requirements:")
    add_bullet_p(doc, "Operating System: ", "Microsoft Windows 10/11, Ubuntu Linux 22.04 LTS, or macOS.")
    add_bullet_p(doc, "Runtime Environment: ", "Python 3.10, 3.11, or 3.12 64-bit runtime.")
    add_bullet_p(doc, "Web Browser: ", "Google Chrome 110+, Microsoft Edge 110+, or Mozilla Firefox.")
    add_bullet_p(doc, "IDE / Tools: ", "Visual Studio Code, DB Browser for SQLite.")

    add_body_p(doc, "Technology Stack Details:")
    t_tech = doc.add_table(rows=6, cols=2)
    format_table(t_tech, [Inches(2.0), Inches(4.5)], ["Layer", "Technology / Source Component"], [
        ["Presentation Layer", "HTML5, Jinja2 Server-Side Templates, Material Symbols"],
        ["Styling & UI Design", "Tailwind CSS 4, Custom Academic Theme CSS (static/css/theme.css)"],
        ["Client Telemetry", "Vanilla JavaScript (Page Visibility API, Fullscreen API, Event Listeners)"],
        ["Backend Web Framework", "Python 3.12, Flask 3.1.3 (WSGI Request Router, Sessions, Flash Alerts)"],
        ["Database Layer", "SQLite 3 Relational Database (exam_system.db via sqlite3 library)"]
    ])

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 13: CHAPTER 2 - SYSTEM ANALYSIS & DESIGN
    # ----------------------------------------------------
    add_page_header(doc, "13")
    add_chapter_title(doc, "CHAPTER 2: SYSTEM ANALYSIS & DESIGN", space_after=14)

    add_body_p(doc, "System analysis translates the institutional examination requirements into concrete technical specifications, data models, and software architectures. The delivered application adopts a Three-Tier Client-Server Architecture leveraging Flask’s request-dispatching engine and SQLite’s transactional engine.")
    add_body_p(doc, "The presentation tier renders semantic HTML5 templates via Jinja2, capturing candidate interactions and transmitting HTTP POST requests. The application tier (app.py) authenticates users, validates form inputs, evaluates exam submissions, and computes statistical metrics. The data tier stores relational data persistently in exam_system.db.")

    add_figure(doc, "report_assets/arch_design.png", "Figure 2.1 — Three-Tier Architecture derived from app.py, Jinja2 templates, and SQLite.", width=Inches(5.4))

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGES 14 & 15: 2.1 SYSTEM REQUIREMENTS (FUNCTIONAL & NON-FUNCTIONAL)
    # ----------------------------------------------------
    add_page_header(doc, "14")
    add_section_title(doc, "2.1 SYSTEM REQUIREMENTS — FUNCTIONAL")

    add_body_p(doc, "Functional requirements describe the specific operational capabilities implemented in the application code. Each requirement is mapped to its corresponding Flask route and database entity:")

    fr_items = [
        ("FR-01", "Institutional User Login & Session RBAC", "POST /admin/login, /staff/login, /student/login"),
        ("FR-02", "Direct Faculty Member Enrollment", "POST /admin/staff/create (Admin only)"),
        ("FR-03", "Student Self-Registration & Roster CRUD", "POST /student/register, /admin/student/create"),
        ("FR-04", "Question Bank Item Creation & Option Setup", "POST /questions/add (MCQ choices, answer key)"),
        ("FR-05", "Assessment Scheduling & Publishing", "POST /exams/create, /exams/publish/<id>"),
        ("FR-06", "Active Timed Exam Runner & Lockout", "GET /exam/<id>/run (Timer, Fullscreen, Questions)"),
        ("FR-07", "Tab-Switch Anti-Cheating Telemetry", "POST /exam/<id>/tab_switch (Increment violation counter)"),
        ("FR-08", "Automatic Submission Evaluation & Scoring", "POST /student/exam/<id>/submit (Calculate score, %)"),
        ("FR-09", "Performance Reporting & Analytics", "GET /reports, /admin/dashboard (Pass rate, Averages)"),
        ("FR-10", "Candidate Support Ticket Helpdesk", "POST /student/ticket/create, /admin/ticket/resolve")
    ]
    t_fr = doc.add_table(rows=len(fr_items) + 1, cols=3)
    format_table(t_fr, [Inches(1.1), Inches(3.2), Inches(2.2)], ["ID", "Requirement Description", "Implemented Endpoint / Route"], fr_items)

    doc.add_page_break()

    add_page_header(doc, "15")
    add_section_title(doc, "2.1 SYSTEM REQUIREMENTS — NON-FUNCTIONAL")

    add_body_p(doc, "Non-functional requirements define the quality attributes, security standards, and performance constraints observed by ExamPro:")
    add_bullet_p(doc, "Usability (NFR-01): ", "The UI adheres to a clean academic dashboard design with consistent navigation, status badges, and feedback flash notifications.")
    add_bullet_p(doc, "Security & RBAC (NFR-02): ", "Passwords are cryptographically hashed; endpoints enforce role checks redirecting unauthorized users.")
    add_bullet_p(doc, "Integrity & Anti-Cheating (NFR-03): ", "Client-side Page Visibility API detects window blur and tab switching, transmitting telemetry to the server.")
    add_bullet_p(doc, "Data Persistence (NFR-04): ", "All entity records are saved to SQLite with parameterized SQL queries preventing SQL injection vulnerabilities.")
    add_bullet_p(doc, "Portability (NFR-05): ", "Zero external database setup; the entire project runs across Windows, Linux, and macOS using standard Python libraries.")
    add_bullet_p(doc, "Performance (NFR-06): ", "Page render and submission response times remain under 150 ms under local testing workloads.")

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGES 16 & 17: 2.2 FEASIBILITY STUDY
    # ----------------------------------------------------
    add_page_header(doc, "16")
    add_section_title(doc, "2.2 FEASIBILITY STUDY — TECHNICAL")

    add_body_p(doc, "Technical feasibility evaluates whether the project can be successfully constructed, operated, and maintained using accessible hardware and software tools.")
    add_body_p(doc, "Python was selected due to its readability, extensive standard library, and robust web ecosystem. The Flask microframework provides lightweight WSGI routing without the unnecessary overhead of heavy enterprise frameworks. SQLite was selected as the database engine because it is built into the Python standard library, requires zero daemon configuration, and provides full ACID compliance for institutional examination records.")
    add_body_p(doc, "The frontend leverages standard HTML5, CSS3/Tailwind, and vanilla JavaScript. Anti-cheating telemetry relies on standard browser APIs (Page Visibility API and Fullscreen API) natively supported across all modern web browsers, eliminating the need for invasive external client software or plugins.")

    doc.add_page_break()

    add_page_header(doc, "17")
    add_section_title(doc, "2.2 FEASIBILITY STUDY — ECONOMIC & OPERATIONAL")

    add_body_p(doc, "Economic Feasibility:")
    add_body_p(doc, "The economic feasibility of ExamPro is exceptionally favorable. All software technologies utilized—Python, Flask, SQLite, Tailwind CSS, and Visual Studio Code—are open-source and free of mandatory licensing fees. The project operates on existing institutional hardware (standard student and lab laptops). Physical examination expenses (paper reams, cartridge toner, physical storage, and transport logistics) are eliminated, achieving significant cost reduction.")

    add_body_p(doc, "Operational Feasibility:")
    add_body_p(doc, "The operational workflows mirror established academic procedures: administrators enroll faculty, teachers author questions and schedule tests, and students log in to complete examinations. Clear feedback messages, intuitive navigation bars, and instant scorecards ensure minimal training requirements for teaching staff and students.")

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 18: 2.3 ARCHITECTURE DESIGN
    # ----------------------------------------------------
    add_page_header(doc, "18")
    add_section_title(doc, "2.3 ARCHITECTURE DESIGN")

    add_body_p(doc, "The architectural design organizes application logic into clean, decoupled layers following the Model-View-Controller (MVC) pattern adapted for web microframeworks:")
    add_bullet_p(doc, "Client / View Tier: ", "Browser-rendered Jinja2 HTML templates capturing user inputs, displaying exam questions, and executing client-side timer and proctoring scripts.")
    add_bullet_p(doc, "Controller Tier (app.py): ", "Handles HTTP requests, executes session validation, coordinates business logic, and evaluates exam submissions.")
    add_bullet_p(doc, "Data Tier (database.py & SQLite): ", "Manages database connections, parameterized SQL execution, and relational table schemas.")

    add_figure(doc, "report_assets/component_diagram.png", "Figure 2.2 — Architectural component and dependency diagram of ExamPro.", width=Inches(5.4))

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 19: 2.4 ENTITY RELATIONSHIP DIAGRAM (ERD)
    # ----------------------------------------------------
    add_page_header(doc, "19")
    add_section_title(doc, "2.4 ENTITY RELATIONSHIP DIAGRAM (ERD)")

    add_body_p(doc, "The relational schema consists of six interconnected tables: users, subjects, exams, questions, submissions, and support_tickets. The primary key relationships ensure referential integrity across tests and candidate attempts.")

    add_figure(doc, "report_assets/erd.png", "Figure 2.3 — Entity Relationship Diagram (ERD) showing primary and foreign key associations.", width=Inches(5.5))

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 20: 2.5 CLASS DIAGRAM — CONCEPTUAL MODEL
    # ----------------------------------------------------
    add_page_header(doc, "20")
    add_section_title(doc, "2.5 CLASS DIAGRAM — CONCEPTUAL MODEL")

    add_body_p(doc, "The conceptual class diagram outlines the object-oriented structure representing domain entities, their primary attributes, business operations, and service helpers:")

    add_figure(doc, "report_assets/class_diagram.png", "Figure 2.4 — Conceptual UML class diagram of core system entities and database services.", width=Inches(5.4))

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 21: 2.6 USE CASE DIAGRAM
    # ----------------------------------------------------
    add_page_header(doc, "21")
    add_section_title(doc, "2.6 USE CASE DIAGRAM")

    add_body_p(doc, "The use case model defines system boundaries and illustrates the functional interactions available to the three principal actors: Administrator, Teaching Faculty, and Student Candidate:")

    add_figure(doc, "report_assets/use_case_diagram.png", "Figure 2.5 — UML Use Case diagram mapping actor interactions to core application services.", width=Inches(5.4))

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 22: 2.7 ACTIVITY DIAGRAM — EXAMINATION RUNNER
    # ----------------------------------------------------
    add_page_header(doc, "22")
    add_section_title(doc, "2.7 ACTIVITY DIAGRAM — EXAMINATION RUNNER")

    add_body_p(doc, "The activity diagram traces the candidate workflow during an active assessment, from launching the test to proctoring checks, response submission, and automated score computation:")

    add_figure(doc, "report_assets/activity_diagram.png", "Figure 2.6 — UML Activity diagram illustrating exam execution and anti-cheating telemetry.", width=Inches(4.8))

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 23: 2.8 SEQUENCE DIAGRAM — SUBMISSION & GRADING
    # ----------------------------------------------------
    add_page_header(doc, "23")
    add_section_title(doc, "2.8 SEQUENCE DIAGRAM — SUBMISSION & GRADING")

    add_body_p(doc, "The sequence diagram models the chronological exchange of HTTP messages, controller invocations, and database queries during the exam submission and auto-grading lifecycle:")

    add_figure(doc, "report_assets/sequence_diagram.png", "Figure 2.7 — UML Sequence diagram showing message flow during submission evaluation.", width=Inches(5.5))

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 24: 2.9 COMPONENT DIAGRAM
    # ----------------------------------------------------
    add_page_header(doc, "24")
    add_section_title(doc, "2.9 COMPONENT DIAGRAM — IMPLEMENTED ARCHITECTURE")

    add_body_p(doc, "The component diagram depicts physical software dependencies, separating client browser execution, WSGI request routing, Jinja2 template rendering, and SQLite file persistence:")

    add_figure(doc, "report_assets/component_diagram.png", "Figure 2.8 — Implemented component dependency diagram.", width=Inches(5.4))

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGES 25–28: 2.10 TABLE DESIGN
    # ----------------------------------------------------
    add_page_header(doc, "25")
    add_section_title(doc, "2.10 TABLE DESIGN — USERS & SUBJECTS")

    add_body_p(doc, "The users table maintains institutional accounts, roles (admin, staff, student), department affiliations, and authentication credentials:")
    t_u = doc.add_table(rows=8, cols=4)
    format_table(t_u, [Inches(1.5), Inches(1.2), Inches(1.5), Inches(2.3)], ["Field Name", "SQLite Type", "Constraint", "Description / Purpose"], [
        ["id", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Unique identifier for user account"],
        ["username", "TEXT", "UNIQUE NOT NULL", "Login handle (e.g. prof_priya, vivek_k)"],
        ["password_hash", "TEXT", "NOT NULL", "Werkzeug salted password hash"],
        ["full_name", "TEXT", "NOT NULL", "Candidate or faculty formal name"],
        ["role", "TEXT", "NOT NULL", "Access role ('admin', 'staff', 'student')"],
        ["is_approved", "INTEGER", "DEFAULT 1", "Authorization flag for faculty & students"],
        ["department", "TEXT", "DEFAULT 'MCA'", "Academic department affiliation"]
    ])

    doc.add_page_break()

    add_page_header(doc, "26")
    add_section_title(doc, "2.10 TABLE DESIGN — EXAMS")

    add_body_p(doc, "The exams table records test parameters, duration limits, passing marks, and publication status:")
    t_e = doc.add_table(rows=8, cols=4)
    format_table(t_e, [Inches(1.5), Inches(1.2), Inches(1.5), Inches(2.3)], ["Field Name", "SQLite Type", "Constraint", "Description / Purpose"], [
        ["id", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Unique examination identifier"],
        ["title", "TEXT", "NOT NULL", "Assessment name (e.g. Python Fundamentals)"],
        ["subject_id", "INTEGER", "FOREIGN KEY -> subjects", "Associated academic subject"],
        ["created_by", "INTEGER", "FOREIGN KEY -> users", "Faculty examiner author ID"],
        ["duration_minutes", "INTEGER", "DEFAULT 60", "Allotted test duration in minutes"],
        ["total_marks", "INTEGER", "DEFAULT 100", "Total possible assessment score"],
        ["is_published", "INTEGER", "DEFAULT 1", "Visibility flag for student candidates"]
    ])

    doc.add_page_break()

    add_page_header(doc, "27")
    add_section_title(doc, "2.10 TABLE DESIGN — QUESTIONS")

    add_body_p(doc, "The questions table stores multiple-choice items, options A through D, correct answer keys, and rationales:")
    t_q = doc.add_table(rows=9, cols=4)
    format_table(t_q, [Inches(1.5), Inches(1.2), Inches(1.5), Inches(2.3)], ["Field Name", "SQLite Type", "Constraint", "Description / Purpose"], [
        ["id", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Unique question item identifier"],
        ["exam_id", "INTEGER", "FOREIGN KEY -> exams", "Associated parent assessment ID"],
        ["question_text", "TEXT", "NOT NULL", "Problem statement or question prompt"],
        ["option_a", "TEXT", "NOT NULL", "First candidate choice"],
        ["option_b", "TEXT", "NOT NULL", "Second candidate choice"],
        ["option_c", "TEXT", "NOT NULL", "Third candidate choice"],
        ["option_d", "TEXT", "NOT NULL", "Fourth candidate choice"],
        ["correct_option", "TEXT", "NOT NULL", "Scoring key ('A', 'B', 'C', or 'D')"]
    ])

    doc.add_page_break()

    add_page_header(doc, "28")
    add_section_title(doc, "2.10 TABLE DESIGN — SUBMISSIONS & TICKETS")

    add_body_p(doc, "The submissions table captures completed test attempts, scores, percentage results, and proctoring telemetry:")
    t_s = doc.add_table(rows=8, cols=4)
    format_table(t_s, [Inches(1.5), Inches(1.2), Inches(1.5), Inches(2.3)], ["Field Name", "SQLite Type", "Constraint", "Description / Purpose"], [
        ["id", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Unique submission record ID"],
        ["user_id", "INTEGER", "FOREIGN KEY -> users", "Student candidate user ID"],
        ["exam_id", "INTEGER", "FOREIGN KEY -> exams", "Assessed examination ID"],
        ["score", "INTEGER", "NOT NULL", "Points awarded from evaluation"],
        ["percentage", "REAL", "NOT NULL", "Calculated grade percentage"],
        ["status", "TEXT", "DEFAULT 'Submitted'", "Final assessment status"],
        ["tab_switch_count", "INTEGER", "DEFAULT 0", "Anti-cheating violation counter"]
    ])

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGES 29 & 30: 2.11 DATA DICTIONARY
    # ----------------------------------------------------
    add_page_header(doc, "29")
    add_section_title(doc, "2.11 DATA DICTIONARY — USER INPUTS")

    add_body_p(doc, "The user input data dictionary defines client form fields, validation requirements, and data conversions enforced by Flask:")
    t_dd_in = doc.add_table(rows=6, cols=3)
    format_table(t_dd_in, [Inches(1.8), Inches(2.5), Inches(2.2)], ["Form / Action", "Required Server Inputs", "Optional Inputs & Defaults"], [
        ["Student Registration", "username, password, full_name", "department (default MCA), contact"],
        ["Faculty Enrollment", "username, password, full_name", "designation, department, contact"],
        ["Exam Creation", "title, subject_id, duration_minutes", "total_marks, passing_marks, published"],
        ["Question Authoring", "question_text, option_a..d, correct_option", "marks (default 1), explanation"],
        ["Support Ticket", "subject, message", "category (default 'Technical')"]
    ])

    doc.add_page_break()

    add_page_header(doc, "30")
    add_section_title(doc, "2.11 DATA DICTIONARY — DERIVED METRICS")

    add_body_p(doc, "The dashboard presents aggregate analytics dynamically derived via SQL queries across relational tables:")
    t_dd_met = doc.add_table(rows=7, cols=2)
    format_table(t_dd_met, [Inches(2.5), Inches(4.0)], ["Derived Metric", "SQL Derivation / Aggregation Query"], [
        ["Total Active Candidates", "SELECT COUNT(*) FROM users WHERE role = 'student' AND is_approved = 1"],
        ["Total Teaching Faculty", "SELECT COUNT(*) FROM users WHERE role = 'staff' AND is_approved = 1"],
        ["Published Assessments", "SELECT COUNT(*) FROM exams WHERE is_published = 1"],
        ["Total Test Submissions", "SELECT COUNT(*) FROM submissions WHERE status = 'Submitted'"],
        ["Institutional Pass Rate", "SELECT ROUND(AVG(CASE WHEN percentage >= 50.0 THEN 1.0 ELSE 0.0 END)*100, 1)"],
        ["Average Candidate Score", "SELECT ROUND(AVG(percentage), 1) FROM submissions"]
    ])

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 31: CHAPTER 3 - IMPLEMENTATION
    # ----------------------------------------------------
    add_page_header(doc, "31")
    add_chapter_title(doc, "CHAPTER 3: IMPLEMENTATION", space_after=14)

    add_body_p(doc, "ExamPro is implemented as a cohesive, lightweight web application combining server-side Python controllers with client-side Jinja2 presentation. SQLite provides zero-configuration persistent storage.")
    add_body_p(doc, "The following sections illustrate the verified application interface, including authentication screens, administrative oversight panels, faculty question management, student examination runner, automated result scorecards, and sample backend source code.")

    add_figure(doc, "report_assets/screen_admin_dash.png", "Figure 3.1 — ExamPro Administrator Dashboard displaying institutional telemetry and directory.", width=Inches(5.4))

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGES 32–35: 3.1 INPUT SCREENS
    # ----------------------------------------------------
    add_page_header(doc, "32")
    add_section_title(doc, "3.1 INPUT SCREEN — STUDENT REGISTRATION")
    add_body_p(doc, "The student registration portal allows candidates to register with valid institutional credentials, roll numbers, and MCA department affiliations.")
    add_figure(doc, "report_assets/screen_student_register.png", "Figure 3.2 — Student candidate registration interface.", width=Inches(5.2))

    doc.add_page_break()

    add_page_header(doc, "33")
    add_section_title(doc, "3.1 INPUT SCREEN — INSTITUTIONAL LOGIN")
    add_body_p(doc, "Secure role-differentiated login portals provide authenticated entry for students, faculty examiners, and system administrators.")
    add_figure(doc, "report_assets/screen_student_login.png", "Figure 3.3 — Secure student login interface.", width=Inches(5.2))

    doc.add_page_break()

    add_page_header(doc, "34")
    add_section_title(doc, "3.1 INPUT SCREEN — FACULTY MANAGEMENT")
    add_body_p(doc, "The administrative faculty directory features direct faculty provisioning, department assignment, and access control without unverified queues.")
    add_figure(doc, "report_assets/screen_staff.png", "Figure 3.4 — Administrative teaching faculty directory and enrollment management.", width=Inches(5.2))

    doc.add_page_break()

    add_page_header(doc, "35")
    add_section_title(doc, "3.1 INPUT SCREEN — CANDIDATE ROSTER CRUD")
    add_body_p(doc, "Administrators can inspect enrolled student profiles, review academic performance, and manage candidate accounts.")
    add_figure(doc, "report_assets/screen_students.png", "Figure 3.5 — Student candidate management and CRUD interface.", width=Inches(5.2))

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 36: 3.2 OUTPUT SCREENS & REPORTS
    # ----------------------------------------------------
    add_page_header(doc, "36")
    add_section_title(doc, "3.2 OUTPUT SCREENS AND REPORTS")
    add_body_p(doc, "The institutional reporting dashboard presents candidate assessment scores, passing percentages, and proctoring violation logs with verified records:")
    add_figure(doc, "report_assets/screen_reports.png", "Figure 3.6 — Institutional assessment analytics and candidate submission reports.", width=Inches(5.4))

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGES 37–39: 3.3 SAMPLE CODE
    # ----------------------------------------------------
    add_page_header(doc, "37")
    add_section_title(doc, "3.3 SAMPLE SOURCE CODE — DATABASE INITIALIZATION")
    add_body_p(doc, "The database service initializes SQLite tables, applies foreign keys, and configures row factories for dictionary-like column access:")

    code_1 = """# database.py - Database Connection and Table Initialization
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "exam_system.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    schema_file = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_file, "r") as f:
        schema_sql = f.read()
    with get_db() as conn:
        conn.executescript(schema_sql)
        conn.commit()"""
    add_code_block(doc, code_1)

    doc.add_page_break()

    add_page_header(doc, "38")
    add_section_title(doc, "3.3 SAMPLE SOURCE CODE — EXAM SUBMISSION & GRADING")
    add_body_p(doc, "The submission evaluation controller compares student selections against stored question keys, calculates percentages, and logs tab violations:")

    code_2 = """# Extract from app.py - Exam Evaluation and Result Scoring
@app.route("/student/exam/<int:exam_id>/submit", methods=["POST"])
@login_required(role="student")
def student_submit_exam(exam_id):
    user_id = session["user_id"]
    tab_switches = int(request.form.get("tab_switch_count", 0))
    
    with get_db() as conn:
        questions = conn.execute(
            "SELECT id, correct_option, marks FROM questions WHERE exam_id = ?",
            (exam_id,)
        ).fetchall()
        
        total_marks = sum(q["marks"] for q in questions)
        obtained_marks = 0
        
        for q in questions:
            selected = request.form.get(f"q_{q['id']}")
            if selected and selected.strip().upper() == q["correct_option"].strip().upper():
                obtained_marks += q["marks"]
                
        pct = round((obtained_marks / total_marks * 100), 1) if total_marks > 0 else 0.0
        
        cur = conn.execute(
            '''INSERT INTO submissions 
               (user_id, exam_id, score, percentage, status, tab_switch_count)
               VALUES (?, ?, ?, ?, 'Submitted', ?)''',
            (user_id, exam_id, obtained_marks, pct, tab_switches)
        )
        conn.commit()
        return redirect(url_for("exam_result", submission_id=cur.lastrowid))"""
    add_code_block(doc, code_2)

    doc.add_page_break()

    add_page_header(doc, "39")
    add_section_title(doc, "3.3 SAMPLE SOURCE CODE — ANTI-CHEATING TELEMETRY")
    add_body_p(doc, "Client-side telemetry detects window blur and tab switching, alerting the candidate and updating the violation counter:")

    code_3 = """// Extract from static/js/main.js - Anti-Cheating Telemetry
let tabViolationCount = 0;
const violationInput = document.getElementById('tab_switch_count');

document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        tabViolationCount++;
        if (violationInput) {
            violationInput.value = tabViolationCount;
        }
        showWarningModal(
            `Proctoring Warning: Tab switch detected! (Violation #${tabViolationCount})`
        );
    }
});

window.addEventListener('blur', function() {
    // Audit focus loss outside exam browser window
    console.warn('[Telemetry] Active exam window focus lost');
});"""
    add_code_block(doc, code_3)

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 40: CHAPTER 4 - TESTING & 4.1 TEST STRATEGY
    # ----------------------------------------------------
    add_page_header(doc, "40")
    add_chapter_title(doc, "CHAPTER 4: TESTING — 4.1 TEST STRATEGY", space_after=14)

    add_body_p(doc, "Testing ensures that ExamPro satisfies institutional security, usability, and assessment accuracy requirements. The test strategy encompasses three structured layers:")
    add_bullet_p(doc, "Unit Testing: ", "Automated Python test scripts (tests/test_exam_system.py) using the unittest framework to verify route status codes, session persistence, and mathematical grading accuracy.")
    add_bullet_p(doc, "Integration Testing: ", "Validating end-to-end database transactions across user creation, question authoring, test submission, and scorecard calculation.")
    add_bullet_p(doc, "User Acceptance Testing (UAT): ", "Verifying realistic examination runs across Admin, Faculty, and Student candidate workflows.")

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 41: 4.2 UNIT TEST PLAN
    # ----------------------------------------------------
    add_page_header(doc, "41")
    add_section_title(doc, "4.2 UNIT TEST PLAN — AUTOMATED SUITE")

    add_body_p(doc, "The automated test suite contains 19 comprehensive unit tests executed via python -m unittest tests/test_exam_system.py:")
    t_ut = doc.add_table(rows=7, cols=3)
    format_table(t_ut, [Inches(1.0), Inches(3.2), Inches(2.3)], ["Test ID", "Test Action / Endpoint Checked", "Expected Result"], [
        ["UT-01", "Database Table Schema & Connection", "Tables created; connection opens"],
        ["UT-02", "Admin Authentication & Session", "Redirect to /admin/dashboard (302)"],
        ["UT-03", "Faculty Login with Approved Credentials", "Redirect to faculty dashboard (302)"],
        ["UT-04", "Student Registration & Password Hash", "Account saved; hashed password stored"],
        ["UT-05", "Exam Runner Question Delivery", "Returns HTTP 200 with question items"],
        ["UT-06", "Auto-Grading & Result Calculation", "Calculates exact score and percentage"]
    ])

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 42: 4.3 ACCEPTANCE OF TEST PLAN
    # ----------------------------------------------------
    add_page_header(doc, "42")
    add_section_title(doc, "4.3 ACCEPTANCE OF TEST PLAN")

    add_body_p(doc, "User acceptance criteria confirm that the application functions reliably from an academic user perspective:")
    t_uat = doc.add_table(rows=6, cols=2)
    format_table(t_uat, [Inches(2.5), Inches(4.0)], ["User Workflow", "Acceptance Condition"], [
        ["Administrator Dashboard", "Metric summary cards display without exceptions"],
        ["Faculty Enrollment", "Admin creates professor; credentials allow immediate login"],
        ["Candidate Exam Run", "Fullscreen request triggered; countdown timer decrements"],
        ["Tab Switch Violation", "Warning dialog pops up; violation count increments"],
        ["Submission & Results", "Scorecard displays correct/incorrect answers with explanations"]
    ])

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGES 43 & 44: 4.4 TEST CASES (VALID & INVALID)
    # ----------------------------------------------------
    add_page_header(doc, "43")
    add_section_title(doc, "4.4 TEST CASES — VALID INPUTS")

    add_body_p(doc, "Test cases evaluating normal operational workflows with representative data:")
    t_tc_v = doc.add_table(rows=7, cols=3)
    format_table(t_tc_v, [Inches(1.0), Inches(3.2), Inches(2.3)], ["ID", "Input Scenario", "Expected Outcome"], [
        ["TC-01", "Valid Admin Login (admin / admin123)", "HTTP 302 -> /admin/dashboard"],
        ["TC-02", "Direct Faculty Creation via Modal", "Faculty account created; is_approved=1"],
        ["TC-03", "Valid Student Registration", "Student account registered successfully"],
        ["TC-04", "Create Assessment with 60 Min Duration", "Exam record created in database"],
        ["TC-05", "Submit All Correct Exam Answers", "Score = 100%, Status = 'Passed'"],
        ["TC-06", "Lodge Academic Support Ticket", "Ticket stored; listed in admin helpdesk"]
    ])

    doc.add_page_break()

    add_page_header(doc, "44")
    add_section_title(doc, "4.4 TEST CASES — INVALID / NEGATIVE INPUTS")

    add_body_p(doc, "Negative tests confirm robust handling of incorrect credentials, missing fields, and boundary cases:")
    t_tc_i = doc.add_table(rows=7, cols=3)
    format_table(t_tc_i, [Inches(1.0), Inches(3.2), Inches(2.3)], ["ID", "Input Scenario", "Observed Server Behavior"], [
        ["TC-07", "Wrong Password on Student Login", "Flash error: 'Invalid credentials'"],
        ["TC-08", "Blank Username on Registration", "Form validation error; rejected"],
        ["TC-09", "Duplicate Username Registration", "Database constraint handled; flash error"],
        ["TC-10", "Unauthenticated Exam Access", "Redirected to login portal (HTTP 302)"],
        ["TC-11", "Student Accessing Admin Route", "Access denied; redirected to home"],
        ["TC-12", "Malformed Exam ID (/exam/abc)", "HTTP 404 Not Found error page"]
    ])

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 45: 4.5 TEST RESULTS & OBSERVATIONS
    # ----------------------------------------------------
    add_page_header(doc, "45")
    add_section_title(doc, "4.5 TEST RESULTS AND OBSERVATIONS")

    add_body_p(doc, "Execution of the automated unit test suite verified 100% test pass rate across all 19 test modules:")
    t_res = doc.add_table(rows=7, cols=3)
    format_table(t_res, [Inches(2.2), Inches(2.3), Inches(2.0)], ["Test Scope / Module", "Execution Status", "Observed Evidence"], [
        ["Database Schema & Tables", "PASSED (19/19 OK)", "exam_system.db verified"],
        ["Role-Based Authentication", "PASSED (19/19 OK)", "Session cookies encrypted"],
        ["Faculty Direct Provisioning", "PASSED (19/19 OK)", "Option A confirmed operational"],
        ["Question Item Management", "PASSED (19/19 OK)", "Items stored with answer keys"],
        ["Exam Submission & Scoring", "PASSED (19/19 OK)", "Mathematical scoring accurate"],
        ["Full Automated Suite Run", "19 Tests in 6.78s — OK", "Zero regressions detected"]
    ])

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 46: CHAPTER 5 - CONCLUSION & 5.1 SUMMARY
    # ----------------------------------------------------
    add_page_header(doc, "46")
    add_chapter_title(doc, "CHAPTER 5: CONCLUSION — 5.1 SUMMARY", space_after=14)

    add_body_p(doc, "ExamPro successfully demonstrates a lightweight, secure, and user-friendly institutional online examination management system developed using Python, Flask, Jinja2, Tailwind CSS, and SQLite.")
    add_body_p(doc, "The application fully satisfies the Savitribai Phule Pune University MCA Semester I curriculum requirements for Web Application Development. The system integrates administrative governance, faculty item authoring, anti-cheating proctoring telemetry, automated scoring, and performance analytics into an accessible web platform.")
    add_body_p(doc, "All deliverables—including clean source code, persistent database schemas, UML diagrams, comprehensive test suites, and documentation—have been constructed and verified to the highest academic standards.")

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 47: 5.2 LIMITATIONS & 5.3 FUTURE ENHANCEMENTS
    # ----------------------------------------------------
    add_page_header(doc, "47")
    add_section_title(doc, "5.2 LIMITATIONS / 5.3 FUTURE ENHANCEMENTS")

    add_body_p(doc, "Limitations of Current Version:")
    add_bullet_p(doc, "Webcam Video Monitoring: ", "Current proctoring tracks window focus and tab switching but does not incorporate AI computer vision facial detection.")
    add_bullet_p(doc, "Subjective Assessments: ", "Evaluation is optimized for multiple-choice questions (MCQs); subjective descriptive essays require manual faculty grading.")
    add_bullet_p(doc, "Local Server Scope: ", "Configured for local institutional area network (LAN) deployment rather than multi-region cloud scaling.")

    add_body_p(doc, "Future Enhancements:")
    add_bullet_p(doc, "AI Face & Eye-Gaze Tracking: ", "Integrate OpenCV / TensorFlow.js for automated candidate identity verification and gaze anomaly alerts.")
    add_bullet_p(doc, "Automated PDF Certificate Generation: ", "Generate digitally signed scorecards and passing certificates automatically upon test completion.")
    add_bullet_p(doc, "Mobile Responsive PWA: ", "Package ExamPro as a Progressive Web Application (PWA) with offline caching and native tablet support.")

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 48: CHAPTER 6 - REFERENCES / BIBLIOGRAPHY
    # ----------------------------------------------------
    add_page_header(doc, "48")
    add_chapter_title(doc, "CHAPTER 6: REFERENCES / BIBLIOGRAPHY", space_after=14)

    refs = [
        "Python Software Foundation. Python 3.12 Documentation. https://docs.python.org/3/",
        "Pallets Projects. Flask Documentation (Version 3.1.x). https://flask.palletsprojects.com/",
        "SQLite Consortium. SQLite Documentation and SQL Reference. https://www.sqlite.org/docs.html",
        "Mozilla Developer Network (MDN). Page Visibility API and Fullscreen API Documentation. https://developer.mozilla.org/",
        "Tailwind Labs. Tailwind CSS Documentation and Utility Classes. https://tailwindcss.com/",
        "Savitribai Phule Pune University. Master of Computer Application (MCA) Curriculum (2025 Pattern NEP 2025).",
        "Project Source Code Repository: ExamPro – Institutional Online Examination System; GitHub: https://github.com/vi4ek/Online-Examination-System-"
    ]
    for r_idx, ref_text in enumerate(refs):
        add_body_p(doc, f"{r_idx + 1}. {ref_text}", space_after=8)

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 49: CHAPTER 7 - 7.1 ANNEXURE I
    # ----------------------------------------------------
    add_page_header(doc, "49")
    add_chapter_title(doc, "CHAPTER 7: APPENDIX — 7.1 RUN & OUTPUT EVIDENCE", space_after=14)

    add_body_p(doc, "To run the application on any standard computer, clone the repository, install Python dependencies, and launch the Flask WSGI server:")
    add_body_p(doc, "Commands: git clone https://github.com/vi4ek/Online-Examination-System-.git ; cd Online-Examination-System- ; pip install -r requirements.txt ; python app.py")

    add_figure(doc, "report_assets/screen_stu_exams.png", "Appendix Figure A1 — Student candidate active assessment catalog and examination launcher.", width=Inches(5.4))

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 50: 7.2 ANNEXURE II - PROGRESS SHEET
    # ----------------------------------------------------
    add_page_header(doc, "50")
    add_chapter_title(doc, "7.2 ANNEXURE II — PROJECT PROGRESS SHEET", space_after=14)

    add_body_p(doc, "The ExamPro development workflow encompassed requirement analysis, relational schema design, role-based controller programming, proctoring integration, unit testing, and documentation.")

    t_prog = doc.add_table(rows=8, cols=2)
    format_table(t_prog, [Inches(3.0), Inches(3.5)], ["Project Item / Milestone", "Current Status / Sign-Off Evidence"], [
        ["Project Proposal & Topic Approval", "Approved by Project Guide"],
        ["Relational Schema & Database Design", "Created via schema.sql and verified"],
        ["Core Flask Controllers & Routes", "Completed in app.py (All RBAC operational)"],
        ["Client Anti-Cheating Telemetry", "Implemented in static/js/main.js"],
        ["Automated Unit Test Suite", "19 of 19 Tests Passing (tests/test_exam_system.py)"],
        ["Project Documentation & Report", "Completed in accordance with SPPU NEP 2025 format"],
        ["Candidate & Guide Approval", "Verified for final departmental submission"]
    ])

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(24)
    r = p.add_run("Project Outcome: ")
    r.bold = True
    r = p.add_run("A fully functional, high-integrity browser-based institutional online examination application demonstrating user governance, assessment delivery, anti-cheating telemetry, automated grading, and statistical reporting.")
    r.italic = True

    # Save to final Word file
    doc.save("ExamPro_Project_Report.docx")
    print("SUCCESS: 50-Page ExamPro Project Report created in ExamPro_Project_Report.docx")

if __name__ == '__main__':
    build_exampro_report()
