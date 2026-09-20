"""
database.py
------------
Handles SQLite database operations and token authentication for AarogyaSaathi.
"""

import sqlite3
import os
import random
from flask import session

DB_NAME = os.path.join(os.path.dirname(__file__), "aarogyasaathi.db")


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def generate_unique_token(prefix="TK-"):
    return prefix + str(random.randint(10000, 99999))


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # ---------- USERS TABLE WITH TOKENS ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            auth_token TEXT UNIQUE,
            family_token TEXT UNIQUE,
            age INTEGER,
            gender TEXT,
            height_cm REAL,
            weight_kg REAL,
            diet TEXT,
            activity_level TEXT,
            health_conditions TEXT,
            goal TEXT,
            bmi REAL,
            family_code TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ---------- WATER TRACKING ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS water_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            entry_date TEXT,
            amount_ml INTEGER DEFAULT 0,
            goal_ml INTEGER DEFAULT 2500
        )
    """)

    # ---------- MEDICINE REMINDERS ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            medicine_name TEXT,
            dosage TEXT,
            time_of_day TEXT,
            notes TEXT,
            taken INTEGER DEFAULT 0,
            entry_date TEXT
        )
    """)

    # ---------- DAILY TASKS ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS daily_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            task_name TEXT,
            completed INTEGER DEFAULT 0,
            entry_date TEXT
        )
    """)

    # ---------- FAMILY MEMBERS TABLE ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS family_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_user_id INTEGER,
            name TEXT,
            relationship TEXT,
            phone TEXT,
            share_tasks INTEGER DEFAULT 1,
            share_water INTEGER DEFAULT 1,
            share_exercise INTEGER DEFAULT 1,
            share_meals INTEGER DEFAULT 1,
            share_medicine INTEGER DEFAULT 0,
            joined_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ---------- FAMILY ACTIVITY TIMELINE ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS family_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            family_member_id INTEGER,
            activity_text TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def get_user_by_token(token):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE auth_token = ?", (token,)).fetchone()
    conn.close()
    return user


def get_user_by_family_token(fam_token):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE family_token = ?", (fam_token,)).fetchone()
    conn.close()
    return user


def create_new_user(name=""):
    conn = get_connection()
    cur = conn.cursor()
    auth_token = generate_unique_token("TK-")
    family_token = generate_unique_token("FAM-")

    cur.execute("""
        INSERT INTO users (name, auth_token, family_token, family_code)
        VALUES (?, ?, ?, ?)
    """, (name, auth_token, family_token, generate_unique_token("AS-")))
    
    conn.commit()
    new_id = cur.lastrowid
    user = cur.execute("SELECT * FROM users WHERE id = ?", (new_id,)).fetchone()
    conn.close()
    return user


def get_or_create_demo_user():
    conn = get_connection()
    cur = conn.cursor()

    user_id = session.get("user_id")
    user = None

    if user_id:
        user = cur.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    if user is None:
        user = create_new_user()
        session["user_id"] = user["id"]

    conn.close()
    return user