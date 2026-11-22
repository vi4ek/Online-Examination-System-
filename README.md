# ExamPro — Institutional Online Examination & Assessment Management System

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask%203.1.3-green.svg)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/database-SQLite%20WAL-orange.svg)](https://www.sqlite.org/)
[![Tests](https://img.shields.io/badge/tests-18%2F18%20passing-brightgreen.svg)](tests/)
[![Institution](https://img.shields.io/badge/Institution-SPPU%20MCA-navy.svg)](http://www.unipune.ac.in/)

**ExamPro** is a role-segregated, full-stack examination and academic assessment web platform developed for the **Department of Master of Computer Applications (MCA)**, Savitribai Phule Pune University (SPPU). 

It features distinct workspaces for **Super Administrators**, **Teaching Faculty/Staff**, and **Student Candidates**, supported by automated grading, question bank management, administrative approvals, and an integrated support ticketing desk.

---

## 1. System Architecture & Portal Overview

```
                                  [ Entrance Hub: http://127.0.0.1:5000/ ]
                                                      │
                       ┌──────────────────────────────┴──────────────────────────────┐
                       ▼                                                             ▼
         [ Faculty & Staff Portal ]                                    [ Student Candidate Portal ]
            /admin/login                                                      /student/login
                 │                                                                 │
        ┌────────┴────────┐                                                        ├── Candidate Workspace (/student/dashboard)
        ▼                 ▼                                                        ├── Available Exams (/student/exams)
[ Super-Admin Console ] [ Staff Exam Studio ]                                      ├── Live Exam Runner (/student/take/<id>)
   /admin/dashboard        /staff/dashboard                                        ├── Assessment History & Scores (/student/history)
   • Staff Approvals       • Exam Builder                                          └── Profile & Security Settings (/student/profile)
   • Student CRUD          • Question Bank
   • Support Desk          • Evaluated Papers
   • System Maintenance    • CSV Export
```

---

## 2. Core Features by Role

### A. Super Administrator (HOD / System Admin)
- **Staff Approval Queue**: Review incoming faculty self-enrollment applications; authorize or reject accounts before privileged access is granted.
- **Student Profile Management (Full CRUD)**:
  - **Create**: Add new students with auto-generated candidate profiles directly from the console modal.
  - **Read**: Live student directory tracking PRN, contact details, total exams taken, and academic average.
  - **Update**: Edit candidate full name, roll number, email address, and phone number.
  - **Reset Password**: Assign new passwords to students in one click.
  - **Delete**: Cascading account cleanup with removal of candidate records and historical submissions.
- **Academic & Technical Support Desk** (`/admin/tickets`):
  - Centralized dashboard to triage student inquiries, lab terminal issues, and mark revaluation requests.
  - Filter tickets by status: **Open**, **In Progress**, **Resolved**, or **All**.
  - Update ticket status and record administrative resolution remarks.
- **System Telemetry & Controls**: Monitor SQLite WAL status, verify foreign key integrity, and trigger database state resets.

### B. Faculty & Teaching Staff
- **Test Management Studio**: Create exams, assign course subjects, configure durations (minutes), set passing thresholds, and publish assessments.
- **Question Bank Repository**: Author multiple-choice questions (MCQs), specify options A–D, designate correct answers, set marks weighting, and add pedagogical explanations.
- **Grading & Analytics Ledger**: Review candidate submissions in real-time, inspect itemized question responses, and export grade sheets to formatted CSV files.

### C. Student Candidate
- **Live Assessment Runner & Browser Lockdown**:
  - Enforced Fullscreen execution mode with modal entry prompt.
  - Active Tab/Window defocus monitoring via `visibilitychange` and `blur` telemetry.
  - 3-Strike Warning Threshold: Displays strike counter alerts; automatically freezes and submits exam on 3rd violation.
  - Restricted Shortcuts: Right-click context menu, clipboard (copy/cut/paste), and developer inspection shortcuts (`F12`, `Ctrl+Shift+I`, `Ctrl+U`) disabled.
  - Synchronized countdown timer, question palette navigation grid, and mark-for-review tracking.
- **Instant Graded Scorecard**: Immediate post-submission breakdown displaying total score, percentage, passing outcome, time taken, and proctoring telemetry audit (tab violations count).
- **Candidate Self-Service**: Dedicated profile page to upload avatar photos, update contact numbers, and change passwords securely.

---

## 3. Technology Stack

- **Backend**: Python 3.12, Flask 3.1.3, Jinja2 Templating
- **Database**: SQLite 3 with Write-Ahead Logging (WAL) and enforced Foreign Key constraints
- **Authentication**: Role-Based Access Control (RBAC) with cryptographic password hashing (Werkzeug PBKDF2/SHA256)
- **Frontend**: Responsive HTML5, Vanilla ES6, and modern Tailwind CSS UI system adhering to institutional design tokens (1120px desktop container, mobile-ready at 375px)
- **Icons & Typography**: Google Material Symbols Outlined, Inter typeface

---

## 4. Default Demo Credentials

The database is pre-seeded with verified test accounts across all three roles:

| Role | Username / Identifier | Password | Portal URL | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Super Admin** | `admin` | `admin123` | [`/admin/login`](http://127.0.0.1:5000/admin/login) | Head of Department & Administrator |
| **Faculty / Staff** | `prof_deshmukh` | `staff123` | [`/admin/login`](http://127.0.0.1:5000/admin/login) | Associate Professor & Active Examiner |
| **Faculty (Pending)** | `prof_kulkarni` | `staff123` | [`/admin/login`](http://127.0.0.1:5000/admin/login) | Awaiting HOD approval on Admin Console |
| **Student** | `aarav` | `student123` | [`/student/login`](http://127.0.0.1:5000/student/login) | Roll No: `MCA2026-001` (Aarav Sharma) |
| **Student** | `pooja` | `student123` | [`/student/login`](http://127.0.0.1:5000/student/login) | Roll No: `MCA2026-002` (Pooja Deshmukh) |
| **Student** | `rohan` | `student123` | [`/student/login`](http://127.0.0.1:5000/student/login) | Roll No: `MCA2026-003` (Rohan Kulkarni) |

---

## 5. Quick Start & Installation

### Prerequisites
- Python 3.10+ (Python 3.12 recommended)
- Git

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/online-examination-system.git
   cd "Online Examination System"
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize and seed the database**:
   ```bash
   python seed_data.py
   ```

5. **Start the application**:
   ```bash
   python app.py
   ```
   The application will be accessible at: **`http://127.0.0.1:5000/`**

---

## 6. Automated Unit Testing

The system includes an extensive automated test suite covering authentication, RBAC boundaries, exam execution, scoring, student CRUD, staff approvals, and ticketing workflows:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Test Suite Execution Output:
```text
test_01_landing_hub ..................................................... ok
test_02_health_endpoints ................................................ ok
test_03_admin_portal_login .............................................. ok
test_04_student_portal_login ............................................ ok
test_05_cross_role_access_restriction ................................... ok
test_06_rbac_student_blocked_from_admin_students_page ................... ok
test_07_student_registration_workflow ................................... ok
test_08_admin_student_roster ............................................ ok
test_09_admin_question_and_exam_management .............................. ok
test_10_student_take_and_submit_exam .................................... ok
test_11_reports_threshold_and_csv_export ................................ ok
test_12_rest_api_suite .................................................. ok
test_13_staff_registration_and_pending_approval ......................... ok
test_14_admin_staff_approval_and_staff_login ............................ ok
test_15_admin_student_management_edit_reset_delete ...................... ok
test_16_student_profile_and_password_change ............................. ok
test_17_support_tickets_lifecycle ....................................... ok
test_18_admin_create_student ............................................ ok
test_19_browser_lock_tab_switches_telemetry ............................. ok

----------------------------------------------------------------------
Ran 19 tests in 8.979s

OK
```

---

## 7. RESTful API Specification (v1)

| Endpoint | Method | Role | Description |
| :--- | :---: | :---: | :--- |
| `/api/v1/health` | `GET` | Public | System status, database connection, and record counts |
| `/api/v1/exams` | `GET` | Authenticated | List all published examinations |
| `/api/v1/exams/<id>` | `GET` | Authenticated | Fetch specific exam specification and question list |
| `/api/v1/exams/<id>/submit` | `POST` | Student | Submit exam responses for automatic grading |
| `/api/v1/submissions/<id>` | `GET` | Candidate/Faculty | Retrieve graded scorecard and response breakdown |

---

## 8. Directory Structure

```text
Online Examination System/
├── app.py                      # Main Flask application and route controllers
├── database.py                 # SQLite WAL connection manager and query helpers
├── schema.sql                  # Relational schema definition (tables, constraints, triggers)
├── seed_data.py                # Database population script with curriculum demo records
├── requirements.txt            # Python runtime dependencies
├── SYNOPSIS.md                 # Academic project synopsis (SPPU MCA curriculum)
├── README.md                   # Complete system documentation
├── static/
│   ├── css/
│   │   ├── style.css           # Custom styling overrides
│   │   └── theme.css           # Institutional color variables
│   ├── images/
│   │   └── sppu_campus.jpg     # SPPU university campus photograph
│   ├── js/
│   │   ├── exam_runner.js      # Client-side timer and auto-save controller
│   │   └── main.js             # General portal interaction scripts
│   └── uploads/avatars/        # Candidate profile avatar uploads
├── templates/
│   ├── base.html               # Shared root HTML shell with Tailwind configuration
│   ├── home.html               # Department landing hub (1120px aligned grid)
│   ├── exams.html              # Faculty exam configuration studio
│   ├── questions.html          # Faculty MCQ question bank authoring
│   ├── reports.html            # Assessment reports ledger and CSV export
│   ├── result.html             # Itemized examination result scorecard
│   ├── exam_runner.html        # Candidate live assessment runner interface
│   ├── admin/
│   │   ├── base_admin.html     # Admin/faculty sidebar and top header layout
│   │   ├── dashboard.html      # Super-Admin console (Staff approvals, Student CRUD, Tickets)
│   │   ├── faculty_dashboard.html # Faculty test management and results overview
│   │   ├── login.html          # Clean neutral #F5F5F7 Faculty Portal login
│   │   ├── staff.html          # Staff approvals and verification directory
│   │   ├── students.html       # Student candidates directory with CRUD operations
│   │   └── tickets.html        # Academic & technical support tickets desk
│   ├── staff/
│   │   ├── login.html          # Staff authentication portal
│   │   └── register.html       # Faculty self-enrollment request form
│   └── student/
│       ├── base_student.html   # Student portal navigation layout
│       ├── dashboard.html      # Candidate dashboard with upcoming exams
│       ├── exams.html          # Enrolled examinations catalog
│       ├── history.html        # Candidate past examination attempts
│       ├── login.html          # Student PRN authentication screen
│       ├── profile.html        # Student candidate profile self-service
│       └── register.html       # Candidate self-registration portal
└── tests/
    └── test_exam_system.py     # 18 comprehensive automated unit tests
```

---

## 9. Academic Affiliation & License

- **Institution**: Department of Master of Computer Applications (MCA), Savitribai Phule Pune University (SPPU), Ganeshkhind, Pune 411007.
- **License**: Educational Project License — open for academic evaluation and institutional extension.
