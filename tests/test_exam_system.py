"""
Comprehensive Test Suite for ExamPro Online Examination System
Verifies:
- Segregated Admin and Student Portals with dedicated authentication
- Role-Based Access Control (Admin vs Student boundaries)
- Student directory & performance tracking (/admin/students)
- RESTful API endpoints (v1)
- Live assessment execution & automated scoring
- Academic Reports & CSV Export
Aligned with SPPU MCA Curriculum Chapter 4 (Testing).
"""

import unittest
import os
import json
from pathlib import Path

os.environ["FLASK_SECRET_KEY"] = "test-secret-key-12345"

from app import app
from database import query_db, modify_db, get_dashboard_metrics, get_student_roster
from seed_data import seed_database


class ExamProComprehensiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Seeds test database with default admin, students, questions, and records."""
        seed_database()

    def setUp(self):
        """Initializes Flask test client."""
        self.app = app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def admin_login(self, username="admin", password="admin123"):
        """Logs into Admin Portal."""
        return self.client.post("/admin/login", data={
            "username": username,
            "password": password,
        }, follow_redirects=True)

    def student_login(self, username="aarav", password="student123"):
        """Logs into Student Portal."""
        return self.client.post("/student/login", data={
            "username": username,
            "password": password,
        }, follow_redirects=True)

    def logout(self):
        """Helper to clear session."""
        with self.client.session_transaction() as sess:
            sess.clear()

    # ------------------------------------------------------------------------
    # 1. Entrance Hub & Health Checks
    # ------------------------------------------------------------------------
    def test_01_landing_hub(self):
        """UT-01: Landing page displays both Faculty and Student portal options."""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Faculty & Administration", res.data)
        self.assertIn(b"Student Examination Portal", res.data)

    def test_02_health_endpoints(self):
        """UT-02: Health endpoints return 200 with DB status healthy."""
        for endpoint in ("/health", "/api/v1/health"):
            res = self.client.get(endpoint)
            self.assertEqual(res.status_code, 200)
            data = json.loads(res.data)
            self.assertEqual(data["status"], "healthy")
            self.assertEqual(data["database"], "connected")

    # ------------------------------------------------------------------------
    # 2. Segregated Portals & Authentication
    # ------------------------------------------------------------------------
    def test_03_admin_portal_login(self):
        """UT-03: Faculty Admin login accesses dedicated admin dashboard."""
        res = self.admin_login("admin", "admin123")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Faculty Administration Console", res.data)
        self.assertIn(b"Overview Dashboard", res.data)
        self.logout()

    def test_04_student_portal_login(self):
        """UT-04: Student login accesses dedicated student candidate workspace."""
        res = self.student_login("aarav", "student123")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Candidate Dashboard", res.data)
        self.assertIn(b"MCA2026-001", res.data)
        self.logout()

    def test_05_cross_role_access_restriction(self):
        """UT-05: Student credentials cannot log in through Admin Portal."""
        res = self.client.post("/admin/login", data={
            "username": "aarav",
            "password": "student123",
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"reserved for Faculty/Admin", res.data)
        self.logout()

    def test_06_rbac_student_blocked_from_admin_students_page(self):
        """UT-06: Student session blocked from accessing /admin/students."""
        self.student_login("aarav", "student123")
        res = self.client.get("/admin/students", follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Faculty/Admin credentials", res.data)
        self.logout()

    def test_07_student_registration_workflow(self):
        """UT-07: New candidate registers through /student/register."""
        res = self.client.post("/student/register", data={
            "full_name": "Siddharth Verma",
            "roll_number": "MCA2026-088",
            "email": "sid.verma@acmi.edu.in",
            "username": "siddharth",
            "password": "password123",
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Siddharth Verma", res.data)
        self.logout()

    # ------------------------------------------------------------------------
    # 3. Admin Features (Question Bank, Exams, Student Roster)
    # ------------------------------------------------------------------------
    def test_08_admin_student_roster(self):
        """UT-08: Admin can view student roster with attempts and scores."""
        self.admin_login("admin", "admin123")
        res = self.client.get("/admin/students")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Enrolled Candidates Directory", res.data)
        self.assertIn(b"MCA2026-001", res.data)
        self.logout()

    def test_09_admin_question_and_exam_management(self):
        """UT-09: Admin can create questions and schedule examinations."""
        self.admin_login("admin", "admin123")
        res_q = self.client.post("/admin/questions", data={
            "subject_id": "1",
            "question_text": "Which module in Python is used for regular expressions?",
            "option_a": "regex",
            "option_b": "re",
            "option_c": "pyregex",
            "option_d": "match",
            "correct_option": "B",
            "marks": "2",
            "explanation": "The 're' standard library module handles regular expressions.",
        }, follow_redirects=True)
        self.assertEqual(res_q.status_code, 200)
        self.assertIn(b"Question successfully added", res_q.data)
        self.logout()

    # ------------------------------------------------------------------------
    # 4. Student Live Exam & Automated Evaluation
    # ------------------------------------------------------------------------
    def test_10_student_take_and_submit_exam(self):
        """UT-10: Student commences exam, submits responses, receives graded scorecard."""
        self.student_login("aarav", "student123")

        # Open exam runner
        res_runner = self.client.get("/student/take/1")
        self.assertEqual(res_runner.status_code, 200)
        self.assertIn(b"Time Remaining", res_runner.data)

        # Submit answers
        payload = {
            "exam_id": 1,
            "time_taken_seconds": 320,
            "answers": {
                "1": "C",
                "2": "B",
                "3": "A",
                "4": "D",
                "5": "B",
            }
        }
        res_sub = self.client.post("/student/submit",
                                   data=json.dumps(payload),
                                   content_type="application/json")
        self.assertEqual(res_sub.status_code, 200)
        sub_data = json.loads(res_sub.data)
        self.assertTrue(sub_data["success"])
        submission_id = sub_data["submission_id"]

        # View scorecard
        res_card = self.client.get(f"/student/result/{submission_id}")
        self.assertEqual(res_card.status_code, 200)
        self.assertIn(b"Assessment Passed", res_card.data)
        self.assertIn(b"100.0% Score", res_card.data)
        self.logout()

    # ------------------------------------------------------------------------
    # 5. Reports & CSV Export
    # ------------------------------------------------------------------------
    def test_11_reports_threshold_and_csv_export(self):
        """UT-11: Reports page and CSV export work properly."""
        self.admin_login("admin", "admin123")
        res = self.client.get("/admin/reports")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Academic Examination Submissions", res.data)

        csv_res = self.client.get("/admin/reports/export.csv")
        self.assertEqual(csv_res.status_code, 200)
        self.assertEqual(csv_res.mimetype, "text/csv")
        self.assertIn(b"Submission ID,Roll Number,Candidate Name", csv_res.data)
        self.logout()

    # ------------------------------------------------------------------------
    # 6. REST API Suite
    # ------------------------------------------------------------------------
    def test_12_rest_api_suite(self):
        """UT-12: REST API v1 endpoints return valid JSON structures."""
        res = self.client.get("/api/v1/subjects")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertGreaterEqual(len(data["data"]), 5)

        res_metrics = self.client.get("/api/v1/metrics")
        self.assertEqual(res_metrics.status_code, 200)
        m_data = json.loads(res_metrics.data)
        self.assertTrue(m_data["success"])
        self.assertIn("pass_rate", m_data["data"])

    # ------------------------------------------------------------------------
    # 7. Staff Lifecycle & Admin Verification Workflow
    # ------------------------------------------------------------------------
    def test_13_admin_create_staff_and_login(self):
        """UT-13: Admin directly enrolls faculty member and staff immediately logs in."""
        self.admin_login("admin", "admin123")
        res = self.client.post("/admin/staff/create", data={
            "full_name": "Prof. Anand Shinde",
            "department": "Department of MCA",
            "designation": "Assistant Professor",
            "email": "anand.shinde@acmi.edu.in",
            "contact_number": "+91 99887 76655",
            "username": "anand_shinde",
            "password": "staffPassword123",
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"enrolled successfully", res.data)
        self.logout()

        # Newly enrolled staff logs in immediately
        res_login = self.client.post("/staff/login", data={
            "username": "anand_shinde",
            "password": "staffPassword123",
        }, follow_redirects=True)
        self.assertEqual(res_login.status_code, 200)
        self.assertIn(b"Staff Overview Dashboard", res_login.data)
        self.logout()

    def test_14_admin_staff_directory_and_delete(self):
        """UT-14: Admin views authorized faculty directory and can revoke staff access."""
        self.admin_login("admin", "admin123")
        res_staff_page = self.client.get("/admin/staff")
        self.assertEqual(res_staff_page.status_code, 200)
        self.assertIn(b"Faculty &amp; Staff Directory", res_staff_page.data)

        # Find user ID for anand_shinde created in test_13
        user_row = query_db("SELECT id FROM users WHERE username = 'anand_shinde'", one=True)
        self.assertIsNotNone(user_row)
        user_id = user_row["id"]

        # Admin deletes/revokes staff
        res_del = self.client.post(f"/admin/staff/{user_id}/delete", follow_redirects=True)
        self.assertEqual(res_del.status_code, 200)
        self.assertIn(b"removed from portal", res_del.data)
        self.logout()

    # ------------------------------------------------------------------------
    # 8. Student Admin Controls (Edit, Reset Password, Delete)
    # ------------------------------------------------------------------------
    def test_15_admin_student_management_edit_reset_delete(self):
        """UT-15: Admin edits info, resets password, and deletes student."""
        self.admin_login("admin", "admin123")

        # 1. Edit info for student 'pooja' (user_id=3)
        res_edit = self.client.post("/admin/students/3/edit", data={
            "full_name": "Pooja D. Deshmukh",
            "roll_number": "MCA2026-002",
            "email": "pooja.updated@acmi.edu.in",
            "contact_number": "+91 91234 56789",
        }, follow_redirects=True)
        self.assertEqual(res_edit.status_code, 200)
        self.assertIn(b"Pooja D. Deshmukh", res_edit.data)

        # 2. Reset password
        res_reset = self.client.post("/admin/students/3/reset-password", data={
            "new_password": "newPoojaPassword123",
        }, follow_redirects=True)
        self.assertEqual(res_reset.status_code, 200)
        self.assertIn(b"successfully reset", res_reset.data)
        self.logout()

        # Student logs in with new password
        res_stu_login = self.client.post("/student/login", data={
            "username": "pooja",
            "password": "newPoojaPassword123",
        }, follow_redirects=True)
        self.assertEqual(res_stu_login.status_code, 200)
        self.assertIn(b"Candidate Dashboard", res_stu_login.data)
        self.logout()

        # 3. Admin deletes a student (e.g. ananya, user_id=7)
        self.admin_login("admin", "admin123")
        res_del = self.client.post("/admin/students/7/delete", follow_redirects=True)
        self.assertEqual(res_del.status_code, 200)
        self.assertIn(b"deleted", res_del.data)
        self.logout()

    # ------------------------------------------------------------------------
    # 9. Student Profile & Password Self-Service
    # ------------------------------------------------------------------------
    def test_16_student_profile_and_password_change(self):
        """UT-16: Student views profile, updates contact, and self-changes password."""
        self.student_login("aarav", "student123")

        res_prof = self.client.get("/student/profile")
        self.assertEqual(res_prof.status_code, 200)
        self.assertIn(b"Candidate Profile", res_prof.data)
        self.assertIn(b"MCA2026-001", res_prof.data)

        # Update contact
        res_upd = self.client.post("/student/profile/update", data={
            "email": "aarav.new@acmi.edu.in",
            "contact_number": "+91 99999 88888",
        }, follow_redirects=True)
        self.assertEqual(res_upd.status_code, 200)
        self.assertIn(b"Profile updated successfully", res_upd.data)

        # Change password
        res_pwd = self.client.post("/student/profile/change-password", data={
            "current_password": "student123",
            "new_password": "mySecureStudentPassword999",
            "confirm_password": "mySecureStudentPassword999",
        }, follow_redirects=True)
        self.assertEqual(res_pwd.status_code, 200)
        self.assertIn(b"Password updated successfully", res_pwd.data)
        self.logout()

        # Login with new password
        res_new_login = self.client.post("/student/login", data={
            "username": "aarav",
            "password": "mySecureStudentPassword999",
        }, follow_redirects=True)
        self.assertEqual(res_new_login.status_code, 200)
        self.assertIn(b"Candidate Dashboard", res_new_login.data)
        self.logout()

    # ------------------------------------------------------------------------
    # 10. Support Tickets & Admin Student Creation
    # ------------------------------------------------------------------------
    def test_17_support_tickets_lifecycle(self):
        """UT-17: Ticket creation, admin view, and status resolution workflow."""
        # 1. Student creates support ticket
        self.student_login("pooja", "student123")
        res_sub = self.client.post("/tickets/create", data={
            "name": "Pooja Deshmukh",
            "email": "pooja.d@acmi.edu.in",
            "subject": "Calculator access question in exam",
            "category": "Academic Support",
            "message": "Can we use an onscreen calculator for numerical questions in CS-102?",
            "priority": "Medium",
        }, follow_redirects=True)
        self.assertEqual(res_sub.status_code, 200)
        self.logout()

        # 2. Admin views tickets desk
        self.admin_login("admin", "admin123")
        res_desk = self.client.get("/admin/tickets")
        self.assertEqual(res_desk.status_code, 200)
        self.assertIn(b"Support &amp; Academic Tickets", res_desk.data)
        self.assertIn(b"Calculator access question in exam", res_desk.data)

        # 3. Admin updates status
        tickets = query_db("SELECT id FROM tickets WHERE subject = 'Calculator access question in exam'")
        self.assertTrue(len(tickets) > 0)
        t_id = tickets[0]["id"]
        res_stat = self.client.post(f"/admin/tickets/{t_id}/status", data={
            "status": "Resolved",
            "resolution_notes": "Clarified that an embedded virtual calculator is provided in Section B.",
        }, follow_redirects=True)
        self.assertEqual(res_stat.status_code, 200)
        self.assertIn(b"status updated", res_stat.data)
        self.logout()

    def test_18_admin_create_student(self):
        """UT-18: Admin enrolls new student and student immediately logs in."""
        self.admin_login("admin", "admin123")
        res_add = self.client.post("/admin/students/create", data={
            "full_name": "Siddharth S. Joshi",
            "roll_number": "MCA2026-099",
            "email": "siddharth.j@acmi.edu.in",
            "contact_number": "+91 98888 11111",
            "password": "siddharthPass123",
        }, follow_redirects=True)
        self.assertEqual(res_add.status_code, 200)
        self.assertIn(b"enrolled successfully", res_add.data)
        self.logout()

        # New student logs in
        res_log = self.client.post("/student/login", data={
            "username": "mca2026-099",
            "password": "siddharthPass123",
        }, follow_redirects=True)
        self.assertEqual(res_log.status_code, 200)
        self.assertIn(b"Candidate Dashboard", res_log.data)
        self.assertIn(b"Siddharth S. Joshi", res_log.data)
        self.logout()

    def test_19_browser_lock_tab_switches_telemetry(self):
        """UT-19: Browser lock telemetry tracks tab switch strikes and shows on results."""
        self.student_login("rohan", "student123")

        # Check runner has proctoring badge and modal
        res_runner = self.client.get("/student/take/1")
        self.assertEqual(res_runner.status_code, 200)
        self.assertIn(b"Browser Lock:", res_runner.data)
        self.assertIn(b"Proctored Examination Lock", res_runner.data)

        # Submit with 2 tab switch violations
        payload = {
            "exam_id": 1,
            "time_taken_seconds": 210,
            "tab_switches_count": 2,
            "answers": {
                "1": "C",
                "2": "B",
            }
        }
        res_sub = self.client.post("/student/submit",
                                   data=json.dumps(payload),
                                   content_type="application/json")
        self.assertEqual(res_sub.status_code, 200)
        sub_data = json.loads(res_sub.data)
        submission_id = sub_data["submission_id"]

        # Scorecard displays the 2 violations
        res_card = self.client.get(f"/student/result/{submission_id}")
        self.assertEqual(res_card.status_code, 200)
        self.assertIn(b"2 Tab Switch Violations Logged", res_card.data)

        # Download CSV scorecard contains proctoring telemetry
        res_csv = self.client.get(f"/result/{submission_id}/download")
        self.assertEqual(res_csv.status_code, 200)
        self.assertIn(b"2 Tab Switch Violations Recorded", res_csv.data)

        self.logout()


if __name__ == "__main__":
    unittest.main()
