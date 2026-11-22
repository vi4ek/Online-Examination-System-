# PROJECT SYNOPSIS

## 1. Project Title
**ExamPro: Institutional Online Examination and Assessment Management System**  
*Curriculum Pattern: National Education Policy (NEP) 2025 / Choice Based Credit System (CBCS)*  
*Discipline: Master of Computer Applications (MCA)*  
*Affiliation: Savitribai Phule Pune University (SPPU), Pune, Maharashtra*

---

## 2. Introduction & Background
With the transition of higher education towards outcome-based learning and continuous pedagogical evaluation, traditional pen-and-paper assessments face challenges including high logistics overhead, grading latency, paper leakage vulnerabilities, and difficulty in extracting real-time performance analytics. 

**ExamPro** is a secure, role-segregated web-based assessment application designed specifically for the **Department of Master of Computer Applications (MCA)**. It bridges the gap between academic governance, curriculum authoring by faculty, and seamless, distraction-free assessment taking by enrolled student candidates.

---

## 3. Problem Statement & Motivation
Existing commercial learning management systems often lack role clarity, conflating administrative governance with curriculum authoring. Moreover, they either suffer from heavy license fees, complex setup procedures, or insecure self-registration flows where unverified users gain privileged access. 

**Key Challenges Addressed:**
1. **Unverified Faculty Access**: Preventing unapproved user accounts from accessing question banks or creating exams via an administrative verification queue.
2. **Student Identity & Credential Management**: Providing administrators with full CRUD control (Create, Read, Update, Reset Password, Delete) over student profiles and roll numbers (PRN).
3. **Assessment Integrity & Browser Lockdown**: Implementing synchronized timer mechanisms, full-screen lockdown enforcement, tab/window defocus detection with strike limits, shortcut blocking, state caching, and automated grading matrices.
4. **Academic Issue Resolution**: Centralizing student queries and exam dispute inquiries into a structured ticketing system.
5. **Modern, Responsive User Experience**: Delivering a unified, minimalist UI conforming to institutional accessibility standards (1120px grid, responsive down to 375px mobile viewports).

---

## 4. Objectives of the Project
- To design and implement a **Role-Based Access Control (RBAC)** architecture supporting three segregated actor roles: **Super Administrator (HOD)**, **Faculty & Teaching Staff**, and **Student Candidates**.
- To author and maintain categorized **Question Banks** with multiple-choice questions (MCQs), marks weighting, and pedagogical explanations.
- To provide a flexible **Exam Scheduling Engine** that manages duration, pass mark criteria, and automated status publishing.
- To engineer a high-reliability **Live Exam Runner** with countdown timers, persistent response logging, and instant automated grading upon submission.
- To implement comprehensive **Administrative Telemetry** with performance analytics, pass-rate gauges, and one-click tabular CSV exports.
- To maintain an administrative **Support Ticketing Desk** to triage technical issues and academic queries.

---

## 5. System Architecture & Actor Roles

```
                                  [ Public Entrance Hub: / ]
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      ▼                                               ▼
         [ Faculty & Staff Portal ]                      [ Student Candidate Portal ]
               /admin/login                                     /student/login
                      │                                               │
         ┌────────────┴────────────┐                                  ├── Dashboard (/student/dashboard)
         ▼                         ▼                                  ├── Available Tests (/student/exams)
 [ Super-Admin Console ]   [ Staff Exam Studio ]                      ├── Exam Runner (/student/take/<id>)
   /admin/dashboard          /staff/dashboard                         ├── Performance Ledger (/student/history)
   • Staff Approvals         • Manage Tests                           └── Profile & Security (/student/profile)
   • Student Profile CRUD    • Question Bank
   • Support Tickets Desk    • Scorecard Reviews
   • Database Governance     • CSV Grade Export
```

### Role Breakdown:
1. **Super Administrator (Head of Department)**:
   - Evaluates and approves/rejects new faculty registration requests.
   - Performs full CRUD operations on student candidates (view PRN, edit details, reset password, delete record).
   - Oversees the Academic Support Tickets desk, updates ticket statuses, and logs resolution remarks.
   - Monitors institutional metrics and executes system database maintenance.

2. **Faculty / Teaching Staff**:
   - Creates and organizes questions by subject and curriculum module.
   - Schedules and configures exams (title, duration, pass benchmarks, question selection).
   - Monitors student submissions and inspects itemized candidate answer scorecards.
   - Generates and exports assessment grade reports.

3. **Student Candidate**:
   - Accesses assigned term examinations via secure PRN/Roll Number authentication.
   - Executes live assessments in locked fullscreen mode with defocus monitoring.
   - Receives instant post-submission scorecards with percentage calculation and proctoring audit.
   - Manages personal profile details, contact number, avatar, and password self-service.

---

## 6. Functional System Modules (Modular Decomposition)

The system is decomposed into eight cohesive, independently verifiable functional modules:

### Module 1: Authentication & Role-Based Access Control (RBAC)
- Provides dedicated entrance gates: Faculty/Staff Portal (`/admin/login`) and Student Candidate Portal (`/student/login`).
- Session isolation using cryptographic tokens and role-checking decorators (`@admin_required`, `@staff_required`, `@student_required`) preventing cross-role horizontal or vertical privilege escalation.

### Module 2: Faculty & Teaching Staff Provisioning (HOD Governance)
- **Problem Solved**: Eliminates the security risk of public staff self-registration where students could attempt to create unauthorized examiner accounts.
- **Workflow**: Teaching staff accounts are provisioned directly by the Super Administrator (HOD). The administrator specifies the faculty member's full name, academic email, official designation (e.g., Associate Professor, Assistant Professor), department, and initial credentials. Upon creation, faculty accounts are immediately authorized (`is_approved = 1`) to access the Exam Studio.

### Module 3: Student Candidate Identity & Profile Management (CRUD)
- Gives administrators complete authority over student academic accounts:
  - **Create**: Add new student candidate records with assigned Roll Numbers (PRN) and academic emails.
  - **Read**: Live student directory with real-time attempt counts, score averages, and contact filters.
  - **Update**: Modify candidate personal information and contact details.
  - **Reset Password**: Instantly assign new secure passwords to students facing credential lockout.
  - **Delete**: Cascading removal of student accounts and historical records upon graduation or exit.

### Module 4: Curriculum Question Bank & Assessment Scheduling Studio
- **Question Bank**: Authoring categorized multiple-choice questions (MCQs) with options A–D, answer keys, marks weighting, and pedagogical explanations.
- **Exam Builder**: Configures assessment sessions linked to SPPU course codes, setting time limits (minutes), passing benchmarks, and draft/published availability flags.

### Module 5: Browser Lockdown & Anti-Cheat Proctoring Engine
- **Fullscreen Enforcement**: Pre-exam modal agreement requiring entry into locked fullscreen mode before the countdown timer begins.
- **Tab & Window Defocus Monitoring**: Active detection of tab switching, window minimization, or app defocus via `visibilitychange` and `blur` events (with 1.5s debouncing).
- **3-Strike Warning Threshold**: Real-time header badge (`0/3 Strikes`). Violations 1 and 2 display an urgent security dialog; violation 3 terminates the exam with automated auto-submission.
- **Shortcut & Clipboard Lockdown**: Disables right-click context menu, text selection, copy/cut/paste, and developer tools shortcuts (`F12`, `Ctrl+Shift+I`, `Ctrl+U`).

### Module 6: Automated Evaluation & Scorecard Analytics
- Instant server-side response evaluation and percentage grading upon submission.
- Itemized candidate scorecard with question-by-question explanations.
- Administrative reporting dashboard with pass-rate gauges, score distribution metrics, and tabular CSV ledger downloads.

### Module 7: Academic & Technical Support Ticketing Desk
- Provides enrolled students with an integrated helpdesk to raise inquiries categorized by **Technical Issues**, **Exam Disputes**, or **Account Security**.
- Administrative triage queue supporting lifecycle state progression (**Open** &rarr; **In Progress** &rarr; **Resolved** &rarr; **Closed**) with resolution notes.

### Module 8: Candidate Profile & Credential Self-Service
- Allows students to manage profile contact numbers, academic email preferences, and personal avatar photos.
- Secure self-service password update workflow requiring current password verification.

---

## 7. Technical Stack & Implementation Details

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | Python 3.12 / Flask 3.1.3 | RESTful routing, session management, and business logic |
| **Database Engine** | SQLite 3 (WAL Mode) | Relational persistence, transactional safety, and Foreign Key constraints |
| **Security & Auth** | Werkzeug Security (`generate_password_hash`) | Cryptographic salted hashing (PBKDF2/SHA256), session RBAC |
| **Frontend Framework** | HTML5 / Vanilla ES6 / Tailwind CSS | Component architecture, responsive layouts (1120px desktop to 375px mobile) |
| **Typography & Icons** | Inter / Google Material Symbols | High-readability typography and consistent institutional iconography |
| **Testing Harness** | Python `unittest` | Automated regression test suite (19 test scenarios covering all workflows) |

---

## 8. Database Entity-Relationship Overview

The database schema (`schema.sql`) enforces strict foreign keys, cascade rules, and check constraints:
- `users`: Core authentication identity table holding `role` (`admin`, `staff`, `student`), `is_approved`, `contact_number`, and profile details.
- `candidates`: Profile directory linked 1-to-1 with student users, tracking academic roll numbers.
- `subjects`: Curriculum modules aligned with the SPPU MCA course structure.
- `questions`: MCQ repository featuring options A through D, designated correct key, and score weighting.
- `exams`: Configured assessment sessions with duration, passing benchmark, and publication status.
- `exam_questions`: Many-to-many relationship mapping questions into exam schedules.
- `submissions`: Evaluated student attempts recording score, percentage, time elapsed, and pass/fail outcome.
- `submission_answers`: Granular response ledger tracking selected choices per question for auditability.
- `tickets`: Academic and technical support inquiry registry with priority and lifecycle states (`Open`, `In Progress`, `Resolved`, `Closed`).

---

## 9. Quality Assurance & Testing Summary
The system has been verified using a comprehensive automated test suite (`tests/test_exam_system.py`) comprising **19 test cases**:
- **UT-01 to UT-02**: Landing entrance routing and `/health` telemetry endpoints.
- **UT-03 to UT-06**: Dedicated portal authentication and strict cross-role boundary enforcement.
- **UT-07 to UT-08**: Student registration lifecycle and administrative directory tracking.
- **UT-09 to UT-12**: Question authoring, test configuration, live exam execution, scoring, CSV export, and REST API validation.
- **UT-13 to UT-14**: Direct admin faculty provisioning, immediate staff sign-in, and authorized faculty directory management/access revocation.
- **UT-15 to UT-16**: Admin student CRUD operations and candidate profile self-service.
- **UT-17 to UT-18**: Support ticket lifecycle and direct admin candidate enrollment.
- **UT-19**: Anti-cheat browser lock, tab switch violation tracking, strike counters, and scorecard proctoring telemetry.

**Outcome**: 100% test passing rate (`19 passed, 0 failures, 0 errors`).

---

## 10. Conclusion
ExamPro delivers an institutional-grade, pedagogically sound, and secure assessment platform tailored for the Department of Master of Computer Applications (MCA), Savitribai Phule Pune University. It eliminates administrative bottlenecks, protects academic integrity, and provides students with an intuitive, reliable examination interface.
