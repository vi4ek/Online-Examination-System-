"""
Seeds the database with users, roles (admin, staff, student), subjects,
questions, exams, candidates, and realistic submission records.
"""

from werkzeug.security import generate_password_hash
from database import init_db, db_session


def seed_database():
    init_db(force=True)

    with db_session() as conn:
        c = conn.cursor()

        # 1. Users (Admin Faculty, MCA Students, and Teaching Staff)
        # Passwords:
        # Admin: admin / admin123
        # Staff: prof_deshmukh (or staff) / staff123, prof_kulkarni / staff123 (pending)
        # Students: username / student123
        admin_hash = generate_password_hash("admin123")
        staff_hash = generate_password_hash("staff123")
        student_hash = generate_password_hash("student123")

        users = [
            ("admin", "admin@acmi.edu.in", admin_hash, "Prof. Jaydeep Shivaji Karpe", "admin", None, "+91 94220 11001", None, "Department of MCA", "Head of Department & Administrator", 1),
            ("aarav", "aarav.sharma@acmi.edu.in", student_hash, "Aarav Sharma", "student", "MCA2026-001", "+91 98231 44551", None, "Department of MCA", "Candidate", 1),
            ("pooja", "pooja.d@acmi.edu.in", student_hash, "Pooja Deshmukh", "student", "MCA2026-002", "+91 98231 44552", None, "Department of MCA", "Candidate", 1),
            ("rohan", "rohan.k@acmi.edu.in", student_hash, "Rohan Kulkarni", "student", "MCA2026-003", "+91 98231 44553", None, "Department of MCA", "Candidate", 1),
            ("sneha", "sneha.patil@acmi.edu.in", student_hash, "Sneha Patil", "student", "MCA2026-004", "+91 98231 44554", None, "Department of MCA", "Candidate", 1),
            ("vikram", "vikram.s@acmi.edu.in", student_hash, "Vikramaditya Shinde", "student", "MCA2026-005", "+91 98231 44555", None, "Department of MCA", "Candidate", 1),
            ("ananya", "ananya.j@acmi.edu.in", student_hash, "Ananya Joshi", "student", "MCA2026-006", "+91 98231 44556", None, "Department of MCA", "Candidate", 1),
            ("prof_deshmukh", "priya.deshmukh@acmi.edu.in", staff_hash, "Dr. Priya Deshmukh", "staff", None, "+91 98220 99881", None, "Department of MCA", "Associate Professor & Examiner", 1),
            ("prof_kulkarni", "nilesh.kulkarni@acmi.edu.in", staff_hash, "Prof. Nilesh Kulkarni", "staff", None, "+91 98220 99882", None, "Department of MCA", "Assistant Professor", 1),
        ]

        c.executemany("""
            INSERT INTO users (username, email, password_hash, full_name, role, roll_number, contact_number, profile_photo, department, designation, is_approved)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, users)

        # 2. Candidates (linked to student users)
        candidates = [
            (2, "MCA2026-001", "Aarav Sharma", "aarav.sharma@acmi.edu.in", "+91 98231 44551"),
            (3, "MCA2026-002", "Pooja Deshmukh", "pooja.d@acmi.edu.in", "+91 98231 44552"),
            (4, "MCA2026-003", "Rohan Kulkarni", "rohan.k@acmi.edu.in", "+91 98231 44553"),
            (5, "MCA2026-004", "Sneha Patil", "sneha.patil@acmi.edu.in", "+91 98231 44554"),
            (6, "MCA2026-005", "Vikramaditya Shinde", "vikram.s@acmi.edu.in", "+91 98231 44555"),
            (7, "MCA2026-006", "Ananya Joshi", "ananya.j@acmi.edu.in", "+91 98231 44556"),
        ]
        c.executemany("""
            INSERT INTO candidates (user_id, roll_number, full_name, email, contact_number)
            VALUES (?, ?, ?, ?, ?)
        """, candidates)

        # 3. Subjects
        subjects = [
            ("CS-101", "Python Programming & Data Structures", "Core programming concepts, built-in types, OOP, algorithmic paradigms"),
            ("CS-102", "Database Management Systems", "Relational design, normalization, ACID properties, SQL transactions"),
            ("CS-103", "Web Application Architectures", "HTTP lifecycle, client-server models, RESTful patterns, MVC"),
            ("CS-104", "Software Engineering & Quality Assurance", "SDLC models, agile testing methodologies, verification and validation"),
            ("CS-105", "Computer Networks & Cloud Infrastructure", "OSI reference stack, TCP/IP routing, cloud deployment paradigms"),
        ]
        c.executemany("INSERT INTO subjects (code, name, description) VALUES (?, ?, ?)", subjects)

        # 4. Questions (21 standard MCQs)
        questions = [
            # Subject 1 (Python) - Answers align with: 1:C, 2:B, 3:A, 4:D, 5:B
            (1, "What is the output of print(type([])) in Python?", "<class 'tuple'>", "<class 'array'>", "<class 'list'>", "<class 'set'>", "C", 2, "Lists in Python are denoted with square brackets and belong to type 'list'."),
            (1, "Which built-in Python module is used for regular expressions?", "regex", "re", "pyregex", "match", "B", 2, "The 're' standard library module handles regular expressions."),
            (1, "How do you instantiate a set with no elements in Python?", "set()", "{}", "[]", "tuple()", "A", 2, "{} denotes an empty dictionary, while set() creates an empty set."),
            (1, "Which keyword is used to define an anonymous inline function in Python?", "def", "func", "inline", "lambda", "D", 2, "Lambda functions are anonymous single-expression functions."),
            (1, "What will '2' + '3' evaluate to in Python?", "5", "'23'", "Error", "None", "B", 2, "String concatenation of two characters produces '23'."),

            # Subject 2 (DBMS)
            (2, "Which normal form deals with removing transitive functional dependency?", "1NF", "2NF", "3NF", "BCNF", "C", 2, "3NF requires relation to be in 2NF and eliminate transitive dependencies on candidate keys."),
            (2, "What does ACID stand for in database transaction management?", "Atomicity, Consistency, Isolation, Durability", "Action, Commit, Integrity, Data", "Access, Control, Isolation, Distribution", "Array, Column, Index, Domain", "A", 2, "ACID guarantees transactional reliability in relational database engines."),
            (2, "Which SQL command is classified under Data Definition Language (DDL)?", "SELECT", "INSERT", "ALTER", "UPDATE", "C", 2, "ALTER modifies database schema objects directly."),
            (2, "Which index type is best suited for exact key matches in relational databases?", "B-Tree Index", "Hash Index", "Bitmap Index", "Spatial Index", "B", 2, "Hash indexing provides O(1) direct equality lookups."),
            (2, "In a SQL query, which clause is evaluated after GROUP BY?", "WHERE", "HAVING", "FROM", "JOIN", "B", 2, "HAVING filters groups created by the GROUP BY clause."),

            # Subject 3 (Web Tech)
            (3, "Which HTTP status code represents 'Resource Created'?", "200", "201", "204", "301", "B", 2, "HTTP 201 indicates a new resource was successfully created on the server."),
            (3, "What header prevents MIME-type sniffing in browsers?", "X-Frame-Options", "X-Content-Type-Options", "Content-Security-Policy", "Strict-Transport-Security", "B", 2, "nosniff directive prevents content-type sniffing."),
            (3, "In RESTful architecture, which method should be idempotent?", "POST", "PUT", "PATCH", "CONNECT", "B", 2, "PUT is idempotent as identical subsequent requests produce the same state."),
            (3, "Which web security mechanism prevents unauthorized cross-origin requests?", "CORS", "CSRF", "XSS", "SQLi", "A", 2, "Cross-Origin Resource Sharing defines trusted origin boundaries."),
            (3, "What does CSS property 'box-sizing: border-box' calculate?", "Margin + Border", "Padding + Border in width", "Content only", "Margin only", "B", 2, "border-box includes padding and border within specified dimensions."),

            # Subject 4 (Software Engineering)
            (4, "Which SDLC model incorporates continuous customer feedback loops?", "Waterfall", "V-Model", "Agile Scrum", "Big Bang", "C", 2, "Agile uses iterative sprints to adapt to customer feedback."),
            (4, "What testing level validates individual software components?", "Unit Testing", "System Testing", "Acceptance Testing", "Integration Testing", "A", 2, "Unit testing isolates and tests single functions or units."),
            (4, "What is cyclomatic complexity primarily used to assess?", "Database speed", "Independent code paths", "Network latency", "UI responsive layouts", "B", 2, "Cyclomatic complexity measures linear independent paths through source code."),
            (4, "In Scrum, who is responsible for maximizing the product value?", "Scrum Master", "Product Owner", "Lead Developer", "QA Tester", "B", 2, "The Product Owner prioritizes backlog items to maximize value."),
            (4, "What type of testing examines code execution without viewing internal logic?", "White-Box Testing", "Black-Box Testing", "Glass-Box Testing", "Static Analysis", "B", 2, "Black-box testing focuses strictly on specifications and I/O."),

            # Additional question for Subject 1
            (1, "Which method adds an element to the end of a Python list?", "add()", "push()", "append()", "insert()", "C", 2, "list.append(x) inserts element x at the end of the list.")
        ]
        c.executemany("""
            INSERT INTO questions (subject_id, question_text, option_a, option_b, option_c, option_d, correct_option, marks, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, questions)

        # 5. Exams (4 scheduled assessments)
        exams = [
            ("MCA-101: Core Python Programming Final Assessment", 1, 30, 10, 5, "Answer all 5 questions. No negative marking.", "Published", 1),
            ("MCA-102: Relational Databases Mid-Term Examination", 2, 45, 10, 5, "Covers Relational Algebra, Normalization, and ACID transactions.", "Published", 1),
            ("MCA-103: Advanced Web Architectures Evaluation", 3, 40, 10, 5, "RESTful endpoints, HTTP headers, CORS compliance.", "Published", 8),
            ("MCA-104: Software Quality Assurance Term Paper", 4, 35, 10, 5, "White-box, Black-box, Cyclomatic Complexity.", "Draft", 8),
        ]
        c.executemany("""
            INSERT INTO exams (title, subject_id, duration_minutes, total_marks, pass_marks, instructions, status, created_by_user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, exams)

        # 6. Exam-Question Mappings
        for q_id in range(1, 6):
            c.execute("INSERT INTO exam_questions (exam_id, question_id) VALUES (1, ?)", (q_id,))
        for q_id in range(6, 11):
            c.execute("INSERT INTO exam_questions (exam_id, question_id) VALUES (2, ?)", (q_id,))
        for q_id in range(11, 16):
            c.execute("INSERT INTO exam_questions (exam_id, question_id) VALUES (3, ?)", (q_id,))
        for q_id in range(16, 21):
            c.execute("INSERT INTO exam_questions (exam_id, question_id) VALUES (4, ?)", (q_id,))

        # 7. Submissions & Answers (6 valid records with user_id)
        c.execute("""
            INSERT INTO submissions (exam_id, candidate_id, user_id, score, total_marks, percentage, status, started_at, submitted_at, time_taken_seconds)
            VALUES (1, 1, 2, 10, 10, 100.0, 'Passed', '2026-11-20 10:00:00', '2026-11-20 10:14:32', 872)
        """)
        sub1_id = c.lastrowid
        ans_sub1 = [(sub1_id, 1, 'C', 1, 2), (sub1_id, 2, 'B', 1, 2), (sub1_id, 3, 'A', 1, 2), (sub1_id, 4, 'D', 1, 2), (sub1_id, 5, 'B', 1, 2)]
        c.executemany("INSERT INTO submission_answers (submission_id, question_id, selected_option, is_correct, marks_awarded) VALUES (?, ?, ?, ?, ?)", ans_sub1)

        c.execute("""
            INSERT INTO submissions (exam_id, candidate_id, user_id, score, total_marks, percentage, status, started_at, submitted_at, time_taken_seconds)
            VALUES (1, 2, 3, 8, 10, 80.0, 'Passed', '2026-11-20 10:05:00', '2026-11-20 10:22:15', 1035)
        """)
        sub2_id = c.lastrowid
        ans_sub2 = [(sub2_id, 1, 'C', 1, 2), (sub2_id, 2, 'B', 1, 2), (sub2_id, 3, 'B', 0, 0), (sub2_id, 4, 'D', 1, 2), (sub2_id, 5, 'B', 1, 2)]
        c.executemany("INSERT INTO submission_answers (submission_id, question_id, selected_option, is_correct, marks_awarded) VALUES (?, ?, ?, ?, ?)", ans_sub2)

        c.execute("""
            INSERT INTO submissions (exam_id, candidate_id, user_id, score, total_marks, percentage, status, started_at, submitted_at, time_taken_seconds)
            VALUES (1, 3, 4, 4, 10, 40.0, 'Failed', '2026-11-20 11:00:00', '2026-11-20 11:28:40', 1720)
        """)
        sub3_id = c.lastrowid
        ans_sub3 = [(sub3_id, 1, 'A', 0, 0), (sub3_id, 2, 'B', 1, 2), (sub3_id, 3, 'C', 0, 0), (sub3_id, 4, 'D', 1, 2), (sub3_id, 5, 'A', 0, 0)]
        c.executemany("INSERT INTO submission_answers (submission_id, question_id, selected_option, is_correct, marks_awarded) VALUES (?, ?, ?, ?, ?)", ans_sub3)

        c.execute("""
            INSERT INTO submissions (exam_id, candidate_id, user_id, score, total_marks, percentage, status, started_at, submitted_at, time_taken_seconds)
            VALUES (2, 4, 5, 10, 10, 100.0, 'Passed', '2026-11-20 14:00:00', '2026-11-20 14:18:10', 1090)
        """)
        sub4_id = c.lastrowid
        ans_sub4 = [(sub4_id, 6, 'B', 1, 2), (sub4_id, 7, 'C', 1, 2), (sub4_id, 8, 'C', 1, 2), (sub4_id, 9, 'D', 1, 2), (sub4_id, 10, 'B', 1, 2)]
        c.executemany("INSERT INTO submission_answers (submission_id, question_id, selected_option, is_correct, marks_awarded) VALUES (?, ?, ?, ?, ?)", ans_sub4)

        c.execute("""
            INSERT INTO submissions (exam_id, candidate_id, user_id, score, total_marks, percentage, status, started_at, submitted_at, time_taken_seconds)
            VALUES (2, 5, 6, 8, 10, 80.0, 'Passed', '2026-11-20 14:30:00', '2026-11-20 14:49:50', 1190)
        """)
        sub5_id = c.lastrowid
        ans_sub5 = [(sub5_id, 6, 'B', 1, 2), (sub5_id, 7, 'A', 0, 0), (sub5_id, 8, 'C', 1, 2), (sub5_id, 9, 'D', 1, 2), (sub5_id, 10, 'B', 1, 2)]
        c.executemany("INSERT INTO submission_answers (submission_id, question_id, selected_option, is_correct, marks_awarded) VALUES (?, ?, ?, ?, ?)", ans_sub5)

        c.execute("""
            INSERT INTO submissions (exam_id, candidate_id, user_id, score, total_marks, percentage, status, started_at, submitted_at, time_taken_seconds)
            VALUES (3, 6, 7, 10, 10, 100.0, 'Passed', '2026-11-21 09:15:00', '2026-11-21 09:29:45', 885)
        """)
        sub6_id = c.lastrowid
        ans_sub6 = [(sub6_id, 11, 'B', 1, 2), (sub6_id, 12, 'B', 1, 2), (sub6_id, 13, 'B', 1, 2), (sub6_id, 14, 'B', 1, 2), (sub6_id, 15, 'B', 1, 2)]
        c.executemany("INSERT INTO submission_answers (submission_id, question_id, selected_option, is_correct, marks_awarded) VALUES (?, ?, ?, ?, ?)", ans_sub6)

        # 8. Support & Academic Query Tickets
        tickets = [
            (2, "Aarav Sharma", "aarav.sharma@acmi.edu.in", "student", "Lab terminal network lag during Web Architectures test", "Technical Issue", "Sir, terminal #4 experienced 40 seconds websocket latency while saving answers. Requesting confirmation that all 5 responses were recorded.", "Open", "High", None),
            (3, "Pooja Deshmukh", "pooja.d@acmi.edu.in", "student", "Clarification on Question #3 regarding list mutability", "Academic Support", "In Python Programming exam, Question 3 had two closely aligned answer descriptions. Could faculty review question explanation?", "In Progress", "Medium", "Assigned to Dr. Priya Deshmukh for review."),
            (4, "Rohan Kulkarni", "rohan.k@acmi.edu.in", "student", "Profile contact number verification request", "Account Security", "Updated my contact number to +91 98231 44553 for SMS test alerts.", "Resolved", "Low", "Profile record verified and updated by administrator."),
            (8, "Dr. Priya Deshmukh", "priya.deshmukh@acmi.edu.in", "staff", "Approval for 15 new PostgreSQL normalization MCQs", "Academic Support", "Requesting HOD approval for expanding the DBMS question bank ahead of Semester 2 term-end tests.", "Open", "Medium", None),
        ]
        c.executemany("""
            INSERT INTO tickets (user_id, name, email, user_role, subject, category, message, status, priority, resolution_notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, tickets)

    print("Database seeded with users (admin, staff & students), subjects, questions, exams, 6 submissions, and support tickets.")


if __name__ == "__main__":
    seed_database()
