"""
Database connection, management, and schema helpers.
Features per-request connection caching via Flask 'g' object, WAL mode,
transactional safety, schema migration, and query helper utilities.
"""

import sqlite3
from pathlib import Path
from contextlib import contextmanager
from flask import g

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "exam_system.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def ensure_schema_upgrades(conn):
    """Safely adds newly required columns to existing SQLite database tables if missing."""
    try:
        cur = conn.cursor()
        # Check users table columns
        user_cols = [c[1] for c in cur.execute("PRAGMA table_info(users)").fetchall()]
        if user_cols:
            if "contact_number" not in user_cols:
                cur.execute("ALTER TABLE users ADD COLUMN contact_number TEXT;")
            if "profile_photo" not in user_cols:
                cur.execute("ALTER TABLE users ADD COLUMN profile_photo TEXT;")
            if "department" not in user_cols:
                cur.execute("ALTER TABLE users ADD COLUMN department TEXT;")
            if "designation" not in user_cols:
                cur.execute("ALTER TABLE users ADD COLUMN designation TEXT;")
            if "is_approved" not in user_cols:
                cur.execute("ALTER TABLE users ADD COLUMN is_approved INTEGER NOT NULL DEFAULT 1;")

        # Check candidates table columns
        cand_cols = [c[1] for c in cur.execute("PRAGMA table_info(candidates)").fetchall()]
        if cand_cols:
            if "contact_number" not in cand_cols:
                cur.execute("ALTER TABLE candidates ADD COLUMN contact_number TEXT;")
            if "profile_photo" not in cand_cols:
                cur.execute("ALTER TABLE candidates ADD COLUMN profile_photo TEXT;")

        # Check submissions table columns
        sub_cols = [c[1] for c in cur.execute("PRAGMA table_info(submissions)").fetchall()]
        if sub_cols:
            if "tab_switches_count" not in sub_cols:
                cur.execute("ALTER TABLE submissions ADD COLUMN tab_switches_count INTEGER DEFAULT 0;")

        # Ensure tickets table exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                user_role TEXT NOT NULL DEFAULT 'student' CHECK(user_role IN ('student', 'staff', 'admin')),
                subject TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'Academic Support',
                message TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Open' CHECK(status IN ('Open', 'In Progress', 'Resolved', 'Closed')),
                priority TEXT NOT NULL DEFAULT 'Medium' CHECK(priority IN ('Low', 'Medium', 'High', 'Urgent')),
                resolution_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            );
        """)
        conn.commit()
    except Exception as e:
        # Avoid crashing if schema is being initialized from scratch
        pass


def make_connection():
    """Creates a raw sqlite3 connection configured with Foreign Keys and WAL mode."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    ensure_schema_upgrades(conn)
    return conn


def get_db():
    """
    Returns the database connection for the current Flask application context.
    Caches connection in flask.g to prevent multiple open connections per request.
    """
    if "db" not in g:
        g.db = make_connection()
    return g.db


def close_db(e=None):
    """Closes the current request's database connection if opened."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


@contextmanager
def db_session():
    """Context manager for standalone/background tasks outside request context."""
    conn = make_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def query_db(query, args=(), one=False):
    """Executes a SELECT query and returns list of dicts (or single dict if one=True)."""
    try:
        db = get_db()
    except RuntimeError:
        with db_session() as conn:
            cur = conn.execute(query, args)
            rv = cur.fetchall()
            cur.close()
            return (dict(rv[0]) if rv else None) if one else [dict(r) for r in rv]

    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (dict(rv[0]) if rv else None) if one else [dict(r) for r in rv]


def modify_db(query, args=()):
    """Executes an INSERT, UPDATE, or DELETE query and commits changes."""
    try:
        db = get_db()
        cur = db.execute(query, args)
        db.commit()
        last_id = cur.lastrowid
        row_count = cur.rowcount
        cur.close()
        return last_id, row_count
    except RuntimeError:
        with db_session() as conn:
            cur = conn.execute(query, args)
            conn.commit()
            last_id = cur.lastrowid
            row_count = cur.rowcount
            cur.close()
            return last_id, row_count


def init_db(force=False):
    """Initializes tables from schema.sql. If force=True, drops existing tables first."""
    with db_session() as conn:
        cursor = conn.cursor()
        if force:
            cursor.execute("PRAGMA foreign_keys = OFF;")
            tables = [
                "submission_answers",
                "submissions",
                "exam_questions",
                "questions",
                "exams",
                "candidates",
                "subjects",
                "users",
            ]
            for t in tables:
                cursor.execute(f"DROP TABLE IF EXISTS {t};")
            cursor.execute("PRAGMA foreign_keys = ON;")

        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())
        conn.commit()


def get_dashboard_metrics():
    """Aggregates all administrative telemetry and performance KPI figures."""
    with db_session() as conn:
        c = conn.cursor()
        total_exams = c.execute("SELECT COUNT(*) FROM exams").fetchone()[0]
        published_exams = c.execute("SELECT COUNT(*) FROM exams WHERE status = 'Published'").fetchone()[0]
        total_questions = c.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
        total_candidates = c.execute("SELECT COUNT(*) FROM candidates").fetchone()[0]
        total_submissions = c.execute("SELECT COUNT(*) FROM submissions").fetchone()[0]
        total_staff = c.execute("SELECT COUNT(*) FROM users WHERE role = 'staff'").fetchone()[0]
        pending_staff = c.execute("SELECT COUNT(*) FROM users WHERE role = 'staff' AND is_approved = 0").fetchone()[0]
        
        # Tickets telemetry
        try:
            total_tickets = c.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
            open_tickets = c.execute("SELECT COUNT(*) FROM tickets WHERE status = 'Open'").fetchone()[0]
            in_progress_tickets = c.execute("SELECT COUNT(*) FROM tickets WHERE status = 'In Progress'").fetchone()[0]
            resolved_tickets = c.execute("SELECT COUNT(*) FROM tickets WHERE status = 'Resolved'").fetchone()[0]
            recent_tickets = c.execute("""
                SELECT id, user_id, name, email, user_role, subject, category, message, status, priority, resolution_notes, created_at
                FROM tickets
                ORDER BY id DESC
                LIMIT 8
            """).fetchall()
        except Exception:
            total_tickets = 0
            open_tickets = 0
            in_progress_tickets = 0
            resolved_tickets = 0
            recent_tickets = []

        # Pending staff list for quick review
        pending_staff_users = c.execute("""
            SELECT id, username, full_name, email, contact_number, department, designation, created_at
            FROM users
            WHERE role = 'staff' AND is_approved = 0
            ORDER BY created_at DESC
        """).fetchall()

        # Approved staff list
        approved_staff_users = c.execute("""
            SELECT id, username, full_name, email, contact_number, department, designation, created_at
            FROM users
            WHERE role = 'staff' AND is_approved = 1
            ORDER BY full_name ASC
        """).fetchall()

        # Student roster summary
        students_list = c.execute("""
            SELECT u.id, u.username, u.roll_number, u.full_name, u.email, u.contact_number, u.created_at,
                   COUNT(s.id) as attempts_count,
                   SUM(CASE WHEN s.status = 'Passed' THEN 1 ELSE 0 END) as passed_count,
                   ROUND(AVG(s.percentage), 1) as avg_score
            FROM users u
            LEFT JOIN submissions s ON u.id = s.user_id
            WHERE u.role = 'student'
            GROUP BY u.id
            ORDER BY u.roll_number ASC
        """).fetchall()

        pass_row = c.execute("""
            SELECT
                SUM(CASE WHEN status = 'Passed' THEN 1 ELSE 0 END) as passed_count,
                COUNT(*) as total
            FROM submissions
        """).fetchone()

        passed_count = pass_row["passed_count"] or 0
        sub_total = pass_row["total"] or 0
        pass_rate = round((passed_count / sub_total * 100), 1) if sub_total > 0 else 0.0

        avg_score_row = c.execute("SELECT AVG(percentage) as avg_pct FROM submissions").fetchone()
        avg_score = round(avg_score_row["avg_pct"], 1) if avg_score_row["avg_pct"] else 0.0

        recent_submissions = c.execute("""
            SELECT s.id, s.score, s.total_marks, s.percentage, s.status, s.submitted_at,
                   c.full_name as candidate_name, c.roll_number,
                   e.title as exam_title
            FROM submissions s
            JOIN candidates c ON s.candidate_id = c.id
            JOIN exams e ON s.exam_id = e.id
            ORDER BY s.submitted_at DESC
            LIMIT 6
        """).fetchall()

        recent_exams = c.execute("""
            SELECT e.id, e.title, sub.name as subject_name, sub.code as subject_code, e.duration_minutes,
                   e.total_marks, e.pass_marks, e.status, COUNT(eq.id) as question_count
            FROM exams e
            JOIN subjects sub ON e.subject_id = sub.id
            LEFT JOIN exam_questions eq ON e.id = eq.exam_id
            GROUP BY e.id
            ORDER BY e.created_at DESC
            LIMIT 5
        """).fetchall()

        subject_stats = c.execute("""
            SELECT s.id, s.name, s.code,
                   (SELECT COUNT(*) FROM questions q WHERE q.subject_id = s.id) as question_count,
                   (SELECT COUNT(*) FROM exams e WHERE e.subject_id = s.id AND e.status = 'Published') as active_exams
            FROM subjects s
            ORDER BY s.code ASC
        """).fetchall()

        return {
            "total_exams": total_exams,
            "published_exams": published_exams,
            "total_questions": total_questions,
            "total_candidates": total_candidates,
            "total_submissions": total_submissions,
            "total_staff": total_staff,
            "pending_staff": pending_staff,
            "pending_staff_count": pending_staff,
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "in_progress_tickets": in_progress_tickets,
            "resolved_tickets": resolved_tickets,
            "recent_tickets": [dict(r) for r in recent_tickets],
            "pending_staff_users": [dict(r) for r in pending_staff_users],
            "approved_staff_users": [dict(r) for r in approved_staff_users],
            "students_list": [dict(r) for r in students_list],
            "pass_rate": pass_rate,
            "avg_score": avg_score,
            "recent_submissions": [dict(r) for r in recent_submissions],
            "recent_exams": [dict(r) for r in recent_exams],
            "subject_stats": [dict(r) for r in subject_stats],
        }


def get_student_roster():
    """Retrieves full student directory with cumulative performance stats and profile info for Admin."""
    return query_db("""
        SELECT u.id, u.username, u.roll_number, u.full_name, u.email, u.contact_number, u.profile_photo, u.created_at,
               COUNT(s.id) as attempts_count,
               SUM(CASE WHEN s.status = 'Passed' THEN 1 ELSE 0 END) as passed_count,
               ROUND(AVG(s.percentage), 1) as avg_score
        FROM users u
        LEFT JOIN submissions s ON u.id = s.user_id
        WHERE u.role = 'student'
        GROUP BY u.id
        ORDER BY u.roll_number ASC
    """)


def get_staff_roster():
    """Retrieves full faculty and staff roster with approval status for Admin."""
    return query_db("""
        SELECT u.id, u.username, u.full_name, u.email, u.contact_number, u.department,
               u.designation, u.is_approved, u.created_at,
               (SELECT COUNT(*) FROM exams e WHERE e.created_by_user_id = u.id) as exams_created
        FROM users u
        WHERE u.role = 'staff'
        ORDER BY u.is_approved ASC, u.created_at DESC
    """)


def get_pending_staff_count():
    """Returns number of staff accounts pending administrative approval."""
    res = query_db("SELECT COUNT(*) as cnt FROM users WHERE role = 'staff' AND is_approved = 0", one=True)
    return res["cnt"] if res else 0


def get_staff_metrics(user_id):
    """Telemetry and stats for a dedicated staff member."""
    with db_session() as conn:
        c = conn.cursor()
        my_exams = c.execute("SELECT COUNT(*) FROM exams WHERE created_by_user_id = ?", (user_id,)).fetchone()[0]
        total_questions = c.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
        total_published = c.execute("SELECT COUNT(*) FROM exams WHERE status = 'Published'").fetchone()[0]
        total_evaluations = c.execute("SELECT COUNT(*) FROM submissions").fetchone()[0]
        return {
            "my_exams": my_exams,
            "total_questions": total_questions,
            "total_published": total_published,
            "total_evaluations": total_evaluations,
        }


def get_tickets(status_filter=None):
    """Retrieves support and academic query tickets with optional status filtering."""
    if status_filter and status_filter.lower() != "all":
        return query_db(
            "SELECT * FROM tickets WHERE status = ? ORDER BY id DESC",
            (status_filter,)
        )
    return query_db("SELECT * FROM tickets ORDER BY id DESC")


def get_ticket_by_id(ticket_id):
    """Fetches a single support ticket by its primary key ID."""
    return query_db("SELECT * FROM tickets WHERE id = ?", (ticket_id,), one=True)


def create_ticket(user_id, name, email, user_role, subject, category, message, priority="Medium"):
    """Creates a new academic or technical support ticket."""
    return modify_db("""
        INSERT INTO tickets (user_id, name, email, user_role, subject, category, message, status, priority)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Open', ?)
    """, (user_id, name, email, user_role, subject, category, message, priority))


def update_ticket_status(ticket_id, status, resolution_notes=None):
    """Updates ticket status and optional resolution remarks."""
    return modify_db("""
        UPDATE tickets
        SET status = ?, resolution_notes = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (status, resolution_notes, ticket_id))


def delete_ticket(ticket_id):
    """Deletes a ticket by ID."""
    return modify_db("DELETE FROM tickets WHERE id = ?", (ticket_id,))

