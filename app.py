"""
Online Examination Management System (ExamPro)
Featuring Strictly Segregated Admin/Faculty and Student Portals with Authentication.
Curriculum for MCA Semester-I — Savitribai Phule Pune University (SPPU)
"""

import os
import csv
import io
import re
from functools import wraps
from datetime import datetime
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    session,
    g,
    Response,
)
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash
from database import (
    get_db,
    close_db,
    query_db,
    modify_db,
    get_dashboard_metrics,
    get_student_roster,
    get_staff_roster,
    get_pending_staff_count,
    get_staff_metrics,
    get_tickets,
    get_ticket_by_id,
    create_ticket,
    update_ticket_status,
    delete_ticket,
    init_db,
)
from seed_data import seed_database

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "exampro-sppu-mca-secret-key-2026")
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB max upload

app.teardown_appcontext(close_db)


# ============================================================================
# Authentication Helpers & Decorators
# ============================================================================

def get_current_user():
    """Retrieves current authenticated user from session or database."""
    user_id = session.get("user_id")
    if not user_id:
        return None
    if "current_user" not in g:
        g.current_user = query_db(
            """SELECT id, username, email, full_name, role, roll_number,
                      contact_number, profile_photo, department, designation,
                      is_approved, created_at
               FROM users WHERE id = ?""",
            (user_id,),
            one=True,
        )
    return g.current_user


@app.context_processor
def inject_global_data():
    """Injects authenticated user and application metadata into all templates."""
    user = get_current_user()
    pending_count = get_pending_staff_count() if user and user.get("role") == "admin" else 0
    return {
        "current_user": user,
        "pending_staff_count": pending_count,
        "current_year": datetime.now().year,
        "app_title": "ExamPro — Online Examination System",
    }


def admin_required(f):
    """Enforces that the user is authenticated specifically as an Admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user or user["role"] != "admin":
            if request.path.startswith("/api/"):
                return jsonify({"success": False, "error": "Admin privileges required"}), 403
            flash("Please sign in with Faculty/Admin credentials to access this console.", "warning")
            return redirect(url_for("admin_login_page"))
        return f(*args, **kwargs)
    return decorated_function


def staff_required(f):
    """Enforces that the user is authenticated as an approved Staff member or Admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user or user["role"] not in ("admin", "staff"):
            if request.path.startswith("/api/"):
                return jsonify({"success": False, "error": "Faculty & Staff authorization required"}), 403
            flash("Please sign in with Faculty & Staff credentials to access this console.", "warning")
            return redirect(url_for("staff_login_page"))
        if user["role"] == "staff" and user.get("is_approved") == 0:
            flash("Your faculty account is pending administrative verification and approval by the Department Head.", "warning")
            return redirect(url_for("staff_login_page"))
        return f(*args, **kwargs)
    return decorated_function


def student_required(f):
    """Enforces that the user is authenticated specifically as an enrolled Student Candidate."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user or user.get("role") != "student":
            if request.path.startswith("/api/"):
                return jsonify({"success": False, "error": "Student candidate authentication required"}), 403
            if user and user.get("role") in ("admin", "staff"):
                flash("Faculty accounts cannot take examinations. Please log in with a student candidate account.", "warning")
                if user["role"] == "admin":
                    return redirect(url_for("admin_dashboard"))
                return redirect(url_for("staff_dashboard"))
            flash("Please sign in with your student account to access the candidate examination portal.", "warning")
            return redirect(url_for("student_login_page"))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# 0. Master Entrance Portal Hub
# ============================================================================

@app.route("/")
def home():
    """Renders the public university home page."""
    return render_template("home.html")


# ============================================================================
# 1. Faculty / Admin Authentication & Dedicated Pages
# ============================================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login_page():
    """Dedicated Faculty Administrator Login."""
    user = get_current_user()
    if user and user["role"] == "admin":
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not (username and password):
            flash("Please enter both username and password.", "danger")
            return render_template("admin/login.html")

        user_match = query_db(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            (username, username),
            one=True,
        )

        if not user_match or not check_password_hash(user_match["password_hash"], password):
            flash("Invalid administrator credentials.", "danger")
            return render_template("admin/login.html")

        if user_match["role"] not in ("admin", "staff"):
            flash("Access denied: This portal is reserved for Faculty/Admin. Please use the Student Portal.", "danger")
            return render_template("admin/login.html")

        if user_match["role"] == "staff":
            if user_match.get("is_approved") == 0:
                flash("Your faculty account is pending administrative verification.", "warning")
                return render_template("admin/login.html")
            session.clear()
            session["user_id"] = user_match["id"]
            session["username"] = user_match["username"]
            session["full_name"] = user_match["full_name"]
            session["role"] = "staff"
            flash(f"Welcome back, {user_match['full_name']}!", "success")
            return redirect(url_for("staff_dashboard"))

        session.clear()
        session["user_id"] = user_match["id"]
        session["username"] = user_match["username"]
        session["full_name"] = user_match["full_name"]
        session["role"] = "admin"

        flash(f"Welcome to Administration Console, {user_match['full_name']}!", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("admin/login.html")


@app.route("/admin/logout")
def admin_logout():
    """Admin logout endpoint."""
    session.clear()
    flash("Faculty Administrator signed out successfully.", "info")
    return redirect(url_for("admin_login_page"))


@app.route("/admin")
@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    """Dedicated Admin Overview Dashboard."""
    metrics = get_dashboard_metrics()
    return render_template("admin/dashboard.html", **metrics)


@app.route("/admin/questions", methods=["GET", "POST"])
@staff_required
def admin_questions_page():
    """Question Bank management for Faculty."""
    if request.method == "POST":
        subject_id = request.form.get("subject_id", "").strip()
        question_text = request.form.get("question_text", "").strip()
        option_a = request.form.get("option_a", "").strip()
        option_b = request.form.get("option_b", "").strip()
        option_c = request.form.get("option_c", "").strip()
        option_d = request.form.get("option_d", "").strip()
        correct_option = request.form.get("correct_option", "").strip().upper()
        marks = request.form.get("marks", "2").strip()
        explanation = request.form.get("explanation", "").strip()

        if not (subject_id and question_text and option_a and option_b and option_c and option_d and correct_option):
            flash("All question fields and four options are required.", "danger")
            return redirect(url_for("admin_questions_page"))

        if correct_option not in ("A", "B", "C", "D"):
            flash("Correct option must be A, B, C, or D.", "danger")
            return redirect(url_for("admin_questions_page"))

        try:
            marks_int = int(marks)
            if marks_int <= 0:
                raise ValueError()
        except ValueError:
            flash("Marks must be a positive integer.", "danger")
            return redirect(url_for("admin_questions_page"))

        modify_db("""
            INSERT INTO questions (subject_id, question_text, option_a, option_b, option_c, option_d, correct_option, marks, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (int(subject_id), question_text, option_a, option_b, option_c, option_d, correct_option, marks_int, explanation))

        flash("Question successfully added to Question Bank.", "success")
        return redirect(url_for("admin_questions_page", subject=subject_id))

    subject_filter = request.args.get("subject", "").strip()
    search_query = request.args.get("q", "").strip()

    subjects = query_db("SELECT id, code, name FROM subjects ORDER BY code")

    query = """
        SELECT q.*, s.name as subject_name, s.code as subject_code
        FROM questions q
        JOIN subjects s ON q.subject_id = s.id
        WHERE 1=1
    """
    params = []
    if subject_filter and subject_filter.isdigit():
        query += " AND q.subject_id = ?"
        params.append(int(subject_filter))
    if search_query:
        query += " AND (q.question_text LIKE ? OR q.explanation LIKE ?)"
        term = f"%{search_query}%"
        params.extend([term, term])

    query += " ORDER BY q.id DESC"
    questions = query_db(query, params)

    return render_template(
        "questions.html",
        questions=questions,
        subjects=subjects,
        selected_subject=subject_filter,
        search_query=search_query,
    )


@app.route("/admin/questions/delete/<int:item_id>", methods=["POST"])
@staff_required
def admin_delete_question(item_id):
    """Deletes a question from Question Bank."""
    modify_db("DELETE FROM questions WHERE id = ?", (item_id,))
    flash("Question deleted successfully.", "success")
    return redirect(url_for("admin_questions_page"))


@app.route("/admin/exams", methods=["GET", "POST"])
@staff_required
def admin_exams_page():
    """Exam scheduling and configuration for Faculty."""
    user = get_current_user()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        subject_id = request.form.get("subject_id", "").strip()
        duration_minutes = request.form.get("duration_minutes", "").strip()
        pass_marks = request.form.get("pass_marks", "").strip()
        instructions = request.form.get("instructions", "").strip()
        selected_question_ids = request.form.getlist("question_ids")

        if not (title and subject_id and duration_minutes and pass_marks):
            flash("Exam title, subject, duration, and pass marks are required.", "danger")
            return redirect(url_for("admin_exams_page"))

        try:
            duration_int = int(duration_minutes)
            pass_marks_int = int(pass_marks)
            if duration_int <= 0 or pass_marks_int < 0:
                raise ValueError()
        except ValueError:
            flash("Duration and Passing Marks must be valid numbers.", "danger")
            return redirect(url_for("admin_exams_page"))

        if not selected_question_ids:
            subject_questions = query_db("SELECT id, marks FROM questions WHERE subject_id = ?", (int(subject_id),))
            if not subject_questions:
                flash("Selected subject has no questions in the bank. Please add questions first.", "danger")
                return redirect(url_for("admin_exams_page"))
            q_ids = [q["id"] for q in subject_questions]
            total_marks = sum(q["marks"] for q in subject_questions)
        else:
            q_ids = [int(qid) for qid in selected_question_ids]
            placeholders = ",".join("?" for _ in q_ids)
            marks_sum = query_db(f"SELECT SUM(marks) as total FROM questions WHERE id IN ({placeholders})", q_ids, one=True)
            total_marks = marks_sum["total"] if marks_sum and marks_sum["total"] else 0

        exam_id, _ = modify_db("""
            INSERT INTO exams (title, subject_id, duration_minutes, total_marks, pass_marks, instructions, status, created_by_user_id)
            VALUES (?, ?, ?, ?, ?, ?, 'Published', ?)
        """, (title, int(subject_id), duration_int, total_marks, pass_marks_int, instructions, user["id"]))

        for qid in q_ids:
            modify_db("INSERT INTO exam_questions (exam_id, question_id) VALUES (?, ?)", (exam_id, qid))

        flash(f"Exam '{title}' successfully configured with {len(q_ids)} questions.", "success")
        return redirect(url_for("admin_exams_page"))

    subjects = query_db("SELECT id, code, name FROM subjects ORDER BY code")
    exams_raw = query_db("""
        SELECT e.*, sub.name as subject_name, sub.code as subject_code,
               COUNT(eq.id) as question_count,
               (SELECT COUNT(*) FROM submissions s WHERE s.exam_id = e.id) as submission_count
        FROM exams e
        JOIN subjects sub ON e.subject_id = sub.id
        LEFT JOIN exam_questions eq ON e.id = eq.exam_id
        GROUP BY e.id
        ORDER BY e.id DESC
    """)

    available_questions = query_db("""
        SELECT q.id, q.subject_id, q.question_text, q.marks, s.code as subject_code
        FROM questions q
        JOIN subjects s ON q.subject_id = s.id
        ORDER BY q.subject_id, q.id
    """)

    return render_template(
        "exams.html",
        exams=exams_raw,
        subjects=subjects,
        available_questions=available_questions,
    )


@app.route("/admin/exams/status/<int:exam_id>", methods=["POST"])
@staff_required
def admin_toggle_exam_status(exam_id):
    """Toggle exam status."""
    new_status = request.form.get("status", "Published")
    modify_db("UPDATE exams SET status = ? WHERE id = ?", (new_status, exam_id))
    flash(f"Exam status updated to {new_status}.", "success")
    return redirect(url_for("admin_exams_page"))


@app.route("/admin/exams/delete/<int:exam_id>", methods=["POST"])
@staff_required
def admin_delete_exam(exam_id):
    """Delete exam if no submissions exist."""
    subs = query_db("SELECT COUNT(*) as count FROM submissions WHERE exam_id = ?", (exam_id,), one=True)
    if subs and subs["count"] > 0:
        flash(f"Cannot delete exam because it has {subs['count']} student submission(s). Archive it instead.", "danger")
        return redirect(url_for("admin_exams_page"))
    modify_db("DELETE FROM exams WHERE id = ?", (exam_id,))
    flash("Exam deleted successfully.", "success")
    return redirect(url_for("admin_exams_page"))


@app.route("/admin/students")
@admin_required
def admin_students_page():
    """Enrolled student candidates directory and performance tracking."""
    search_query = request.args.get("q", "").strip()
    students = get_student_roster()
    if search_query:
        term = search_query.lower()
        students = [
            s for s in students
            if term in (s.get("full_name") or "").lower()
            or term in (s.get("roll_number") or "").lower()
            or term in (s.get("email") or "").lower()
            or term in (s.get("username") or "").lower()
        ]
    return render_template("admin/students.html", students=students, search_query=search_query)


@app.route("/admin/students/<int:student_id>/edit", methods=["POST"])
@admin_required
def admin_edit_student(student_id):
    """Admin modifies student candidate credentials and information."""
    full_name = request.form.get("full_name", "").strip()
    roll_number = request.form.get("roll_number", "").strip().upper()
    email = request.form.get("email", "").strip().lower()
    contact_number = request.form.get("contact_number", "").strip()

    if not (full_name and roll_number and email):
        flash("Name, Roll Number (PRN), and Email are required.", "danger")
        return redirect(url_for("admin_students_page"))

    # Update users table
    modify_db("""
        UPDATE users
        SET full_name = ?, roll_number = ?, email = ?, contact_number = ?
        WHERE id = ? AND role = 'student'
    """, (full_name, roll_number, email, contact_number, student_id))

    # Update candidates table
    modify_db("""
        UPDATE candidates
        SET full_name = ?, roll_number = ?, email = ?, contact_number = ?
        WHERE user_id = ?
    """, (full_name, roll_number, email, contact_number, student_id))

    flash(f"Student candidate '{full_name}' ({roll_number}) updated successfully.", "success")
    return redirect(url_for("admin_students_page"))


@app.route("/admin/students/<int:student_id>/reset-password", methods=["POST"])
@admin_required
def admin_reset_student_password(student_id):
    """Admin sets a new password for a student candidate."""
    new_password = request.form.get("new_password", "").strip()
    if not new_password or len(new_password) < 4:
        flash("Password must be at least 4 characters long.", "danger")
        return redirect(url_for("admin_students_page"))

    pwd_hash = generate_password_hash(new_password)
    modify_db("UPDATE users SET password_hash = ? WHERE id = ? AND role = 'student'", (pwd_hash, student_id))
    flash("Candidate password successfully reset.", "success")
    return redirect(url_for("admin_students_page"))


@app.route("/admin/students/<int:student_id>/delete", methods=["POST"])
@admin_required
def admin_delete_student(student_id):
    """Admin permanently deletes student account and cascaded records."""
    stu = query_db("SELECT full_name, roll_number FROM users WHERE id = ? AND role = 'student'", (student_id,), one=True)
    if not stu:
        flash("Student candidate record not found.", "danger")
        return redirect(url_for("admin_students_page"))

    modify_db("DELETE FROM submissions WHERE user_id = ?", (student_id,))
    modify_db("DELETE FROM candidates WHERE user_id = ?", (student_id,))
    modify_db("DELETE FROM users WHERE id = ? AND role = 'student'", (student_id,))

    flash(f"Candidate {stu['full_name']} ({stu['roll_number']}) and all associated records deleted.", "success")
    return redirect(request.referrer or url_for("admin_students_page"))


@app.route("/admin/students/create", methods=["POST"])
@admin_required
def admin_create_student():
    """Admin registers a new student candidate into the system."""
    full_name = request.form.get("full_name", "").strip()
    roll_number = request.form.get("roll_number", "").strip().upper()
    email = request.form.get("email", "").strip().lower()
    contact_number = request.form.get("contact_number", "").strip()
    password = request.form.get("password", "").strip() or "student123"

    if not (full_name and roll_number and email):
        flash("Student name, roll number (PRN), and email address are required.", "danger")
        return redirect(request.referrer or url_for("admin_students_page"))

    existing = query_db(
        "SELECT id FROM users WHERE username = ? OR email = ? OR roll_number = ?",
        (roll_number.lower(), email, roll_number),
        one=True,
    )
    if existing:
        flash(f"Candidate with roll number {roll_number} or email {email} already exists.", "danger")
        return redirect(request.referrer or url_for("admin_students_page"))

    pwd_hash = generate_password_hash(password)
    user_id, _ = modify_db("""
        INSERT INTO users (username, email, password_hash, full_name, role, roll_number, contact_number, is_approved)
        VALUES (?, ?, ?, ?, 'student', ?, ?, 1)
    """, (roll_number.lower(), email, pwd_hash, full_name, roll_number, contact_number))

    modify_db("""
        INSERT INTO candidates (user_id, roll_number, full_name, email, contact_number)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, roll_number, full_name, email, contact_number))

    flash(f"Candidate '{full_name}' ({roll_number}) enrolled successfully. Initial password: '{password}'.", "success")
    return redirect(request.referrer or url_for("admin_students_page"))


# ============================================================================
# 1.4. Admin Staff Verification & Authorization Console
# ============================================================================

@app.route("/admin/staff")
@admin_required
def admin_staff_page():
    """Admin console to view and manage authorized faculty staff accounts."""
    staff_list = get_staff_roster()
    approved_staff = [s for s in staff_list if s.get("is_approved") == 1]
    return render_template(
        "admin/staff.html",
        approved_staff=approved_staff,
        total_count=len(approved_staff),
    )


@app.route("/admin/staff/create", methods=["POST"])
@admin_required
def admin_create_staff():
    """Admin provisions and enrolls a new faculty / staff member directly."""
    full_name = request.form.get("full_name", "").strip()
    department = request.form.get("department", "Department of MCA").strip()
    designation = request.form.get("designation", "Assistant Professor").strip()
    email = request.form.get("email", "").strip().lower()
    contact_number = request.form.get("contact_number", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip() or "staff123"

    if not (full_name and email and username and password):
        flash("Please complete all required fields (Name, Username, Email, Password).", "danger")
        return redirect(url_for("admin_staff_page"))

    existing = query_db(
        "SELECT * FROM users WHERE username = ? OR email = ?",
        (username, email),
        one=True,
    )
    if existing:
        if existing["username"] == username:
            flash("Username already exists in portal.", "danger")
        else:
            flash("An account with this email address already exists.", "danger")
        return redirect(url_for("admin_staff_page"))

    pwd_hash = generate_password_hash(password)
    modify_db("""
        INSERT INTO users (username, email, password_hash, full_name, role, contact_number, department, designation, is_approved)
        VALUES (?, ?, ?, ?, 'staff', ?, ?, ?, 1)
    """, (username, email, pwd_hash, full_name, contact_number, department, designation))

    flash(f"Faculty member {full_name} enrolled successfully with active privileges.", "success")
    return redirect(request.referrer or url_for("admin_staff_page"))


@app.route("/admin/staff/<int:user_id>/approve", methods=["POST"])
@admin_required
def admin_approve_staff(user_id):
    """Admin approves a staff account."""
    modify_db("UPDATE users SET is_approved = 1 WHERE id = ? AND role = 'staff'", (user_id,))
    flash("Faculty/Staff account has been verified and authorized successfully.", "success")
    return redirect(request.referrer or url_for("admin_staff_page"))


@app.route("/admin/staff/<int:user_id>/reject", methods=["POST"])
@admin_required
def admin_reject_staff(user_id):
    """Admin rejects and deletes an unapproved staff registration."""
    modify_db("DELETE FROM users WHERE id = ? AND role = 'staff' AND is_approved = 0", (user_id,))
    flash("Staff registration request has been rejected and removed.", "info")
    return redirect(request.referrer or url_for("admin_staff_page"))


@app.route("/admin/staff/<int:user_id>/delete", methods=["POST"])
@admin_required
def admin_delete_staff(user_id):
    """Admin removes an existing staff account."""
    modify_db("DELETE FROM users WHERE id = ? AND role = 'staff'", (user_id,))
    flash("Faculty/Staff account removed from portal.", "success")
    return redirect(request.referrer or url_for("admin_staff_page"))


# ============================================================================
# 1.5. Academic & Technical Support Tickets Management
# ============================================================================

@app.route("/admin/tickets")
@admin_required
def admin_tickets_page():
    """Admin console to view, track, and resolve academic & technical support tickets."""
    status_filter = request.args.get("status", "all").strip()
    tickets_list = get_tickets(None if status_filter.lower() == "all" else status_filter)
    all_tickets = get_tickets()
    open_cnt = sum(1 for t in all_tickets if t["status"] == "Open")
    in_prog_cnt = sum(1 for t in all_tickets if t["status"] == "In Progress")
    resolved_cnt = sum(1 for t in all_tickets if t["status"] == "Resolved")

    return render_template(
        "admin/tickets.html",
        tickets=tickets_list,
        status_filter=status_filter,
        open_count=open_cnt,
        in_progress_count=in_prog_cnt,
        resolved_count=resolved_cnt,
        total_count=len(all_tickets),
    )


@app.route("/admin/tickets/<int:ticket_id>/status", methods=["POST"])
@admin_required
def admin_update_ticket_status(ticket_id):
    """Admin updates ticket status and resolution remarks."""
    new_status = request.form.get("status", "Open").strip()
    notes = request.form.get("resolution_notes", "").strip()

    if new_status not in ("Open", "In Progress", "Resolved", "Closed"):
        flash("Invalid ticket status.", "danger")
        return redirect(request.referrer or url_for("admin_tickets_page"))

    update_ticket_status(ticket_id, new_status, notes or None)
    flash(f"Ticket #{ticket_id} status updated to '{new_status}'.", "success")
    return redirect(request.referrer or url_for("admin_tickets_page"))


@app.route("/admin/tickets/<int:ticket_id>/delete", methods=["POST"])
@admin_required
def admin_delete_ticket(ticket_id):
    """Admin deletes a support ticket."""
    delete_ticket(ticket_id)
    flash(f"Ticket #{ticket_id} removed.", "info")
    return redirect(request.referrer or url_for("admin_tickets_page"))


@app.route("/tickets/create", methods=["POST"])
def submit_support_ticket():
    """Allows authenticated candidates, staff, or visitors to submit inquiries."""
    user = get_current_user()
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    subject = request.form.get("subject", "").strip()
    category = request.form.get("category", "Academic Support").strip()
    message = request.form.get("message", "").strip()
    priority = request.form.get("priority", "Medium").strip()

    if user:
        user_id = user["id"]
        name = name or user["full_name"]
        email = email or user["email"]
        user_role = user["role"]
    else:
        user_id = None
        user_role = "student"

    if not (name and email and subject and message):
        flash("Name, email, subject, and description are required.", "danger")
        return redirect(request.referrer or url_for("home"))

    create_ticket(user_id, name, email, user_role, subject, category, message, priority)
    flash("Support inquiry ticket registered successfully. Department administration has been notified.", "success")
    return redirect(request.referrer or url_for("home"))


@app.route("/admin/reports")
@staff_required
def admin_reports_page():
    """Academic assessment reports."""
    exam_filter = request.args.get("exam", "").strip()
    status_filter = request.args.get("status", "").strip()
    search_query = request.args.get("q", "").strip()

    exams = query_db("SELECT id, title FROM exams ORDER BY id")

    query = """
        SELECT s.*, e.title as exam_title, e.pass_marks,
               sub.name as subject_name, sub.code as subject_code,
               c.roll_number, c.full_name, c.email
        FROM submissions s
        JOIN exams e ON s.exam_id = e.id
        JOIN subjects sub ON e.subject_id = sub.id
        JOIN candidates c ON s.candidate_id = c.id
        WHERE 1=1
    """
    params = []

    if exam_filter and exam_filter.isdigit():
        query += " AND s.exam_id = ?"
        params.append(int(exam_filter))

    if status_filter in ("Passed", "Failed"):
        query += " AND s.status = ?"
        params.append(status_filter)

    if search_query:
        query += " AND (c.roll_number LIKE ? OR c.full_name LIKE ? OR c.email LIKE ?)"
        term = f"%{search_query}%"
        params.extend([term, term, term])

    query += " ORDER BY s.submitted_at DESC"
    submissions = query_db(query, params)

    return render_template(
        "reports.html",
        submissions=submissions,
        exams=exams,
        selected_exam=exam_filter,
        selected_status=status_filter,
        search_query=search_query,
    )


@app.route("/admin/reports/export.csv")
@staff_required
def admin_export_reports_csv():
    """Export assessment records to CSV."""
    submissions = query_db("""
        SELECT s.id, c.roll_number, c.full_name, c.email, e.title as exam_title,
               sub.code as subject_code, s.score, s.total_marks, s.percentage,
               s.status, s.tab_switches_count, s.time_taken_seconds, s.submitted_at
        FROM submissions s
        JOIN exams e ON s.exam_id = e.id
        JOIN subjects sub ON e.subject_id = sub.id
        JOIN candidates c ON s.candidate_id = c.id
        ORDER BY s.id ASC
    """)

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow([
        "Submission ID", "Roll Number", "Candidate Name", "Email",
        "Exam Title", "Subject Code", "Score Obtained", "Total Marks",
        "Percentage (%)", "Result Status", "Tab Switches (Violations)", "Time Taken (Seconds)", "Submitted Timestamp"
    ])

    for row in submissions:
        cw.writerow([
            row["id"], row["roll_number"], row["full_name"], row["email"],
            row["exam_title"], row["subject_code"], row["score"], row["total_marks"],
            row["percentage"], row["status"], row.get("tab_switches_count", 0), row["time_taken_seconds"], row["submitted_at"]
        ])

    output = io.BytesIO(si.getvalue().encode("utf-8"))
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=exampro_assessment_records.csv"}
    )


@app.route("/admin/result/<int:submission_id>")
@app.route("/staff/result/<int:submission_id>")
@staff_required
def admin_view_result(submission_id):
    """View candidate scorecard as Admin or Faculty Staff."""
    return exam_result_common(submission_id)


@app.route("/result/<int:submission_id>")
def view_submission_result(submission_id):
    """General view submission result endpoint."""
    return exam_result_common(submission_id)


# ============================================================================
# 1.5. Academic Staff & Faculty Authentication & Dedicated Workflows
# ============================================================================

@app.route("/staff/login", methods=["GET", "POST"])
def staff_login_page():
    """Dedicated Faculty & Staff Login."""
    user = get_current_user()
    if user:
        if user["role"] == "admin":
            return redirect(url_for("admin_dashboard"))
        if user["role"] == "staff" and user.get("is_approved") == 1:
            return redirect(url_for("staff_dashboard"))

    if request.method == "POST":
        identifier = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not (identifier and password):
            flash("Please enter both username/email and password.", "danger")
            return render_template("staff/login.html")

        staff_user = query_db(
            "SELECT * FROM users WHERE (username = ? OR email = ?)",
            (identifier, identifier.lower()),
            one=True,
        )

        if not staff_user or not check_password_hash(staff_user["password_hash"], password):
            flash("Invalid faculty credentials. Please re-check your username/email and password.", "danger")
            return render_template("staff/login.html")

        if staff_user["role"] == "student":
            flash("This portal is reserved for Academic Staff & Faculty. Candidates should sign in via Student Examination Portal.", "warning")
            return redirect(url_for("student_login_page"))

        if staff_user["role"] == "admin":
            session.clear()
            session["user_id"] = staff_user["id"]
            session["username"] = staff_user["username"]
            session["role"] = staff_user["role"]
            session["full_name"] = staff_user["full_name"]
            flash(f"Welcome to Administration Console, {staff_user['full_name']}!", "success")
            return redirect(url_for("admin_dashboard"))

        if staff_user["role"] == "staff":
            if staff_user.get("is_approved") == 0:
                flash("Your faculty/staff account has been registered but is awaiting administrative verification and approval by the Department Head. You will receive access once approved.", "warning")
                return render_template("staff/login.html", pending_approval=True)

            session.clear()
            session["user_id"] = staff_user["id"]
            session["username"] = staff_user["username"]
            session["role"] = staff_user["role"]
            session["full_name"] = staff_user["full_name"]
            flash(f"Welcome back, {staff_user['full_name']}!", "success")
            return redirect(url_for("staff_dashboard"))

    return render_template("staff/login.html")


@app.route("/staff/register", methods=["GET", "POST"])
def staff_register_page():
    """Faculty accounts are provisioned directly by Admin; redirect to faculty login."""
    flash("Faculty accounts are provisioned directly by the Department Administrator. Please contact your HOD for credentials.", "info")
    return redirect(url_for("admin_login_page"))


@app.route("/staff/dashboard")
@staff_required
def staff_dashboard():
    """Dedicated Staff & Faculty Overview Dashboard for exam management, question authoring, and results review."""
    metrics = get_dashboard_metrics()
    return render_template("admin/faculty_dashboard.html", **metrics)


@app.route("/staff/logout")
def staff_logout():
    """Staff logout endpoint."""
    session.clear()
    flash("You have been signed out from the Faculty & Staff Console.", "info")
    return redirect(url_for("staff_login_page"))


@app.route("/staff/exams")
@staff_required
def staff_exams_page():
    """Staff interface for scheduled examinations."""
    exams = query_db("""
        SELECT e.*, s.name as subject_name, s.code as subject_code,
               COUNT(eq.id) as question_count
        FROM exams e
        JOIN subjects s ON e.subject_id = s.id
        LEFT JOIN exam_questions eq ON e.id = eq.exam_id
        GROUP BY e.id
        ORDER BY e.id DESC
    """)
    subjects = query_db("SELECT id, name, code FROM subjects ORDER BY code ASC")
    return render_template("exams.html", exams=exams, subjects=subjects, is_staff_view=True)


@app.route("/staff/questions", methods=["GET", "POST"])
@staff_required
def staff_questions_page():
    """Staff interface for Question Bank authoring."""
    return admin_questions_page()


@app.route("/staff/reports")
@staff_required
def staff_reports_page():
    """Staff interface for examination analytics & score reviews."""
    return admin_reports_page()


# ============================================================================
# 2. Student Authentication & Dedicated Pages
# ============================================================================

@app.route("/student/login", methods=["GET", "POST"])
def student_login_page():
    """Dedicated Student Candidate Login."""
    user = get_current_user()
    if user and user["role"] == "student":
        return redirect(url_for("student_dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not (username and password):
            flash("Please enter both username/roll number and password.", "danger")
            return render_template("student/login.html")

        user_match = query_db("""
            SELECT * FROM users
            WHERE username = ? OR email = ? OR roll_number = ?
        """, (username, username, username.upper()), one=True)

        if not user_match or not check_password_hash(user_match["password_hash"], password):
            flash("Invalid candidate credentials.", "danger")
            return render_template("student/login.html")

        if user_match["role"] != "student":
            flash("Faculty account detected. Please sign in via the Faculty Portal.", "info")
            return redirect(url_for("admin_login_page"))

        session.clear()
        session["user_id"] = user_match["id"]
        session["username"] = user_match["username"]
        session["full_name"] = user_match["full_name"]
        session["role"] = "student"
        session["roll_number"] = user_match["roll_number"]

        flash(f"Welcome back, {user_match['full_name']}!", "success")
        return redirect(url_for("student_dashboard"))

    return render_template("student/login.html")


@app.route("/student/register", methods=["GET", "POST"])
def student_register_page():
    """Student Self-Registration Portal."""
    if get_current_user():
        return redirect(url_for("student_dashboard"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        roll_number = request.form.get("roll_number", "").strip().upper()
        email = request.form.get("email", "").strip().lower()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not (full_name and roll_number and email and username and password):
            flash("All fields are mandatory for student registration.", "danger")
            return render_template("student/register.html")

        existing = query_db("""
            SELECT username, email, roll_number FROM users
            WHERE username = ? OR email = ? OR roll_number = ?
        """, (username, email, roll_number), one=True)

        if existing:
            if existing["username"] == username:
                flash("Username is already taken.", "danger")
            elif existing["email"] == email:
                flash("An account with this email already exists.", "danger")
            else:
                flash("This roll number is already registered.", "danger")
            return render_template("student/register.html")

        pwd_hash = generate_password_hash(password)
        user_id, _ = modify_db("""
            INSERT INTO users (username, email, password_hash, full_name, role, roll_number)
            VALUES (?, ?, ?, ?, 'student', ?)
        """, (username, email, pwd_hash, full_name, roll_number))

        modify_db("""
            INSERT INTO candidates (user_id, roll_number, full_name, email)
            VALUES (?, ?, ?, ?)
        """, (user_id, roll_number, full_name, email))

        session.clear()
        session["user_id"] = user_id
        session["username"] = username
        session["full_name"] = full_name
        session["role"] = "student"
        session["roll_number"] = roll_number

        flash("Registration successful! You are now logged in.", "success")
        return redirect(url_for("student_dashboard"))

    return render_template("student/register.html")


@app.route("/student/logout")
def student_logout():
    """Student logout endpoint."""
    session.clear()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for("student_login_page"))


@app.route("/student/profile")
@student_required
def student_profile_page():
    """Candidate profile view & personal settings."""
    user = get_current_user()
    cand = query_db("SELECT * FROM candidates WHERE user_id = ?", (user["id"],), one=True)
    stats = query_db("""
        SELECT COUNT(id) as attempts,
               SUM(CASE WHEN status = 'Passed' THEN 1 ELSE 0 END) as passed,
               ROUND(AVG(percentage), 1) as avg_score
        FROM submissions
        WHERE user_id = ?
    """, (user["id"],), one=True)
    return render_template("student/profile.html", user=user, candidate=cand, stats=stats)


@app.route("/student/profile/update", methods=["POST"])
@student_required
def student_update_profile():
    """Updates candidate contact info and uploads profile picture."""
    user = get_current_user()
    email = request.form.get("email", "").strip().lower()
    contact_number = request.form.get("contact_number", "").strip()

    if not email:
        flash("Academic email cannot be empty.", "danger")
        return redirect(url_for("student_profile_page"))

    profile_photo_filename = user.get("profile_photo")

    # Handle optional avatar upload
    if "profile_photo" in request.files:
        file = request.files["profile_photo"]
        if file and file.filename:
            ext = file.filename.rsplit(".", 1)[-1].lower()
            if ext in {"png", "jpg", "jpeg", "gif", "webp"}:
                import time
                filename = f"avatar_{user['id']}_{int(time.time())}.{ext}"
                upload_dir = BASE_DIR / "static" / "uploads" / "avatars"
                upload_dir.mkdir(parents=True, exist_ok=True)
                file.save(str(upload_dir / filename))
                profile_photo_filename = filename
            else:
                flash("Invalid file format. Please upload PNG, JPG, or WEBP.", "danger")
                return redirect(url_for("student_profile_page"))

    # Update users table
    modify_db("""
        UPDATE users
        SET email = ?, contact_number = ?, profile_photo = ?
        WHERE id = ?
    """, (email, contact_number, profile_photo_filename, user["id"]))

    # Update candidates table
    modify_db("""
        UPDATE candidates
        SET email = ?, contact_number = ?, profile_photo = ?
        WHERE user_id = ?
    """, (email, contact_number, profile_photo_filename, user["id"]))

    flash("Profile updated successfully.", "success")
    return redirect(url_for("student_profile_page"))


@app.route("/student/profile/change-password", methods=["POST"])
@student_required
def student_change_password():
    """Allows student to change their password securely."""
    user = get_current_user()
    current_password = request.form.get("current_password", "").strip()
    new_password = request.form.get("new_password", "").strip()
    confirm_password = request.form.get("confirm_password", "").strip()

    full_user = query_db("SELECT password_hash FROM users WHERE id = ?", (user["id"],), one=True)
    if not check_password_hash(full_user["password_hash"], current_password):
        flash("Current password is incorrect.", "danger")
        return redirect(url_for("student_profile_page"))

    if len(new_password) < 4:
        flash("New password must be at least 4 characters long.", "danger")
        return redirect(url_for("student_profile_page"))

    if new_password != confirm_password:
        flash("New password and confirm password do not match.", "danger")
        return redirect(url_for("student_profile_page"))

    new_hash = generate_password_hash(new_password)
    modify_db("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user["id"]))
    flash("Password updated successfully.", "success")
    return redirect(url_for("student_profile_page"))


@app.route("/student")
@app.route("/student/dashboard")
@student_required
def student_dashboard():
    """Student Personal Assessment Dashboard."""
    user = get_current_user()

    available_exams = query_db("""
        SELECT e.id, e.title, e.duration_minutes, e.total_marks, e.pass_marks,
               s.name as subject_name, s.code as subject_code,
               COUNT(eq.id) as question_count
        FROM exams e
        JOIN subjects s ON e.subject_id = s.id
        LEFT JOIN exam_questions eq ON e.id = eq.exam_id
        WHERE e.status = 'Published'
        GROUP BY e.id
        HAVING question_count > 0
        ORDER BY e.id DESC
    """)

    my_submissions = query_db("""
        SELECT s.*, e.title as exam_title, sub.name as subject_name, sub.code as subject_code
        FROM submissions s
        JOIN exams e ON s.exam_id = e.id
        JOIN subjects sub ON e.subject_id = sub.id
        WHERE s.user_id = ?
        ORDER BY s.submitted_at DESC
    """, (user["id"],))

    total_attempts = len(my_submissions)
    passed_attempts = sum(1 for s in my_submissions if s["status"] == "Passed")
    avg_score = round(sum(s["percentage"] for s in my_submissions) / total_attempts, 1) if total_attempts > 0 else 0.0

    return render_template(
        "student/dashboard.html",
        user=user,
        available_exams=available_exams,
        my_submissions=my_submissions,
        stats={
            "total_attempts": total_attempts,
            "passed_attempts": passed_attempts,
            "avg_score": avg_score,
        }
    )


@app.route("/student/exams")
@student_required
def student_exams_page():
    """Available examinations for students to select and commence."""
    available_exams = query_db("""
        SELECT e.id, e.title, e.duration_minutes, e.total_marks, e.pass_marks,
               e.instructions, s.name as subject_name, s.code as subject_code,
               COUNT(eq.id) as question_count
        FROM exams e
        JOIN subjects s ON e.subject_id = s.id
        LEFT JOIN exam_questions eq ON e.id = eq.exam_id
        WHERE e.status = 'Published'
        GROUP BY e.id
        HAVING question_count > 0
        ORDER BY e.id DESC
    """)
    return render_template("student/exams.html", exams=available_exams)


@app.route("/student/take/<int:exam_id>")
@student_required
def student_take_exam(exam_id):
    """Commences live assessment runner for the authenticated student."""
    user = get_current_user()

    exam = query_db("""
        SELECT e.*, s.name as subject_name, s.code as subject_code
        FROM exams e
        JOIN subjects s ON e.subject_id = s.id
        WHERE e.id = ? AND e.status = 'Published'
    """, (exam_id,), one=True)

    if not exam:
        flash("Exam not found or is currently not published.", "danger")
        return redirect(url_for("student_exams_page"))

    questions = query_db("""
        SELECT q.id, q.question_text, q.option_a, q.option_b, q.option_c, q.option_d, q.marks
        FROM questions q
        JOIN exam_questions eq ON q.id = eq.question_id
        WHERE eq.exam_id = ?
        ORDER BY eq.id ASC
    """, (exam_id,))

    if not questions:
        flash("This exam has no questions configured.", "danger")
        return redirect(url_for("student_exams_page"))

    # Ensure candidate record exists
    candidate = query_db("SELECT id, roll_number, full_name, email FROM candidates WHERE user_id = ?", (user["id"],), one=True)
    roll_number = user.get("roll_number") or (candidate["roll_number"] if candidate else f"ROLL-{user['id']:04d}")
    full_name = user.get("full_name") or (candidate["full_name"] if candidate else user.get("username", "Candidate"))
    email = user.get("email") or (candidate["email"] if candidate else f"{user.get('username', 'user')}@acmi.edu.in")

    if not candidate:
        cid, _ = modify_db("""
            INSERT INTO candidates (user_id, roll_number, full_name, email)
            VALUES (?, ?, ?, ?)
        """, (user["id"], roll_number, full_name, email))
        candidate_id = cid
    else:
        candidate_id = candidate["id"]
        roll_number = candidate.get("roll_number") or roll_number
        full_name = candidate.get("full_name") or full_name

    session["exam_id"] = exam_id
    session["candidate_id"] = candidate_id
    session["exam_start_time"] = datetime.now().isoformat()

    return render_template(
        "exam_runner.html",
        exam=exam,
        questions=questions,
        candidate={
            "roll_number": roll_number,
            "full_name": full_name,
        },
    )


@app.route("/student/submit", methods=["POST"])
@app.route("/exam/submit", methods=["POST"])
@student_required
def student_submit_exam():
    """Evaluates exam responses, computes score and passes, returns JSON redirect."""
    user = get_current_user()
    data = request.get_json(silent=True) or request.form

    exam_id = int(data.get("exam_id", session.get("exam_id") or 0))
    time_taken = int(data.get("time_taken_seconds", 0))
    tab_switches_count = int(data.get("tab_switches_count", 0))
    raw_answers = data.get("answers", {})

    user_id = user["id"] if user else session.get("user_id")
    candidate_id = session.get("candidate_id")

    if not candidate_id and user_id:
        c = query_db("SELECT id FROM candidates WHERE user_id = ?", (user_id,), one=True)
        if c:
            candidate_id = c["id"]
        else:
            u = user or query_db("SELECT * FROM users WHERE id = ?", (user_id,), one=True)
            if u:
                roll = u.get("roll_number") or f"MCA2026-{user_id:03d}"
                name = u.get("full_name") or u.get("username", "Candidate")
                email = u.get("email") or f"{u.get('username', 'user')}@acmi.edu.in"
                cid, _ = modify_db("""
                    INSERT INTO candidates (user_id, roll_number, full_name, email)
                    VALUES (?, ?, ?, ?)
                """, (user_id, roll, name, email))
                candidate_id = cid
        if candidate_id:
            session["candidate_id"] = candidate_id

    if not exam_id or not candidate_id:
        return jsonify({"success": False, "error": "Invalid exam session"}), 400

    exam = query_db("SELECT * FROM exams WHERE id = ?", (exam_id,), one=True)
    if not exam:
        return jsonify({"success": False, "error": "Exam not found"}), 404

    questions = query_db("""
        SELECT q.id, q.correct_option, q.marks
        FROM questions q
        JOIN exam_questions eq ON q.id = eq.question_id
        WHERE eq.exam_id = ?
    """, (exam_id,))

    total_exam_marks = sum(q["marks"] for q in questions)
    total_score = 0
    recorded_answers = []

    for q in questions:
        qid_str = str(q["id"])
        selected = raw_answers.get(qid_str)
        if selected:
            selected = selected.strip().upper()
            if selected not in ("A", "B", "C", "D"):
                selected = None

        is_correct = 1 if (selected and selected == q["correct_option"]) else 0
        marks_awarded = q["marks"] if is_correct else 0
        total_score += marks_awarded

        recorded_answers.append({
            "question_id": q["id"],
            "selected_option": selected,
            "is_correct": is_correct,
            "marks_awarded": marks_awarded,
        })

    percentage = round((total_score / total_exam_marks * 100), 2) if total_exam_marks > 0 else 0.0
    status = "Passed" if total_score >= exam["pass_marks"] else "Failed"

    submission_id, _ = modify_db("""
        INSERT INTO submissions (exam_id, candidate_id, user_id, score, total_marks, percentage, status, time_taken_seconds, tab_switches_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (exam_id, candidate_id, user_id, total_score, total_exam_marks, percentage, status, time_taken, tab_switches_count))

    for item in recorded_answers:
        modify_db("""
            INSERT INTO submission_answers (submission_id, question_id, selected_option, is_correct, marks_awarded)
            VALUES (?, ?, ?, ?, ?)
        """, (submission_id, item["question_id"], item["selected_option"], item["is_correct"], item["marks_awarded"]))

    session.pop("exam_id", None)
    session.pop("exam_start_time", None)

    return jsonify({
        "success": True,
        "submission_id": submission_id,
        "redirect_url": url_for("student_view_result", submission_id=submission_id),
    })


@app.route("/student/result/<int:submission_id>")
@app.route("/result/<int:submission_id>")
def student_view_result(submission_id):
    """Candidate Scorecard & Review."""
    return exam_result_common(submission_id)


@app.route("/student/history")
@student_required
def student_history_page():
    """Archive of all scorecards for current student."""
    user = get_current_user()
    submissions = query_db("""
        SELECT s.*, e.title as exam_title, sub.name as subject_name, sub.code as subject_code
        FROM submissions s
        JOIN exams e ON s.exam_id = e.id
        JOIN subjects sub ON e.subject_id = sub.id
        WHERE s.user_id = ?
        ORDER BY s.submitted_at DESC
    """, (user["id"],))

    return render_template("student/history.html", submissions=submissions)


def exam_result_common(submission_id):
    """Shared helper for rendering scorecards."""
    user = get_current_user()
    submission = query_db("""
        SELECT s.*, e.title as exam_title, e.pass_marks,
               sub.name as subject_name, sub.code as subject_code,
               c.roll_number, c.full_name, c.email
        FROM submissions s
        JOIN exams e ON s.exam_id = e.id
        JOIN subjects sub ON e.subject_id = sub.id
        JOIN candidates c ON s.candidate_id = c.id
        WHERE s.id = ?
    """, (submission_id,), one=True)

    if not submission:
        flash("Submission record not found.", "danger")
        return redirect(url_for("home"))

    review_items = query_db("""
        SELECT sa.*, q.question_text, q.option_a, q.option_b, q.option_c, q.option_d,
               q.correct_option, q.explanation, q.marks as max_marks
        FROM submission_answers sa
        JOIN questions q ON sa.question_id = q.id
        WHERE sa.submission_id = ?
        ORDER BY sa.id ASC
    """, (submission_id,))

    correct_count = sum(1 for item in review_items if item["is_correct"] == 1)
    wrong_count = sum(1 for item in review_items if item["selected_option"] and item["is_correct"] == 0)
    unanswered_count = sum(1 for item in review_items if not item["selected_option"])

    is_admin_view = bool(user and user.get("role") == "admin" and request.path.startswith("/admin"))

    return render_template(
        "result.html",
        sub=submission,
        review_items=review_items,
        is_admin_view=is_admin_view,
        stats={
            "total_questions": len(review_items),
            "correct_count": correct_count,
            "wrong_count": wrong_count,
            "unanswered_count": unanswered_count,
        }
    )


@app.route("/result/<int:submission_id>/download")
@app.route("/student/result/<int:submission_id>/download")
@app.route("/admin/result/<int:submission_id>/download")
def download_result_csv(submission_id):
    """Generates and downloads official candidate scorecard CSV transcript."""
    submission = query_db("""
        SELECT s.*, e.title as exam_title, e.pass_marks,
               sub.name as subject_name, sub.code as subject_code,
               c.roll_number, c.full_name, c.email
        FROM submissions s
        JOIN exams e ON s.exam_id = e.id
        JOIN subjects sub ON e.subject_id = sub.id
        JOIN candidates c ON s.candidate_id = c.id
        WHERE s.id = ?
    """, (submission_id,), one=True)

    if not submission:
        flash("Submission record not found for download.", "danger")
        return redirect(url_for("home"))

    review_items = query_db("""
        SELECT sa.*, q.question_text, q.option_a, q.option_b, q.option_c, q.option_d,
               q.correct_option, q.explanation, q.marks as max_marks
        FROM submission_answers sa
        JOIN questions q ON sa.question_id = q.id
        WHERE sa.submission_id = ?
        ORDER BY sa.id ASC
    """, (submission_id,))

    output = io.StringIO()
    writer = csv.writer(output)

    # Institutional Header
    writer.writerow(["SAVITRIBAI PHULE PUNE UNIVERSITY - ACMI AHMEDNAGAR"])
    writer.writerow(["DEPARTMENT OF MASTER OF COMPUTER APPLICATION (NEP 2025 PATTERN)"])
    writer.writerow(["OFFICIAL STUDENT ASSESSMENT SCORECARD & TRANSCRIPT"])
    writer.writerow([])

    # Candidate & Exam Information
    writer.writerow(["Candidate Name", submission["full_name"]])
    writer.writerow(["Exam Seat / Roll No", submission["roll_number"]])
    writer.writerow(["Academic Email", submission["email"]])
    writer.writerow(["Examination Title", submission["exam_title"]])
    writer.writerow(["Curriculum Subject", f"{submission['subject_code']}: {submission['subject_name']}"])
    writer.writerow(["Submission ID", f"SUB-{submission['id']:04d}"])
    writer.writerow(["Submission Timestamp", submission["submitted_at"]])
    duration_str = f"{submission['time_taken_seconds'] // 60}m {submission['time_taken_seconds'] % 60}s"
    writer.writerow(["Duration Taken", duration_str])
    writer.writerow(["Score Obtained", f"{submission['score']} / {submission['total_marks']}"])
    writer.writerow(["Percentage", f"{submission['percentage']}%"])
    writer.writerow(["Pass Benchmark", f"{submission['pass_marks']} Marks"])
    writer.writerow(["Final Result", submission["status"].upper()])
    proctoring_status = f"{submission['tab_switches_count']} Tab Switch Violations Recorded" if submission.get("tab_switches_count") else "Clean (0 Violations) - Browser Locked"
    writer.writerow(["Proctoring Status", proctoring_status])
    writer.writerow([])

    # Question Breakdown Table
    writer.writerow(["Question #", "Question Text", "Candidate Answer", "Correct Key", "Status", "Marks Awarded", "Max Marks", "Academic Explanation"])
    for idx, item in enumerate(review_items, 1):
        status_text = "CORRECT" if item["is_correct"] == 1 else ("INCORRECT" if item["selected_option"] else "UNANSWERED")
        writer.writerow([
            idx,
            item["question_text"],
            item["selected_option"] or "None",
            item["correct_option"],
            status_text,
            item["marks_awarded"],
            item["max_marks"],
            item["explanation"] or "-"
        ])

    csv_data = output.getvalue()
    clean_roll = re.sub(r'[^A-Za-z0-9_-]', '_', submission["roll_number"] or "CAND")
    filename = f"Scorecard_{clean_roll}_Exam{submission['exam_id']}.csv"

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


# ============================================================================
# 3. Compatibility Aliases (Ensures all existing paths work seamlessly)
# ============================================================================

@app.route("/login")
def login_page():
    return redirect(url_for("student_login_page"))

@app.route("/register")
def register_page():
    return redirect(url_for("student_register_page"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/questions")
def questions_page():
    return redirect(url_for("admin_questions_page"))

@app.route("/exams")
def exams_page():
    return redirect(url_for("admin_exams_page"))

@app.route("/reports")
def reports_page():
    return redirect(url_for("admin_reports_page"))

@app.route("/portal")
def candidate_portal():
    return redirect(url_for("student_exams_page"))

@app.route("/exam/run/<int:exam_id>")
def exam_runner(exam_id):
    return redirect(url_for("student_take_exam", exam_id=exam_id))

@app.route("/exam/start", methods=["POST", "GET"])
def start_exam():
    exam_id = request.form.get("exam_id") or request.args.get("exam_id")
    if not exam_id:
        return redirect(url_for("student_exams_page"))

    current_u = get_current_user()
    if current_u and current_u.get("role") == "admin":
        flash("Faculty accounts cannot take student examinations. Please log in with an enrolled student account.", "warning")
        return redirect(url_for("admin_dashboard"))

    # If roll_number or email is provided on entrance form
    roll_number = (request.form.get("roll_number") or "").strip().upper()
    email = (request.form.get("email") or "").strip().lower()
    full_name = (request.form.get("full_name") or "").strip()

    if not current_u and (roll_number or email):
        u = None
        if roll_number:
            u = query_db("SELECT * FROM users WHERE roll_number = ? AND role = 'student'", (roll_number,), one=True)
        if not u and email:
            u = query_db("SELECT * FROM users WHERE email = ? AND role = 'student'", (email,), one=True)
        if u:
            session["user_id"] = u["id"]
        else:
            uname = roll_number.lower().replace("-", "") if roll_number else (email.split("@")[0] if email else "candidate")
            from werkzeug.security import generate_password_hash
            new_uid, _ = modify_db("""
                INSERT INTO users (username, email, password_hash, full_name, role, roll_number)
                VALUES (?, ?, ?, ?, 'student', ?)
            """, (uname, email or f"{uname}@acmi.edu.in", generate_password_hash("student123"), full_name or "Enrolled Candidate", roll_number or "MCA2026-999"))
            session["user_id"] = new_uid

    try:
        return redirect(url_for("student_take_exam", exam_id=int(exam_id)))
    except (ValueError, TypeError):
        return redirect(url_for("student_exams_page"))


# ============================================================================
# 4. RESTful API Suite (API v1)
# ============================================================================

@app.route("/health")
@app.route("/api/v1/health")
def api_health():
    """Health check endpoint for automated testing."""
    try:
        metrics = get_dashboard_metrics()
        return jsonify({
            "success": True,
            "status": "healthy",
            "service": "ExamPro Online Examination System",
            "database": "connected",
            "timestamp": datetime.now().isoformat(),
            "counts": {
                "exams": metrics["total_exams"],
                "questions": metrics["total_questions"],
                "candidates": metrics["total_candidates"],
                "submissions": metrics["total_submissions"],
            }
        }), 200
    except Exception as e:
        return jsonify({"success": False, "status": "unhealthy", "error": str(e)}), 500


@app.route("/api/v1/auth/login", methods=["POST"])
def api_login():
    """API endpoint for JSON authentication."""
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not (username and password):
        return jsonify({"success": False, "error": "Username and password required"}), 400

    user = query_db("SELECT * FROM users WHERE username = ? OR email = ?", (username, username), one=True)
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"success": False, "error": "Invalid credentials"}), 401

    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["role"] = user["role"]

    return jsonify({
        "success": True,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "full_name": user["full_name"],
            "email": user["email"],
            "role": user["role"],
            "roll_number": user["roll_number"],
        }
    }), 200


@app.route("/api/v1/auth/me")
def api_me():
    """API endpoint to get current authenticated profile."""
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "authenticated": False}), 401
    return jsonify({"success": True, "authenticated": True, "user": user})


@app.route("/api/v1/subjects", methods=["GET"])
def api_get_subjects():
    """API endpoint to list curriculum subjects."""
    subjects = query_db("""
        SELECT s.*, COUNT(q.id) as question_count
        FROM subjects s
        LEFT JOIN questions q ON s.id = q.subject_id
        GROUP BY s.id
        ORDER BY s.code
    """)
    return jsonify({"success": True, "data": subjects})


@app.route("/api/v1/questions", methods=["GET", "POST"])
def api_questions():
    """API endpoint to list or create questions."""
    if request.method == "POST":
        user = get_current_user()
        if not user or user["role"] != "admin":
            return jsonify({"success": False, "error": "Admin privileges required"}), 403

        data = request.get_json(silent=True) or {}
        subject_id = data.get("subject_id")
        q_text = data.get("question_text", "").strip()
        opt_a = data.get("option_a", "").strip()
        opt_b = data.get("option_b", "").strip()
        opt_c = data.get("option_c", "").strip()
        opt_d = data.get("option_d", "").strip()
        correct = data.get("correct_option", "").strip().upper()
        marks = int(data.get("marks", 2))
        explanation = data.get("explanation", "").strip()

        if not (subject_id and q_text and opt_a and opt_b and opt_c and opt_d and correct in ("A", "B", "C", "D")):
            return jsonify({"success": False, "error": "Invalid question input payload"}), 400

        qid, _ = modify_db("""
            INSERT INTO questions (subject_id, question_text, option_a, option_b, option_c, option_d, correct_option, marks, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (subject_id, q_text, opt_a, opt_b, opt_c, opt_d, correct, marks, explanation))

        return jsonify({"success": True, "question_id": qid, "message": "Question created"}), 201

    subject_id = request.args.get("subject_id")
    if subject_id:
        questions = query_db("SELECT * FROM questions WHERE subject_id = ? ORDER BY id DESC", (subject_id,))
    else:
        questions = query_db("SELECT * FROM questions ORDER BY id DESC")

    return jsonify({"success": True, "data": questions})


@app.route("/api/v1/exams", methods=["GET"])
def api_get_exams():
    """API endpoint to retrieve exams list."""
    exams = query_db("""
        SELECT e.*, s.name as subject_name, s.code as subject_code,
               COUNT(eq.id) as question_count
        FROM exams e
        JOIN subjects s ON e.subject_id = s.id
        LEFT JOIN exam_questions eq ON e.id = eq.exam_id
        GROUP BY e.id
        ORDER BY e.id DESC
    """)
    return jsonify({"success": True, "data": exams})


@app.route("/api/v1/metrics")
def api_get_metrics():
    """API endpoint to get summary metrics."""
    return jsonify({"success": True, "data": get_dashboard_metrics()})


# ============================================================================
# Application Entry Point
# ============================================================================

if __name__ == "__main__":
    init_db(force=False)
    print("ExamPro Server running at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
