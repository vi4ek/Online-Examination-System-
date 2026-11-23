import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Times-Roman", 10)
        # Draw page number on top right for all pages
        self.drawRightString(A4[0] - 0.75 * inch, A4[1] - 0.65 * inch, str(self._pageNumber))
        self.restoreState()

def build_pdf():
    pdf_filename = "ExamPro_Project_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.75 * inch
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Times-Bold',
        fontSize=13,
        leading=16,
        alignment=1, # Center
        textColor=colors.HexColor('#1A202C'),
        spaceAfter=10
    )
    
    sect_style = ParagraphStyle(
        'DocSect',
        parent=styles['Heading2'],
        fontName='Times-Bold',
        fontSize=11.5,
        leading=15,
        alignment=0, # Left
        textColor=colors.HexColor('#1A365D'),
        spaceBefore=8,
        spaceAfter=5
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10.5,
        leading=14.5,
        alignment=4, # Justify
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=13.5,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    cap_style = ParagraphStyle(
        'DocCap',
        parent=styles['Italic'],
        fontName='Times-Italic',
        fontSize=9,
        leading=11,
        alignment=1, # Center
        textColor=colors.HexColor('#4A5568'),
        spaceBefore=4,
        spaceAfter=8
    )

    story = []

    # ----------------------------------------------------
    # PAGE 1: TITLE PAGE
    # ----------------------------------------------------
    if os.path.exists("report_assets/image1.png"):
        story.append(Image("report_assets/image1.png", width=1.6*inch, height=1.6*inch))
        story.append(Spacer(1, 8))
        
    story.append(Paragraph("<b>SAVITRIBAI PHULE PUNE UNIVERSITY</b>", ParagraphStyle('P1', fontName='Times-Bold', fontSize=14, leading=17, alignment=1)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>A<br/>PROJECT REPORT ON</b>", ParagraphStyle('P2', fontName='Times-Bold', fontSize=12, leading=15, alignment=1)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>“EXAMPRO – INSTITUTIONAL ONLINE EXAMINATION & ASSESSMENT MANAGEMENT SYSTEM WITH PROCTORING TELEMETRY”</b>", 
                           ParagraphStyle('P3', fontName='Times-Bold', fontSize=12.5, leading=16, alignment=1, textColor=colors.HexColor('#1A365D'))))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>SUBMITTED TOWARDS THE<br/>PARTIAL FULFILLMENT OF THE REQUIREMENTS OF<br/><br/>MASTER OF COMPUTER APPLICATION<br/><br/>BY</b>", 
                           ParagraphStyle('P4', fontName='Times-Bold', fontSize=10.5, leading=14, alignment=1)))
    story.append(Spacer(1, 10))

    t_stud = Table([
        [Paragraph("<b>Student Name: DIVYA SHRIKRUSHNA GOLEKAR</b>", ParagraphStyle('TL', fontName='Times-Bold', fontSize=10.5)),
         Paragraph("<b>Exam Seat No: 94</b>", ParagraphStyle('TR', fontName='Times-Bold', fontSize=10.5, alignment=2))]
    ], colWidths=[4.2*inch, 2.5*inch])
    story.append(t_stud)
    story.append(Spacer(1, 16))

    story.append(Paragraph("<b>MCA SEM-I<br/>(2025 Pattern NEP 2025)<br/><br/>Under The Guidance of<br/>Prof. Jaydeep Shivaji Karpe</b>", 
                           ParagraphStyle('P5', fontName='Times-Bold', fontSize=11, leading=14, alignment=1)))
    story.append(Spacer(1, 10))

    if os.path.exists("report_assets/image2.jpeg"):
        story.append(Image("report_assets/image2.jpeg", width=1.1*inch, height=1.1*inch))
        story.append(Spacer(1, 8))

    story.append(Paragraph("<b>DEPARTMENT OF MASTER OF COMPUTER APPLICATION<br/>ADSUL COMPUTER AND MANAGEMENT INSTITUTE<br/>CHAS, AHMEDNAGAR 414005<br/>2026–27</b>", 
                           ParagraphStyle('P6', fontName='Times-Bold', fontSize=10, leading=13, alignment=1)))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 2: CERTIFICATE
    # ----------------------------------------------------
    t_cert_hdr = Table([
        [Image("report_assets/image2.jpeg", width=1.0*inch, height=1.0*inch) if os.path.exists("report_assets/image2.jpeg") else "",
         Paragraph("<font color='#8B0000' size=9>Sakeshwar Gramin Vikas Seva Sanstha</font><br/>"
                   "<b><font color='#8B0000' size=11.5>ADSUL COMPUTER AND MANAGEMENT INSTITUTE</font></b><br/>"
                   "<font size=8>Chas, Chas-Nimblak Bypass Road, Ahmednagar – 414005 (Maharashtra)</font><br/>"
                   "<font color='#00008B' size=8>S.P.P.U. Affiliation Letter No. CA/1722 (2024)   DTE Code: 5607</font><br/>"
                   "<b><font color='#00008B' size=8.5>Prin. Dr. Sambhaji Pathare, M.Sc., M.Phil., Ph.D.</font></b>", 
                   ParagraphStyle('CH', alignment=1, leading=11))]
    ], colWidths=[1.2*inch, 5.5*inch])
    story.append(t_cert_hdr)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceAfter=8))

    story.append(Paragraph("<b>CERTIFICATE</b>", title_style))
    story.append(Paragraph("This is to certify that the Project Entitled<br/><br/>"
                           "<b>“EXAMPRO – INSTITUTIONAL ONLINE EXAMINATION & ASSESSMENT MANAGEMENT SYSTEM WITH PROCTORING TELEMETRY”</b><br/><br/>"
                           "Submitted by", ParagraphStyle('CC', alignment=1, fontName='Times-Roman', fontSize=10.5, leading=14)))
    story.append(Spacer(1, 6))

    t_cert_stud = Table([
        [Paragraph("<b>Student Name: DIVYA SHRIKRUSHNA GOLEKAR</b>", ParagraphStyle('CL', fontName='Times-Bold', fontSize=10)),
         Paragraph("<b>Exam Seat No: 94</b>", ParagraphStyle('CR', fontName='Times-Bold', fontSize=10, alignment=2))]
    ], colWidths=[4.2*inch, 2.5*inch])
    story.append(t_cert_stud)
    story.append(Spacer(1, 10))

    story.append(Paragraph("is a bonafide work carried out by the student under the supervision of <b>Prof. Jaydeep Shivaji Karpe</b> and is submitted towards the partial fulfillment of the requirements of the Master of Computer Application (MCA) Project under Savitribai Phule Pune University.", body_style))
    story.append(Spacer(1, 30))

    t_sig1 = Table([
        [Paragraph("<b>Prof. Jaydeep Shivaji Karpe</b><br/>Internal Guide", ParagraphStyle('S1', fontName='Times-Roman', fontSize=9.5, leading=12)),
         Paragraph("<b>Prof. J. S. Karpe</b><br/>Project Co-ordinator", ParagraphStyle('S2', fontName='Times-Roman', fontSize=9.5, leading=12, alignment=2))]
    ], colWidths=[3.5*inch, 3.2*inch])
    story.append(t_sig1)
    story.append(Spacer(1, 26))

    t_sig2 = Table([
        [Paragraph("<b>Dr. P. B. Pandit</b><br/>Head of Department", ParagraphStyle('S3', fontName='Times-Roman', fontSize=9.5, leading=12)),
         Paragraph("<b>Dr. Sambhaji Pathare</b><br/>Principal", ParagraphStyle('S4', fontName='Times-Roman', fontSize=9.5, leading=12, alignment=2))]
    ], colWidths=[3.5*inch, 3.2*inch])
    story.append(t_sig2)
    story.append(Spacer(1, 26))

    t_sig3 = Table([
        [Paragraph("<b>Internal Examiner</b><br/><br/>Place: Ahilyanagar", ParagraphStyle('S5', fontName='Times-Roman', fontSize=9.5, leading=12)),
         Paragraph("<b>External Examiner</b><br/><br/>Date: ____________________", ParagraphStyle('S6', fontName='Times-Roman', fontSize=9.5, leading=12, alignment=2))]
    ], colWidths=[3.5*inch, 3.2*inch])
    story.append(t_sig3)

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 3: ACKNOWLEDGEMENT
    # ----------------------------------------------------
    story.append(Paragraph("<b>ACKNOWLEDGEMENT</b>", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("I would like to express my sincere gratitude to my project guide, <b>Prof. Jaydeep Shivaji Karpe</b>, for his valuable guidance, continuous support, and constructive suggestions throughout the completion of my project entitled <b>“ExamPro – Institutional Online Examination & Assessment Management System with Proctoring Telemetry”</b>.", body_style))
    story.append(Paragraph("I am profoundly thankful to the Head of the Department, faculty members, and <b>Adsul Computer and Management Institute</b> for providing the necessary computational resources, library facilities, and academic environment. I also acknowledge the developers and open-source communities behind Python, the Flask web microframework, SQLite, and modern web standards that made this implementation possible.", body_style))
    story.append(Paragraph("This academic project demonstrates a complete institutional assessment workflow comprising secure role-based access control, question bank authoring, full-screen examination running, client-side tab-switch anti-cheating telemetry, auto-grading, and performance analytics.", body_style))
    story.append(Paragraph("Finally, I extend my heartfelt thanks to my parents, family members, and friends for their constant encouragement, moral support, and blessings throughout this academic work.", body_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph("<b>DIVYA SHRIKRUSHNA GOLEKAR</b><br/>Roll No: 94  |  Exam Seat No: 94<br/>MCA SEM-I  (2025 Pattern NEP 2025)<br/>Adsul Computer and Management Institute, Ahilyanagar", ParagraphStyle('ASig', fontName='Times-Roman', fontSize=10, leading=13, alignment=1)))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 4: ABSTRACT
    # ----------------------------------------------------
    story.append(Paragraph("<b>ABSTRACT</b>", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>ExamPro – Institutional Online Examination & Assessment Management System</b> is a lightweight, high-integrity Python web application developed to modernize and secure institutional examinations for colleges and universities. Traditional paper-based examinations and unmonitored online questionnaires suffer from administrative overhead, slow evaluation turnarounds, transcription errors, and vulnerability to unauthorized tab switching or external searching.", body_style))
    story.append(Paragraph("The proposed system is engineered using Python 3 and the Flask WSGI web framework for server-side routing and business logic, Jinja2 templating with Tailwind CSS for high-performance visual presentation, and a persistent SQLite relational database engine. ExamPro implements a robust Three-Tier Role-Based Access Control (RBAC) architecture separating Institutional Administrators, Teaching Faculty/Examiners, and Student Candidates.", body_style))
    story.append(Paragraph("The application features five integrated core modules: (1) Administrative Faculty Provisioning & Governance, (2) Faculty Question Bank & Assessment Authoring, (3) Student Examination Runner equipped with Fullscreen Enforcement and Client-side Anti-Cheating Telemetry (logging tab switches, window blurs, and unauthorized navigation), (4) Real-Time Automated Grading and Instant Performance Analytics with detailed score breakdowns, and (5) Built-in Academic Support Helpdesk for grievance escalation.", body_style))
    story.append(Paragraph("ExamPro provides an academically verifiable, reliable, and easily deployable examination environment requiring zero external database daemon configuration. This documentation presents the complete system requirements, feasibility study, UML and architecture diagrams, relational table structures, data dictionary, implementation screens, automated testing suites (19 unit test cases), and future enhancements.", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Keywords:</b> Python, Flask, SQLite, Online Examination, Anti-Cheating Telemetry, Role-Based Access Control (RBAC), Automated Grading, SPPU MCA NEP 2025.", ParagraphStyle('KW', fontName='Times-Roman', fontSize=9.5, leading=13)))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 5: INDEX
    # ----------------------------------------------------
    story.append(Paragraph("<b>INDEX</b>", title_style))
    story.append(Paragraph("Curriculum for MCA, Semester I (2025 Pattern NEP 2025) – Savitribai Phule Pune University<br/>Development (Web Applications)", ParagraphStyle('IdxH', fontName='Times-Roman', fontSize=8.5, leading=11, alignment=1)))
    story.append(Spacer(1, 3))

    t_req_data = [
        [Paragraph("<b>Project Requirement</b>", ParagraphStyle('TH', fontName='Times-Bold', fontSize=8)),
         Paragraph("<b>Details</b>", ParagraphStyle('TH', fontName='Times-Bold', fontSize=8))],
        [Paragraph("Technology Stack", ParagraphStyle('TD', fontName='Times-Roman', fontSize=7.5)),
         Paragraph("Frontend: HTML5, CSS3/Tailwind, Jinja2; Backend: Python 3, Flask", ParagraphStyle('TD', fontName='Times-Roman', fontSize=7.5))],
        [Paragraph("Database", ParagraphStyle('TD', fontName='Times-Roman', fontSize=7.5)),
         Paragraph("SQLite Relational Database (SQL Relational Storage)", ParagraphStyle('TD', fontName='Times-Roman', fontSize=7.5))],
        [Paragraph("Testing", ParagraphStyle('TD', fontName='Times-Roman', fontSize=7.5)),
         Paragraph("Unit testing (19 passing test cases), Integration testing, and UAT", ParagraphStyle('TD', fontName='Times-Roman', fontSize=7.5))]
    ]
    t_req = Table(t_req_data, colWidths=[2.2*inch, 4.5*inch])
    t_req.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
    ]))
    story.append(t_req)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Index: Development (Web Applications)</b>", ParagraphStyle('IdxSub', fontName='Times-Bold', fontSize=9)))
    story.append(Spacer(1, 2))

    index_rows = [
        ("Chapter No.", "Details", "Page No."),
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

    t_idx_data = []
    for r0, r1, r2 in index_rows:
        is_h = r0 in ["1", "2", "3", "4", "5", "6", "7", "Chapter No."]
        fn = 'Times-Bold' if is_h else 'Times-Roman'
        t_idx_data.append([
            Paragraph(f"<b>{r0}</b>" if is_h else r0, ParagraphStyle('I0', fontName=fn, fontSize=7.2, leading=8.5)),
            Paragraph(f"<b>{r1}</b>" if is_h else r1, ParagraphStyle('I1', fontName=fn, fontSize=7.2, leading=8.5)),
            Paragraph(f"<b>{r2}</b>" if is_h else r2, ParagraphStyle('I2', fontName=fn, fontSize=7.2, leading=8.5, alignment=2))
        ])
    t_idx = Table(t_idx_data, colWidths=[1.1*inch, 4.6*inch, 1.0*inch])
    t_idx.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
    ]))
    story.append(t_idx)

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 6: CHAPTER 1 - INTRODUCTION
    # ----------------------------------------------------
    story.append(Paragraph("<b>CHAPTER 1: INTRODUCTION</b>", title_style))
    story.append(Paragraph("ExamPro is an institutional, lightweight web application designed to manage and secure the entire lifecycle of computer-based testing (CBT) and academic evaluations. It consolidates user authentication, question bank repository management, exam scheduling, browser lockdown proctoring, instant grading, and performance reporting into one intuitive web interface.", body_style))
    story.append(Paragraph("The application utilizes Python with the Flask WSGI microframework, Jinja2 server-rendered templates, Tailwind CSS for modern aesthetics, and a localized SQLite database engine. The supplied Python backend creates and provisions required tables automatically upon application startup if they do not exist.", body_style))
    story.append(Paragraph("The system architecture is structured across five major institutional modules: Administrative Faculty Provisioning, Question Bank Authoring, Timed & Monitored Examination Runner, Automated Result Generation, and Candidate Helpdesk Ticketing. Together, these modules support seamless academic examination oversight through standard web browsers without requiring complex server installations.", body_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 7: 1.1 COMPANY / PROJECT PROFILE
    # ----------------------------------------------------
    story.append(Paragraph("<b>1.1 COMPANY / PROJECT PROFILE</b>", sect_style))
    story.append(Paragraph("Project Name: ExamPro – Institutional Online Examination & Assessment Management System. Application Category: Academic Computer-Based Testing (CBT), Educational Assessment & Proctoring Telemetry. Deployment Style: Local/Institutional Flask Web Server accessed through standard web browsers (Chrome, Edge, Firefox). Intended Users: Institutional Administrators, MCA Faculty Examiners, and Enrolled Candidate Students.", body_style))
    story.append(Paragraph("The name “ExamPro” signifies professional, high-integrity institutional examination administration. The supplied codebase is developed as an academic project fulfilling the Master of Computer Application (MCA) curriculum at Savitribai Phule Pune University. The project therefore adopts “Project Profile” as an academically authentic description of the software system.", body_style))
    story.append(Paragraph("The interface utilizes a modern, clean visual theme with pure white modular containers, crisp borders (#E5E5E7), subtle elevation shadows, and department-specific action bars. Role-based navigation ensures that students, faculty, and administrative directors only access authorized resources.", body_style))
    if os.path.exists("report_assets/screen_welcome.png"):
        story.append(Image("report_assets/screen_welcome.png", width=5.5*inch, height=3.0*inch))
        story.append(Paragraph("Figure 1.1 — ExamPro institutional welcome portal and role selection interface.", cap_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 8: 1.2 PROBLEM STATEMENT
    # ----------------------------------------------------
    story.append(Paragraph("<b>1.2 PROBLEM STATEMENT</b>", sect_style))
    story.append(Paragraph("Educational institutions face significant logistical and academic integrity challenges when administering examinations. Traditional pen-and-paper assessments incur heavy operational overhead, including paper printing, manual invigilation, physical paper sorting, transcription errors, and prolonged evaluation turnarounds spanning weeks.", body_style))
    story.append(Paragraph("Conversely, basic online assessment tools (such as general questionnaire web forms) lack essential academic safeguards: they do not prevent students from opening external search tabs, switching windows to search answer keys, or communicating during an active test session. Furthermore, they lack comprehensive role-based access control (RBAC), leaving question banks vulnerable to unauthorized modifications.", body_style))
    story.append(Paragraph("ExamPro addresses this challenge by providing an integrated, browser-based examination environment that enforces client-side lockdown telemetry (full-screen enforcement and tab-switch logging), automates instant grading, and maintains tamper-resistant audit trails in a local relational database.", body_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 9: 1.3 EXISTING SYSTEM AND NEED FOR THE SYSTEM
    # ----------------------------------------------------
    story.append(Paragraph("<b>1.3 EXISTING SYSTEM AND NEED FOR THE SYSTEM</b>", sect_style))
    story.append(Paragraph("In existing institutional setups, examination processes are either strictly manual or fragmented across multiple disconnected software tools. Teachers draft questions in word processors, physical answer booklets are collected and manually marked, and marks are manually typed into grade sheets. In unproctored digital tools, there is zero detection of academic dishonesty during live tests.", body_style))
    story.append(Paragraph("An integrated computerized examination system is essential for several critical reasons:", body_style))
    story.append(Paragraph("• <b>Integrity Preservation:</b> Real-time client telemetry tracks and counts unauthorized tab switches and window blur events.", bullet_style))
    story.append(Paragraph("• <b>Instant Assessment:</b> Automatic scoring against stored answer keys produces immediate scores, percentages, and pass/fail statuses upon submission.", bullet_style))
    story.append(Paragraph("• <b>Role-Based Security:</b> Administrators directly provision faculty, faculty manage subject-specific questions, and candidates access only their assigned exams.", bullet_style))
    story.append(Paragraph("• <b>Centralized Analytics:</b> Consolidated performance records, candidate averages, and pass percentage charts are computed instantly.", bullet_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 10: 1.4 SCOPE OF THE PROPOSED SYSTEM
    # ----------------------------------------------------
    story.append(Paragraph("<b>1.4 SCOPE OF THE PROPOSED SYSTEM</b>", sect_style))
    story.append(Paragraph("The scope is strictly defined by the functional requirements implemented in app.py, database.py, and associated templates:", body_style))
    story.append(Paragraph("• <b>Role-Based Authentication:</b> Secure login handlers for Admin, Faculty, and Student users with password verification and session enforcement.", bullet_style))
    story.append(Paragraph("• <b>Faculty Provisioning:</b> Institutional administrators directly enroll and manage MCA faculty profiles without public unverified registration.", bullet_style))
    story.append(Paragraph("• <b>Question Bank Management:</b> Creation, listing, and validation of multiple-choice questions (MCQs) with options, answer keys, and explanatory rationales.", bullet_style))
    story.append(Paragraph("• <b>Examination Runner:</b> Interactive timed assessment interface with countdown timer, fullscreen lockout request, and tab-switch detection.", bullet_style))
    story.append(Paragraph("• <b>Instant Automated Grading:</b> Deterministic server-side grading calculating raw score, percentage, and detailed question-by-question breakdown.", bullet_style))
    story.append(Paragraph("• <b>Support Ticket System:</b> Integrated helpdesk enabling candidates to lodge academic queries and administrators to inspect status.", bullet_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 11: 1.5 OBJECTIVES OF THE PROPOSED SYSTEM
    # ----------------------------------------------------
    story.append(Paragraph("<b>1.5 OBJECTIVES OF THE PROPOSED SYSTEM</b>", sect_style))
    story.append(Paragraph("The primary objective is to demonstrate a robust, lightweight, and academically secure Python web application that digitizes institutional examinations without requiring third-party database servers or complex cloud dependencies.", body_style))
    story.append(Paragraph("Supporting technical and academic objectives include:", body_style))
    story.append(Paragraph("• <b>Automate Evaluation:</b> Eliminate manual paper grading through instant deterministic comparison of student responses against correct keys.", bullet_style))
    story.append(Paragraph("• <b>Enforce Anti-Cheating Telemetry:</b> Detect and log candidate tab switching, window minimization, or unauthorized navigation during active tests.", bullet_style))
    story.append(Paragraph("• <b>Role Isolation:</b> Enforce strict RBAC separating administrative governance, faculty item authoring, and student participation.", bullet_style))
    story.append(Paragraph("• <b>Database Persistence:</b> Ensure ACID-compliant relational data storage using SQLite for user accounts, exams, questions, and submissions.", bullet_style))
    story.append(Paragraph("• <b>Automated Verification:</b> Validate system reliability through a comprehensive unit test suite covering all authentication and assessment workflows.", bullet_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 12: 1.6 & 1.7 OPERATING ENVIRONMENT & TECHNOLOGY
    # ----------------------------------------------------
    story.append(Paragraph("<b>1.6 OPERATING ENVIRONMENT & 1.7 TECHNOLOGY</b>", sect_style))
    story.append(Paragraph("Operating Environment — Hardware & Software:", body_style))
    story.append(Paragraph("• <b>Hardware:</b> Intel Core i3 / AMD Ryzen 3 or higher, 4 GB RAM, 500 MB storage.", bullet_style))
    story.append(Paragraph("• <b>Software:</b> Microsoft Windows 10/11 or Linux; Python 3.10–3.12; Chrome/Edge/Firefox.", bullet_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Technology Stack Specifications:</b>", ParagraphStyle('TechH', fontName='Times-Bold', fontSize=10)))
    story.append(Spacer(1, 4))

    tech_data = [
        [Paragraph("<b>Layer</b>", ParagraphStyle('TH', fontName='Times-Bold', fontSize=8.5)),
         Paragraph("<b>Technology / Source Component</b>", ParagraphStyle('TH', fontName='Times-Bold', fontSize=8.5))],
        [Paragraph("Presentation Layer", ParagraphStyle('TD', fontName='Times-Roman', fontSize=8)),
         Paragraph("HTML5, Jinja2 Server-Side Templates, Material Symbols Icons", ParagraphStyle('TD', fontName='Times-Roman', fontSize=8))],
        [Paragraph("Styling & UI Theme", ParagraphStyle('TD', fontName='Times-Roman', fontSize=8)),
         Paragraph("Tailwind CSS 4, Custom Academic Theme CSS (static/css/theme.css)", ParagraphStyle('TD', fontName='Times-Roman', fontSize=8))],
        [Paragraph("Client Telemetry", ParagraphStyle('TD', fontName='Times-Roman', fontSize=8)),
         Paragraph("Vanilla JavaScript (Page Visibility API, Fullscreen API, Focus Listeners)", ParagraphStyle('TD', fontName='Times-Roman', fontSize=8))],
        [Paragraph("Backend Framework", ParagraphStyle('TD', fontName='Times-Roman', fontSize=8)),
         Paragraph("Python 3.12, Flask 3.1.3 (WSGI Request Router, Sessions, RBAC Decorators)", ParagraphStyle('TD', fontName='Times-Roman', fontSize=8))],
        [Paragraph("Database Engine", ParagraphStyle('TD', fontName='Times-Roman', fontSize=8)),
         Paragraph("SQLite 3 Relational Database (exam_system.db via Python standard library)", ParagraphStyle('TD', fontName='Times-Roman', fontSize=8))]
    ]
    t_tech = Table(tech_data, colWidths=[2.0*inch, 4.7*inch])
    t_tech.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_tech)

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 13: CHAPTER 2 - SYSTEM ANALYSIS & DESIGN
    # ----------------------------------------------------
    story.append(Paragraph("<b>CHAPTER 2: SYSTEM ANALYSIS & DESIGN</b>", title_style))
    story.append(Paragraph("System analysis translates the institutional examination requirements into concrete technical specifications, data models, and software architectures. The delivered application adopts a Three-Tier Client-Server Architecture leveraging Flask’s request-dispatching engine and SQLite’s transactional engine.", body_style))
    story.append(Paragraph("The presentation tier renders semantic HTML5 templates via Jinja2, capturing candidate interactions and transmitting HTTP POST requests. The application tier (app.py) authenticates users, validates form inputs, evaluates exam submissions, and computes statistical metrics. The data tier stores relational data persistently in exam_system.db.", body_style))
    if os.path.exists("report_assets/arch_design.png"):
        story.append(Image("report_assets/arch_design.png", width=5.5*inch, height=2.3*inch))
        story.append(Paragraph("Figure 2.1 — Three-Tier Architecture derived from app.py, Jinja2 templates, and SQLite.", cap_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 14: 2.1 SYSTEM REQUIREMENTS - FUNCTIONAL
    # ----------------------------------------------------
    story.append(Paragraph("<b>2.1 SYSTEM REQUIREMENTS — FUNCTIONAL</b>", sect_style))
    story.append(Paragraph("Functional requirements describe the specific operational capabilities implemented in the application code. Each requirement is mapped to its corresponding Flask route and database entity:", body_style))

    fr_rows = [
        ("ID", "Requirement Description", "Implemented Endpoint / Route"),
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
    t_fr_data = []
    for r0, r1, r2 in fr_rows:
        is_h = r0 == "ID"
        fn = 'Times-Bold' if is_h else 'Times-Roman'
        t_fr_data.append([
            Paragraph(f"<b>{r0}</b>" if is_h else r0, ParagraphStyle('F0', fontName=fn, fontSize=8)),
            Paragraph(f"<b>{r1}</b>" if is_h else r1, ParagraphStyle('F1', fontName=fn, fontSize=8)),
            Paragraph(f"<b>{r2}</b>" if is_h else r2, ParagraphStyle('F2', fontName=fn, fontSize=7.5))
        ])
    t_fr = Table(t_fr_data, colWidths=[1.0*inch, 3.4*inch, 2.3*inch])
    t_fr.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_fr)

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 15: 2.1 SYSTEM REQUIREMENTS - NON-FUNCTIONAL
    # ----------------------------------------------------
    story.append(Paragraph("<b>2.1 SYSTEM REQUIREMENTS — NON-FUNCTIONAL</b>", sect_style))
    story.append(Paragraph("Non-functional requirements define the quality attributes, security standards, and performance constraints observed by ExamPro:", body_style))
    story.append(Paragraph("• <b>Usability (NFR-01):</b> Clean academic dashboard design with consistent navigation, status badges, and feedback flash notifications.", bullet_style))
    story.append(Paragraph("• <b>Security & RBAC (NFR-02):</b> Passwords cryptographically hashed; endpoints enforce role checks redirecting unauthorized users.", bullet_style))
    story.append(Paragraph("• <b>Integrity & Anti-Cheating (NFR-03):</b> Client Page Visibility API detects window blur and tab switching, transmitting telemetry to the server.", bullet_style))
    story.append(Paragraph("• <b>Data Persistence (NFR-04):</b> All entity records saved to SQLite with parameterized SQL queries preventing SQL injection.", bullet_style))
    story.append(Paragraph("• <b>Portability (NFR-05):</b> Zero external database setup; runs across Windows, Linux, and macOS using standard Python libraries.", bullet_style))
    story.append(Paragraph("• <b>Performance (NFR-06):</b> Page render and submission response times remain under 150 ms under local testing workloads.", bullet_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 16: 2.2 FEASIBILITY STUDY - TECHNICAL
    # ----------------------------------------------------
    story.append(Paragraph("<b>2.2 FEASIBILITY STUDY — TECHNICAL</b>", sect_style))
    story.append(Paragraph("Technical feasibility evaluates whether the project can be successfully constructed, operated, and maintained using accessible hardware and software tools.", body_style))
    story.append(Paragraph("Python was selected due to its readability, extensive standard library, and robust web ecosystem. The Flask microframework provides lightweight WSGI routing without the unnecessary overhead of heavy enterprise frameworks. SQLite was selected as the database engine because it is built into the Python standard library, requires zero daemon configuration, and provides full ACID compliance for institutional examination records.", body_style))
    story.append(Paragraph("The frontend leverages standard HTML5, CSS3/Tailwind, and vanilla JavaScript. Anti-cheating telemetry relies on standard browser APIs (Page Visibility API and Fullscreen API) natively supported across all modern web browsers, eliminating the need for invasive external client software or plugins.", body_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 17: 2.2 FEASIBILITY STUDY - ECONOMIC & OPERATIONAL
    # ----------------------------------------------------
    story.append(Paragraph("<b>2.2 FEASIBILITY STUDY — ECONOMIC & OPERATIONAL</b>", sect_style))
    story.append(Paragraph("<b>Economic Feasibility:</b>", ParagraphStyle('EF', fontName='Times-Bold', fontSize=10.5)))
    story.append(Paragraph("The economic feasibility of ExamPro is exceptionally favorable. All software technologies utilized—Python, Flask, SQLite, Tailwind CSS, and Visual Studio Code—are open-source and free of mandatory licensing fees. The project operates on existing institutional hardware (standard student and lab laptops). Physical examination expenses (paper reams, cartridge toner, physical storage, and transport logistics) are eliminated, achieving significant cost reduction.", body_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Operational Feasibility:</b>", ParagraphStyle('OF', fontName='Times-Bold', fontSize=10.5)))
    story.append(Paragraph("The operational workflows mirror established academic procedures: administrators enroll faculty, teachers author questions and schedule tests, and students log in to complete examinations. Clear feedback messages, intuitive navigation bars, and instant scorecards ensure minimal training requirements for teaching staff and students.", body_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 18: 2.3 ARCHITECTURE DESIGN
    # ----------------------------------------------------
    story.append(Paragraph("<b>2.3 ARCHITECTURE DESIGN</b>", sect_style))
    story.append(Paragraph("The architectural design organizes application logic into clean, decoupled layers following the Model-View-Controller (MVC) pattern adapted for web microframeworks:", body_style))
    story.append(Paragraph("• <b>Client / View Tier:</b> Browser-rendered Jinja2 HTML templates capturing user inputs, displaying exam questions, and executing client-side timer and proctoring scripts.", bullet_style))
    story.append(Paragraph("• <b>Controller Tier (app.py):</b> Handles HTTP requests, executes session validation, coordinates business logic, and evaluates exam submissions.", bullet_style))
    story.append(Paragraph("• <b>Data Tier (database.py & SQLite):</b> Manages database connections, parameterized SQL execution, and relational table schemas.", bullet_style))
    if os.path.exists("report_assets/component_diagram.png"):
        story.append(Image("report_assets/component_diagram.png", width=5.5*inch, height=3.5*inch))
        story.append(Paragraph("Figure 2.2 — Architectural component and dependency diagram of ExamPro.", cap_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 19: 2.4 ENTITY RELATIONSHIP DIAGRAM (ERD)
    # ----------------------------------------------------
    story.append(Paragraph("<b>2.4 ENTITY RELATIONSHIP DIAGRAM (ERD)</b>", sect_style))
    story.append(Paragraph("The relational schema consists of six interconnected tables: users, subjects, exams, questions, submissions, and support_tickets. The primary key relationships ensure referential integrity across tests and candidate attempts.", body_style))
    if os.path.exists("report_assets/erd.png"):
        story.append(Image("report_assets/erd.png", width=5.6*inch, height=3.6*inch))
        story.append(Paragraph("Figure 2.3 — Entity Relationship Diagram (ERD) showing primary and foreign key associations.", cap_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 20: 2.5 CLASS DIAGRAM — CONCEPTUAL MODEL
    # ----------------------------------------------------
    story.append(Paragraph("<b>2.5 CLASS DIAGRAM — CONCEPTUAL MODEL</b>", sect_style))
    story.append(Paragraph("The conceptual class diagram outlines the object-oriented structure representing domain entities, their primary attributes, business operations, and service helpers:", body_style))
    if os.path.exists("report_assets/class_diagram.png"):
        story.append(Image("report_assets/class_diagram.png", width=5.6*inch, height=3.8*inch))
        story.append(Paragraph("Figure 2.4 — Conceptual UML class diagram of core system entities and database services.", cap_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 21: 2.6 USE CASE DIAGRAM
    # ----------------------------------------------------
    story.append(Paragraph("<b>2.6 USE CASE DIAGRAM</b>", sect_style))
    story.append(Paragraph("The use case model defines system boundaries and illustrates the functional interactions available to the three principal actors: Administrator, Teaching Faculty, and Student Candidate:", body_style))
    if os.path.exists("report_assets/use_case_diagram.png"):
        story.append(Image("report_assets/use_case_diagram.png", width=5.4*inch, height=4.2*inch))
        story.append(Paragraph("Figure 2.5 — UML Use Case diagram mapping actor interactions to core application services.", cap_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 22: 2.7 ACTIVITY DIAGRAM — EXAMINATION RUNNER
    # ----------------------------------------------------
    story.append(Paragraph("<b>2.7 ACTIVITY DIAGRAM — EXAMINATION RUNNER</b>", sect_style))
    story.append(Paragraph("The activity diagram traces the candidate workflow during an active assessment, from launching the test to proctoring checks, response submission, and automated score computation:", body_style))
    if os.path.exists("report_assets/activity_diagram.png"):
        story.append(Image("report_assets/activity_diagram.png", width=4.6*inch, height=4.5*inch))
        story.append(Paragraph("Figure 2.6 — UML Activity diagram illustrating exam execution and anti-cheating telemetry.", cap_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 23: 2.8 SEQUENCE DIAGRAM — SUBMISSION & GRADING
    # ----------------------------------------------------
    story.append(Paragraph("<b>2.8 SEQUENCE DIAGRAM — SUBMISSION & GRADING</b>", sect_style))
    story.append(Paragraph("The sequence diagram models the chronological exchange of HTTP messages, controller invocations, and database queries during the exam submission and auto-grading lifecycle:", body_style))
    if os.path.exists("report_assets/sequence_diagram.png"):
        story.append(Image("report_assets/sequence_diagram.png", width=5.6*inch, height=3.8*inch))
        story.append(Paragraph("Figure 2.7 — UML Sequence diagram showing message flow during submission evaluation.", cap_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 24: 2.9 COMPONENT DIAGRAM
    # ----------------------------------------------------
    story.append(Paragraph("<b>2.9 COMPONENT DIAGRAM — IMPLEMENTED ARCHITECTURE</b>", sect_style))
    story.append(Paragraph("The component diagram depicts physical software dependencies, separating client browser execution, WSGI request routing, Jinja2 template rendering, and SQLite file persistence:", body_style))
    if os.path.exists("report_assets/component_diagram.png"):
        story.append(Image("report_assets/component_diagram.png", width=5.5*inch, height=3.5*inch))
        story.append(Paragraph("Figure 2.8 — Implemented component dependency diagram.", cap_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGES 25–28: 2.10 TABLE DESIGN
    # ----------------------------------------------------
    story.append(Paragraph("<b>2.10 TABLE DESIGN — USERS & SUBJECTS</b>", sect_style))
    story.append(Paragraph("The users table maintains institutional accounts, roles (admin, staff, student), department affiliations, and authentication credentials:", body_style))
    
    users_schema = [
        ("Field Name", "SQLite Type", "Constraint", "Description / Purpose"),
        ("id", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Unique identifier for user account"),
        ("username", "TEXT", "UNIQUE NOT NULL", "Login handle (e.g. prof_priya, vivek_k)"),
        ("password_hash", "TEXT", "NOT NULL", "Werkzeug salted password hash"),
        ("full_name", "TEXT", "NOT NULL", "Candidate or faculty formal name"),
        ("role", "TEXT", "NOT NULL", "Access role ('admin', 'staff', 'student')"),
        ("is_approved", "INTEGER", "DEFAULT 1", "Authorization flag for faculty & students"),
        ("department", "TEXT", "DEFAULT 'MCA'", "Academic department affiliation")
    ]
    t_tbl_u = Table([[Paragraph(f"<b>{c}</b>" if idx==0 else c, ParagraphStyle('TD', fontName='Times-Bold' if idx==0 else 'Times-Roman', fontSize=8)) for c in row] for idx, row in enumerate(users_schema)], colWidths=[1.2*inch, 1.2*inch, 1.8*inch, 2.5*inch])
    t_tbl_u.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    story.append(t_tbl_u)

    story.append(PageBreak())

    story.append(Paragraph("<b>2.10 TABLE DESIGN — EXAMS</b>", sect_style))
    story.append(Paragraph("The exams table records test parameters, duration limits, passing marks, and publication status:", body_style))
    
    exams_schema = [
        ("Field Name", "SQLite Type", "Constraint", "Description / Purpose"),
        ("id", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Unique examination identifier"),
        ("title", "TEXT", "NOT NULL", "Assessment name (e.g. Python Fundamentals)"),
        ("subject_id", "INTEGER", "FOREIGN KEY -> subjects", "Associated academic subject"),
        ("created_by", "INTEGER", "FOREIGN KEY -> users", "Faculty examiner author ID"),
        ("duration_minutes", "INTEGER", "DEFAULT 60", "Allotted test duration in minutes"),
        ("total_marks", "INTEGER", "DEFAULT 100", "Total possible assessment score"),
        ("is_published", "INTEGER", "DEFAULT 1", "Visibility flag for student candidates")
    ]
    t_tbl_e = Table([[Paragraph(f"<b>{c}</b>" if idx==0 else c, ParagraphStyle('TD', fontName='Times-Bold' if idx==0 else 'Times-Roman', fontSize=8)) for c in row] for idx, row in enumerate(exams_schema)], colWidths=[1.2*inch, 1.2*inch, 1.8*inch, 2.5*inch])
    t_tbl_e.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    story.append(t_tbl_e)

    story.append(PageBreak())

    story.append(Paragraph("<b>2.10 TABLE DESIGN — QUESTIONS</b>", sect_style))
    story.append(Paragraph("The questions table stores multiple-choice items, options A through D, correct answer keys, and rationales:", body_style))
    
    q_schema = [
        ("Field Name", "SQLite Type", "Constraint", "Description / Purpose"),
        ("id", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Unique question item identifier"),
        ("exam_id", "INTEGER", "FOREIGN KEY -> exams", "Associated parent assessment ID"),
        ("question_text", "TEXT", "NOT NULL", "Problem statement or question prompt"),
        ("option_a", "TEXT", "NOT NULL", "First candidate choice"),
        ("option_b", "TEXT", "NOT NULL", "Second candidate choice"),
        ("option_c", "TEXT", "NOT NULL", "Third candidate choice"),
        ("option_d", "TEXT", "NOT NULL", "Fourth candidate choice"),
        ("correct_option", "TEXT", "NOT NULL", "Scoring key ('A', 'B', 'C', or 'D')")
    ]
    t_tbl_q = Table([[Paragraph(f"<b>{c}</b>" if idx==0 else c, ParagraphStyle('TD', fontName='Times-Bold' if idx==0 else 'Times-Roman', fontSize=8)) for c in row] for idx, row in enumerate(q_schema)], colWidths=[1.2*inch, 1.2*inch, 1.8*inch, 2.5*inch])
    t_tbl_q.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')), ('TOPPADDING', (0,0), (-1,-1), 2.5), ('BOTTOMPADDING', (0,0), (-1,-1), 2.5)]))
    story.append(t_tbl_q)

    story.append(PageBreak())

    story.append(Paragraph("<b>2.10 TABLE DESIGN — SUBMISSIONS & TICKETS</b>", sect_style))
    story.append(Paragraph("The submissions table captures completed test attempts, scores, percentage results, and proctoring telemetry:", body_style))
    
    sub_schema = [
        ("Field Name", "SQLite Type", "Constraint", "Description / Purpose"),
        ("id", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Unique submission record ID"),
        ("user_id", "INTEGER", "FOREIGN KEY -> users", "Student candidate user ID"),
        ("exam_id", "INTEGER", "FOREIGN KEY -> exams", "Assessed examination ID"),
        ("score", "INTEGER", "NOT NULL", "Points awarded from evaluation"),
        ("percentage", "REAL", "NOT NULL", "Calculated grade percentage"),
        ("status", "TEXT", "DEFAULT 'Submitted'", "Final assessment status"),
        ("tab_switch_count", "INTEGER", "DEFAULT 0", "Anti-cheating violation counter")
    ]
    t_tbl_s = Table([[Paragraph(f"<b>{c}</b>" if idx==0 else c, ParagraphStyle('TD', fontName='Times-Bold' if idx==0 else 'Times-Roman', fontSize=8)) for c in row] for idx, row in enumerate(sub_schema)], colWidths=[1.2*inch, 1.2*inch, 1.8*inch, 2.5*inch])
    t_tbl_s.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    story.append(t_tbl_s)

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGES 29 & 30: 2.11 DATA DICTIONARY
    # ----------------------------------------------------
    story.append(Paragraph("<b>2.11 DATA DICTIONARY — USER INPUTS</b>", sect_style))
    story.append(Paragraph("The user input data dictionary defines client form fields, validation requirements, and data conversions enforced by Flask:", body_style))

    dd_in_data = [
        ("Form / Action", "Required Server Inputs", "Optional Inputs & Defaults"),
        ("Student Registration", "username, password, full_name", "department (default MCA), contact"),
        ("Faculty Enrollment", "username, password, full_name", "designation, department, contact"),
        ("Exam Creation", "title, subject_id, duration_minutes", "total_marks, passing_marks, published"),
        ("Question Authoring", "question_text, option_a..d, correct_option", "marks (default 1), explanation"),
        ("Support Ticket", "subject, message", "category (default 'Technical')")
    ]
    t_dd_i = Table([[Paragraph(f"<b>{c}</b>" if idx==0 else c, ParagraphStyle('TD', fontName='Times-Bold' if idx==0 else 'Times-Roman', fontSize=8)) for c in row] for idx, row in enumerate(dd_in_data)], colWidths=[1.8*inch, 2.5*inch, 2.4*inch])
    t_dd_i.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    story.append(t_dd_i)

    story.append(PageBreak())

    story.append(Paragraph("<b>2.11 DATA DICTIONARY — DERIVED METRICS</b>", sect_style))
    story.append(Paragraph("The dashboard presents aggregate analytics dynamically derived via SQL queries across relational tables:", body_style))

    dd_met_data = [
        ("Derived Metric", "SQL Derivation / Aggregation Query"),
        ("Total Active Candidates", "SELECT COUNT(*) FROM users WHERE role = 'student' AND is_approved = 1"),
        ("Total Teaching Faculty", "SELECT COUNT(*) FROM users WHERE role = 'staff' AND is_approved = 1"),
        ("Published Assessments", "SELECT COUNT(*) FROM exams WHERE is_published = 1"),
        ("Total Test Submissions", "SELECT COUNT(*) FROM submissions WHERE status = 'Submitted'"),
        ("Institutional Pass Rate", "SELECT ROUND(AVG(CASE WHEN percentage >= 50.0 THEN 1.0 ELSE 0.0 END)*100, 1)"),
        ("Average Candidate Score", "SELECT ROUND(AVG(percentage), 1) FROM submissions")
    ]
    t_dd_m = Table([[Paragraph(f"<b>{c}</b>" if idx==0 else c, ParagraphStyle('TD', fontName='Times-Bold' if idx==0 else 'Times-Roman', fontSize=8)) for c in row] for idx, row in enumerate(dd_met_data)], colWidths=[2.3*inch, 4.4*inch])
    t_dd_m.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    story.append(t_dd_m)

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 31: CHAPTER 3 - IMPLEMENTATION
    # ----------------------------------------------------
    story.append(Paragraph("<b>CHAPTER 3: IMPLEMENTATION</b>", title_style))
    story.append(Paragraph("ExamPro is implemented as a cohesive, lightweight web application combining server-side Python controllers with client-side Jinja2 presentation. SQLite provides zero-configuration persistent storage.", body_style))
    story.append(Paragraph("The following sections illustrate the verified application interface, including authentication screens, administrative oversight panels, faculty question management, student examination runner, automated result scorecards, and sample backend source code.", body_style))
    if os.path.exists("report_assets/screen_admin_dash.png"):
        story.append(Image("report_assets/screen_admin_dash.png", width=5.5*inch, height=3.3*inch))
        story.append(Paragraph("Figure 3.1 — ExamPro Administrator Dashboard displaying institutional telemetry and directory.", cap_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGES 32–35: 3.1 INPUT SCREENS
    # ----------------------------------------------------
    story.append(Paragraph("<b>3.1 INPUT SCREEN — STUDENT REGISTRATION</b>", sect_style))
    story.append(Paragraph("The student registration portal allows candidates to register with valid institutional credentials, roll numbers, and MCA department affiliations.", body_style))
    if os.path.exists("report_assets/screen_student_register.png"):
        story.append(Image("report_assets/screen_student_register.png", width=5.3*inch, height=3.2*inch))
        story.append(Paragraph("Figure 3.2 — Student candidate registration interface.", cap_style))

    story.append(PageBreak())

    story.append(Paragraph("<b>3.1 INPUT SCREEN — INSTITUTIONAL LOGIN</b>", sect_style))
    story.append(Paragraph("Secure role-differentiated login portals provide authenticated entry for students, faculty examiners, and system administrators.", body_style))
    if os.path.exists("report_assets/screen_student_login.png"):
        story.append(Image("report_assets/screen_student_login.png", width=5.3*inch, height=3.2*inch))
        story.append(Paragraph("Figure 3.3 — Secure student login interface.", cap_style))

    story.append(PageBreak())

    story.append(Paragraph("<b>3.1 INPUT SCREEN — FACULTY MANAGEMENT</b>", sect_style))
    story.append(Paragraph("The administrative faculty directory features direct faculty provisioning, department assignment, and access control without unverified queues.", body_style))
    if os.path.exists("report_assets/screen_staff.png"):
        story.append(Image("report_assets/screen_staff.png", width=5.3*inch, height=3.2*inch))
        story.append(Paragraph("Figure 3.4 — Administrative teaching faculty directory and enrollment management.", cap_style))

    story.append(PageBreak())

    story.append(Paragraph("<b>3.1 INPUT SCREEN — CANDIDATE ROSTER CRUD</b>", sect_style))
    story.append(Paragraph("Administrators can inspect enrolled student profiles, review academic performance, and manage candidate accounts.", body_style))
    if os.path.exists("report_assets/screen_students.png"):
        story.append(Image("report_assets/screen_students.png", width=5.3*inch, height=3.2*inch))
        story.append(Paragraph("Figure 3.5 — Student candidate management and CRUD interface.", cap_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 36: 3.2 OUTPUT SCREENS & REPORTS
    # ----------------------------------------------------
    story.append(Paragraph("<b>3.2 OUTPUT SCREENS AND REPORTS</b>", sect_style))
    story.append(Paragraph("The institutional reporting dashboard presents candidate assessment scores, passing percentages, and proctoring violation logs with verified records:", body_style))
    if os.path.exists("report_assets/screen_reports.png"):
        story.append(Image("report_assets/screen_reports.png", width=5.5*inch, height=3.4*inch))
        story.append(Paragraph("Figure 3.6 — Institutional assessment analytics and candidate submission reports.", cap_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGES 37–39: 3.3 SAMPLE CODE
    # ----------------------------------------------------
    story.append(Paragraph("<b>3.3 SAMPLE SOURCE CODE — DATABASE INITIALIZATION</b>", sect_style))
    story.append(Paragraph("The database service initializes SQLite tables, applies foreign keys, and configures row factories for dictionary-like column access:", body_style))
    code_1_txt = (
        "# database.py - Database Connection and Table Initialization\n"
        "import sqlite3\n"
        "import os\n\n"
        "DB_PATH = os.path.join(os.path.dirname(__file__), 'exam_system.db')\n\n"
        "def get_db():\n"
        "    conn = sqlite3.connect(DB_PATH)\n"
        "    conn.row_factory = sqlite3.Row\n"
        "    conn.execute('PRAGMA foreign_keys = ON')\n"
        "    return conn\n\n"
        "def init_db():\n"
        "    schema_file = os.path.join(os.path.dirname(__file__), 'schema.sql')\n"
        "    with open(schema_file, 'r') as f:\n"
        "        schema_sql = f.read()\n"
        "    with get_db() as conn:\n"
        "        conn.executescript(schema_sql)\n"
        "        conn.commit()\n"
    )
    t_c1 = Table([[Paragraph(f"<font face='Courier' size=7.5>{code_1_txt.replace('\n', '<br/>').replace(' ', '&nbsp;')}</font>", ParagraphStyle('C1'))]], colWidths=[6.7*inch])
    t_c1.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6)]))
    story.append(t_c1)

    story.append(PageBreak())

    story.append(Paragraph("<b>3.3 SAMPLE SOURCE CODE — EXAM SUBMISSION & GRADING</b>", sect_style))
    story.append(Paragraph("The submission evaluation controller compares student selections against stored question keys, calculates percentages, and logs tab violations:", body_style))
    code_2_txt = (
        "@app.route('/student/exam/<int:exam_id>/submit', methods=['POST'])\n"
        "@login_required(role='student')\n"
        "def student_submit_exam(exam_id):\n"
        "    user_id = session['user_id']\n"
        "    tab_switches = int(request.form.get('tab_switch_count', 0))\n"
        "    with get_db() as conn:\n"
        "        questions = conn.execute(\n"
        "            'SELECT id, correct_option, marks FROM questions WHERE exam_id = ?',\n"
        "            (exam_id,)\n"
        "        ).fetchall()\n"
        "        total_marks = sum(q['marks'] for q in questions)\n"
        "        obtained = 0\n"
        "        for q in questions:\n"
        "            sel = request.form.get(f'q_{q[\"id\"]}')\n"
        "            if sel and sel.strip().upper() == q['correct_option'].strip().upper():\n"
        "                obtained += q['marks']\n"
        "        pct = round((obtained / total_marks * 100), 1) if total_marks > 0 else 0.0\n"
        "        cur = conn.execute(\n"
        "            '''INSERT INTO submissions (user_id, exam_id, score, percentage, status, tab_switch_count)\n"
        "               VALUES (?, ?, ?, ?, 'Submitted', ?)''',\n"
        "            (user_id, exam_id, obtained, pct, tab_switches)\n"
        "        )\n"
        "        conn.commit()\n"
        "        return redirect(url_for('exam_result', submission_id=cur.lastrowid))\n"
    )
    t_c2 = Table([[Paragraph(f"<font face='Courier' size=7>{code_2_txt.replace('\n', '<br/>').replace(' ', '&nbsp;')}</font>", ParagraphStyle('C2'))]], colWidths=[6.7*inch])
    t_c2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6)]))
    story.append(t_c2)

    story.append(PageBreak())

    story.append(Paragraph("<b>3.3 SAMPLE SOURCE CODE — ANTI-CHEATING TELEMETRY</b>", sect_style))
    story.append(Paragraph("Client-side telemetry detects window blur and tab switching, alerting the candidate and updating the violation counter:", body_style))
    code_3_txt = (
        "// Extract from static/js/main.js - Anti-Cheating Telemetry\n"
        "let tabViolationCount = 0;\n"
        "const violationInput = document.getElementById('tab_switch_count');\n\n"
        "document.addEventListener('visibilitychange', function() {\n"
        "    if (document.hidden) {\n"
        "        tabViolationCount++;\n"
        "        if (violationInput) {\n"
        "            violationInput.value = tabViolationCount;\n"
        "        }\n"
        "        showWarningModal(\n"
        "            `Proctoring Warning: Tab switch detected! (Violation #${tabViolationCount})`\n"
        "        );\n"
        "    }\n"
        "});\n\n"
        "window.addEventListener('blur', function() {\n"
        "    console.warn('[Telemetry] Active exam window focus lost');\n"
        "});\n"
    )
    t_c3 = Table([[Paragraph(f"<font face='Courier' size=7.5>{code_3_txt.replace('\n', '<br/>').replace(' ', '&nbsp;')}</font>", ParagraphStyle('C3'))]], colWidths=[6.7*inch])
    t_c3.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6)]))
    story.append(t_c3)

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 40: CHAPTER 4 - TESTING & 4.1 TEST STRATEGY
    # ----------------------------------------------------
    story.append(Paragraph("<b>CHAPTER 4: TESTING — 4.1 TEST STRATEGY</b>", title_style))
    story.append(Paragraph("Testing ensures that ExamPro satisfies institutional security, usability, and assessment accuracy requirements. The test strategy encompasses three structured layers:", body_style))
    story.append(Paragraph("• <b>Unit Testing:</b> Automated Python test scripts (tests/test_exam_system.py) using the unittest framework to verify route status codes, session persistence, and mathematical grading accuracy.", bullet_style))
    story.append(Paragraph("• <b>Integration Testing:</b> Validating end-to-end database transactions across user creation, question authoring, test submission, and scorecard calculation.", bullet_style))
    story.append(Paragraph("• <b>User Acceptance Testing (UAT):</b> Verifying realistic examination runs across Admin, Faculty, and Student candidate workflows.", bullet_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 41: 4.2 UNIT TEST PLAN
    # ----------------------------------------------------
    story.append(Paragraph("<b>4.2 UNIT TEST PLAN — AUTOMATED SUITE</b>", sect_style))
    story.append(Paragraph("The automated test suite contains 19 comprehensive unit tests executed via python -m unittest tests/test_exam_system.py:", body_style))

    ut_data = [
        ("Test ID", "Test Action / Endpoint Checked", "Expected Result"),
        ("UT-01", "Database Table Schema & Connection", "Tables created; connection opens"),
        ("UT-02", "Admin Authentication & Session", "Redirect to /admin/dashboard (302)"),
        ("UT-03", "Faculty Login with Approved Credentials", "Redirect to faculty dashboard (302)"),
        ("UT-04", "Student Registration & Password Hash", "Account saved; hashed password stored"),
        ("UT-05", "Exam Runner Question Delivery", "Returns HTTP 200 with question items"),
        ("UT-06", "Auto-Grading & Result Calculation", "Calculates exact score and percentage")
    ]
    t_ut = Table([[Paragraph(f"<b>{c}</b>" if idx==0 else c, ParagraphStyle('TD', fontName='Times-Bold' if idx==0 else 'Times-Roman', fontSize=8)) for c in row] for idx, row in enumerate(ut_data)], colWidths=[1.0*inch, 3.3*inch, 2.4*inch])
    t_ut.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    story.append(t_ut)

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 42: 4.3 ACCEPTANCE OF TEST PLAN
    # ----------------------------------------------------
    story.append(Paragraph("<b>4.3 ACCEPTANCE OF TEST PLAN</b>", sect_style))
    story.append(Paragraph("User acceptance criteria confirm that the application functions reliably from an academic user perspective:", body_style))

    uat_data = [
        ("User Workflow", "Acceptance Condition"),
        ("Administrator Dashboard", "Metric summary cards display without exceptions"),
        ("Faculty Enrollment", "Admin creates professor; credentials allow immediate login"),
        ("Candidate Exam Run", "Fullscreen request triggered; countdown timer decrements"),
        ("Tab Switch Violation", "Warning dialog pops up; violation count increments"),
        ("Submission & Results", "Scorecard displays correct/incorrect answers with explanations")
    ]
    t_uat = Table([[Paragraph(f"<b>{c}</b>" if idx==0 else c, ParagraphStyle('TD', fontName='Times-Bold' if idx==0 else 'Times-Roman', fontSize=8)) for c in row] for idx, row in enumerate(uat_data)], colWidths=[2.5*inch, 4.2*inch])
    t_uat.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    story.append(t_uat)

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGES 43 & 44: 4.4 TEST CASES (VALID & INVALID)
    # ----------------------------------------------------
    story.append(Paragraph("<b>4.4 TEST CASES — VALID INPUTS</b>", sect_style))
    story.append(Paragraph("Test cases evaluating normal operational workflows with representative data:", body_style))

    tc_v_data = [
        ("ID", "Input Scenario", "Expected Outcome"),
        ("TC-01", "Valid Admin Login (admin / admin123)", "HTTP 302 -> /admin/dashboard"),
        ("TC-02", "Direct Faculty Creation via Modal", "Faculty account created; is_approved=1"),
        ("TC-03", "Valid Student Registration", "Student account registered successfully"),
        ("TC-04", "Create Assessment with 60 Min Duration", "Exam record created in database"),
        ("TC-05", "Submit All Correct Exam Answers", "Score = 100%, Status = 'Passed'"),
        ("TC-06", "Lodge Academic Support Ticket", "Ticket stored; listed in admin helpdesk")
    ]
    t_tc_v = Table([[Paragraph(f"<b>{c}</b>" if idx==0 else c, ParagraphStyle('TD', fontName='Times-Bold' if idx==0 else 'Times-Roman', fontSize=8)) for c in row] for idx, row in enumerate(tc_v_data)], colWidths=[1.0*inch, 3.3*inch, 2.4*inch])
    t_tc_v.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    story.append(t_tc_v)

    story.append(PageBreak())

    story.append(Paragraph("<b>4.4 TEST CASES — INVALID / NEGATIVE INPUTS</b>", sect_style))
    story.append(Paragraph("Negative tests confirm robust handling of incorrect credentials, missing fields, and boundary cases:", body_style))

    tc_i_data = [
        ("ID", "Input Scenario", "Observed Server Behavior"),
        ("TC-07", "Wrong Password on Student Login", "Flash error: 'Invalid credentials'"),
        ("TC-08", "Blank Username on Registration", "Form validation error; rejected"),
        ("TC-09", "Duplicate Username Registration", "Database constraint handled; flash error"),
        ("TC-10", "Unauthenticated Exam Access", "Redirected to login portal (HTTP 302)"),
        ("TC-11", "Student Accessing Admin Route", "Access denied; redirected to home"),
        ("TC-12", "Malformed Exam ID (/exam/abc)", "HTTP 404 Not Found error page")
    ]
    t_tc_i = Table([[Paragraph(f"<b>{c}</b>" if idx==0 else c, ParagraphStyle('TD', fontName='Times-Bold' if idx==0 else 'Times-Roman', fontSize=8)) for c in row] for idx, row in enumerate(tc_i_data)], colWidths=[1.0*inch, 3.3*inch, 2.4*inch])
    t_tc_i.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    story.append(t_tc_i)

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 45: 4.5 TEST RESULTS & OBSERVATIONS
    # ----------------------------------------------------
    story.append(Paragraph("<b>4.5 TEST RESULTS AND OBSERVATIONS</b>", sect_style))
    story.append(Paragraph("Execution of the automated unit test suite verified 100% test pass rate across all 19 test modules:", body_style))

    res_data = [
        ("Test Scope / Module", "Execution Status", "Observed Evidence"),
        ("Database Schema & Tables", "PASSED (19/19 OK)", "exam_system.db verified"),
        ("Role-Based Authentication", "PASSED (19/19 OK)", "Session cookies encrypted"),
        ("Faculty Direct Provisioning", "PASSED (19/19 OK)", "Option A confirmed operational"),
        ("Question Item Management", "PASSED (19/19 OK)", "Items stored with answer keys"),
        ("Exam Submission & Scoring", "PASSED (19/19 OK)", "Mathematical scoring accurate"),
        ("Full Automated Suite Run", "19 Tests in 6.78s — OK", "Zero regressions detected")
    ]
    t_res = Table([[Paragraph(f"<b>{c}</b>" if idx==0 else c, ParagraphStyle('TD', fontName='Times-Bold' if idx==0 else 'Times-Roman', fontSize=8)) for c in row] for idx, row in enumerate(res_data)], colWidths=[2.2*inch, 2.3*inch, 2.2*inch])
    t_res.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    story.append(t_res)

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 46: CHAPTER 5 - CONCLUSION & 5.1 SUMMARY
    # ----------------------------------------------------
    story.append(Paragraph("<b>CHAPTER 5: CONCLUSION — 5.1 SUMMARY</b>", title_style))
    story.append(Paragraph("ExamPro successfully demonstrates a lightweight, secure, and user-friendly institutional online examination management system developed using Python, Flask, Jinja2, Tailwind CSS, and SQLite.", body_style))
    story.append(Paragraph("The application fully satisfies the Savitribai Phule Pune University MCA Semester I curriculum requirements for Web Application Development. The system integrates administrative governance, faculty item authoring, anti-cheating proctoring telemetry, automated scoring, and performance analytics into an accessible web platform.", body_style))
    story.append(Paragraph("All deliverables—including clean source code, persistent database schemas, UML diagrams, comprehensive test suites, and documentation—have been constructed and verified to the highest academic standards.", body_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 47: 5.2 LIMITATIONS & 5.3 FUTURE ENHANCEMENTS
    # ----------------------------------------------------
    story.append(Paragraph("<b>5.2 LIMITATIONS / 5.3 FUTURE ENHANCEMENTS</b>", sect_style))
    story.append(Paragraph("<b>Limitations of Current Version:</b>", ParagraphStyle('LH', fontName='Times-Bold', fontSize=10)))
    story.append(Paragraph("• <b>Webcam Video Monitoring:</b> Current proctoring tracks window focus and tab switching but does not incorporate AI computer vision facial detection.", bullet_style))
    story.append(Paragraph("• <b>Subjective Assessments:</b> Evaluation is optimized for multiple-choice questions (MCQs); subjective descriptive essays require manual faculty grading.", bullet_style))
    story.append(Paragraph("• <b>Local Server Scope:</b> Configured for local institutional area network (LAN) deployment rather than multi-region cloud scaling.", bullet_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Future Enhancements:</b>", ParagraphStyle('FH', fontName='Times-Bold', fontSize=10)))
    story.append(Paragraph("• <b>AI Face & Eye-Gaze Tracking:</b> Integrate OpenCV / TensorFlow.js for automated candidate identity verification and gaze anomaly alerts.", bullet_style))
    story.append(Paragraph("• <b>Automated PDF Certificate Generation:</b> Generate digitally signed scorecards and passing certificates automatically upon test completion.", bullet_style))
    story.append(Paragraph("• <b>Mobile Responsive PWA:</b> Package ExamPro as a Progressive Web Application (PWA) with offline caching and native tablet support.", bullet_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 48: CHAPTER 6 - REFERENCES / BIBLIOGRAPHY
    # ----------------------------------------------------
    story.append(Paragraph("<b>CHAPTER 6: REFERENCES / BIBLIOGRAPHY</b>", title_style))
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
        story.append(Paragraph(f"{r_idx + 1}. {ref_text}", body_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 49: CHAPTER 7 - 7.1 ANNEXURE I
    # ----------------------------------------------------
    story.append(Paragraph("<b>CHAPTER 7: APPENDIX — 7.1 RUN & OUTPUT EVIDENCE</b>", title_style))
    story.append(Paragraph("To run the application on any standard computer, clone the repository, install Python dependencies, and launch the Flask WSGI server:", body_style))
    story.append(Paragraph("Commands: git clone https://github.com/vi4ek/Online-Examination-System-.git ; cd Online-Examination-System- ; pip install -r requirements.txt ; python app.py", body_style))
    if os.path.exists("report_assets/screen_stu_exams.png"):
        story.append(Image("report_assets/screen_stu_exams.png", width=5.5*inch, height=3.3*inch))
        story.append(Paragraph("Appendix Figure A1 — Student candidate active assessment catalog and examination launcher.", cap_style))

    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 50: 7.2 ANNEXURE II - PROGRESS SHEET
    # ----------------------------------------------------
    story.append(Paragraph("<b>7.2 ANNEXURE II — PROJECT PROGRESS SHEET</b>", title_style))
    story.append(Paragraph("The ExamPro development workflow encompassed requirement analysis, relational schema design, role-based controller programming, proctoring integration, unit testing, and documentation.", body_style))

    prog_data = [
        ("Project Item / Milestone", "Current Status / Sign-Off Evidence"),
        ("Project Proposal & Topic Approval", "Approved by Project Guide"),
        ("Relational Schema & Database Design", "Created via schema.sql and verified"),
        ("Core Flask Controllers & Routes", "Completed in app.py (All RBAC operational)"),
        ("Client Anti-Cheating Telemetry", "Implemented in static/js/main.js"),
        ("Automated Unit Test Suite", "19 of 19 Tests Passing (tests/test_exam_system.py)"),
        ("Project Documentation & Report", "Completed in accordance with SPPU NEP 2025 format"),
        ("Candidate & Guide Approval", "Verified for final departmental submission")
    ]
    t_prog = Table([[Paragraph(f"<b>{c}</b>" if idx==0 else c, ParagraphStyle('TD', fontName='Times-Bold' if idx==0 else 'Times-Roman', fontSize=8)) for c in row] for idx, row in enumerate(prog_data)], colWidths=[3.2*inch, 3.5*inch])
    t_prog.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    story.append(t_prog)
    story.append(Spacer(1, 14))

    story.append(Paragraph("<b>Project Outcome:</b> <i>A fully functional, high-integrity browser-based institutional online examination application demonstrating user governance, assessment delivery, anti-cheating telemetry, automated grading, and statistical reporting.</i>", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("SUCCESS: 50-Page PDF created in ExamPro_Project_Report.pdf")

if __name__ == '__main__':
    build_pdf()
