# db.py — COMPLETE VERSION
import sqlite3
import hashlib
import os

DB_PATH = "fradb.sqlite"


# ─────────────────────── HELPERS ─────────────────────── #

def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


# ─────────────────────── INIT ────────────────────────── #

def init_db():
    conn = _conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id  INTEGER PRIMARY KEY,
            name        TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT UNIQUE NOT NULL,
            password    TEXT NOT NULL,
            role        TEXT NOT NULL DEFAULT 'user',
            student_id  INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id  INTEGER,
            name        TEXT,
            date        TEXT,
            time        TEXT,
            status      TEXT DEFAULT 'Present',
            photo_path  TEXT,
            FOREIGN KEY(student_id) REFERENCES students(student_id)
        )
    """)

    conn.commit()
    conn.close()
    ensure_admin()


# ─────────────────────── ADMIN ───────────────────────── #

def ensure_admin():
    """Creates a default admin account if none exists."""
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE role='admin' LIMIT 1")
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?,?,?)",
            ("admin", _hash("admin123"), "admin")
        )
        conn.commit()
        print("[DB] Default admin created → username: admin  password: admin123")
    conn.close()


# ─────────────────────── USERS ───────────────────────── #

def add_user(username: str, password: str, role: str = "user", student_id: int = None):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, password, role, student_id) VALUES (?,?,?,?)",
        (username, _hash(password), role, student_id)
    )
    conn.commit()
    conn.close()


def validate_user(username: str, password: str):
    """Returns user dict or None."""
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, _hash(password))
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_student_id(username: str):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT student_id FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    return row["student_id"] if row else None


def link_student_to_user(username: str, student_id: int):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET student_id=? WHERE username=?",
        (student_id, username)
    )
    conn.commit()
    conn.close()


# ─────────────────────── STUDENTS ────────────────────── #

def add_student(student_id: int, name: str):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO students (student_id, name) VALUES (?,?)",
        (student_id, name)
    )
    conn.commit()
    conn.close()


def get_student_name(student_id: int):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT name FROM students WHERE student_id=?", (student_id,))
    row = cur.fetchone()
    conn.close()
    return row["name"] if row else None


def get_all_students():
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT student_id, name FROM students ORDER BY student_id")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_student(student_id: int):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE student_id=?", (student_id,))
    cur.execute("DELETE FROM attendance WHERE student_id=?", (student_id,))
    conn.commit()
    conn.close()


# ─────────────────────── ATTENDANCE ──────────────────── #

def insert_attendance(student_id: int, name: str, date: str, time: str,
                      status: str = "Present", photo_path: str = None):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO attendance (student_id, name, date, time, status, photo_path)
        VALUES (?,?,?,?,?,?)
    """, (student_id, name, date, time, status, photo_path))
    conn.commit()
    conn.close()


# Alias used by migrate.py
log_attendance = insert_attendance


def already_marked_today(student_id: int, date: str) -> bool:
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM attendance WHERE student_id=? AND date=?",
        (student_id, date)
    )
    row = cur.fetchone()
    conn.close()
    return row is not None


def get_today_attendance(date: str):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT student_id, name, time, status, photo_path
        FROM attendance WHERE date=? ORDER BY time ASC
    """, (date,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_user_attendance(student_id: int):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT date, time, status
        FROM attendance WHERE student_id=?
        ORDER BY date DESC, time DESC
    """, (student_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_attendance():
    conn = _conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT student_id, name, date, time, status, photo_path
        FROM attendance ORDER BY date DESC, time DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_absentees(date: str):
    """Mark all registered students who have no entry today as Absent."""
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT student_id, name FROM students")
    all_students = cur.fetchall()
    cur.execute("SELECT DISTINCT student_id FROM attendance WHERE date=?", (date,))
    present_ids = {r["student_id"] for r in cur.fetchall()}
    for s in all_students:
        if s["student_id"] not in present_ids:
            cur.execute("""
                INSERT INTO attendance (student_id, name, date, time, status)
                VALUES (?,?,?,?,?)
            """, (s["student_id"], s["name"], date, "00:00:00", "Absent"))
    conn.commit()
    conn.close()


# Run on import
init_db()
