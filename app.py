"""
app.py
------
Flask Application with Personal Token Login & Family Token Monitoring.
"""

import os
import random
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash

import database
from services.health_service import calculate_bmi, bmi_category
from services.meal_service import generate_meal_plan
from services.exercise_service import get_exercise_plan, get_yoga_poses, get_yoga_timing_guide
from services.meal_analyzer import analyze_meal_photo
from translations import get_text

# =========================================================
# APP CONFIGURATION
# =========================================================
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

TODAY = lambda: date.today().isoformat()


# =========================================================
# HELPER FUNCTIONS & TRANSLATION
# =========================================================
@app.context_processor
def inject_translator():
    lang = session.get("lang", "en")

    def t(key):
        return get_text(key, lang)

    return dict(t=t, current_lang=lang)


@app.route("/set-language/<lang_code>")
def set_language(lang_code):
    if lang_code in ("en", "hi"):
        session["lang"] = lang_code
    return redirect(request.referrer or url_for("index"))


# =========================================================
# WELCOME & AUTHENTICATION (TOKENS)
# =========================================================
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    """Create a new account and assign unique Personal & Family Tokens."""
    name = request.form.get("name", "").strip()
    session.clear()
    user = database.create_new_user(name)
    session["user_id"] = user["id"]
    return redirect(url_for("profile"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login using Personal Auth Token."""
    if request.method == "POST":
        token = request.form.get("token", "").strip()
        user = database.get_user_by_token(token)
        if user:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid Personal Token! Please check and try again.")
    return render_template("login.html")


@app.route("/family/mentor", methods=["POST"])
def mentor_login():
    """Monitor a family member's dashboard using their Family Token."""
    fam_token = request.form.get("family_token", "").strip()
    user = database.get_user_by_family_token(fam_token)
    if user:
        session["mentor_user_id"] = user["id"]
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("family", error="Invalid Family Token!"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# =========================================================
# PROFILE SETUP
# =========================================================
@app.route("/profile", methods=["GET", "POST"])
def profile():
    user = database.get_or_create_demo_user()
    current_user_id = user["id"]

    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age", type=int)
        gender = request.form.get("gender")
        height_cm = request.form.get("height_cm", type=float)
        weight_kg = request.form.get("weight_kg", type=float)
        diet = request.form.get("diet")
        activity_level = request.form.get("activity_level")
        goal = request.form.get("goal")

        conditions = request.form.getlist("health_conditions")
        other_condition = request.form.get("other_condition")
        if other_condition:
            conditions.append(other_condition)
        conditions_text = ",".join(conditions)

        bmi = calculate_bmi(weight_kg, height_cm)

        conn = database.get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE users SET
                name = ?, age = ?, gender = ?, height_cm = ?, weight_kg = ?,
                diet = ?, activity_level = ?, health_conditions = ?, goal = ?,
                bmi = ?
            WHERE id = ?
        """, (name, age, gender, height_cm, weight_kg, diet, activity_level,
              conditions_text, goal, bmi, current_user_id))
        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("profile.html", user=user)


# =========================================================
# DASHBOARD
# =========================================================
@app.route("/dashboard")
def dashboard():
    target_user_id = session.get("mentor_user_id") or session.get("user_id")
    
    if not target_user_id:
        user = database.get_or_create_demo_user()
        target_user_id = user["id"]
    else:
        conn = database.get_connection()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (target_user_id,)).fetchone()
        conn.close()

    conn = database.get_connection()
    cur = conn.cursor()

    water_row = cur.execute(
        "SELECT * FROM water_tracking WHERE user_id = ? AND entry_date = ?", (target_user_id, TODAY())
    ).fetchone()
    water_amount = water_row["amount_ml"] if water_row else 0
    water_goal = water_row["goal_ml"] if water_row else 2500

    tasks = cur.execute(
        "SELECT * FROM daily_tasks WHERE user_id = ? AND entry_date = ?", (target_user_id, TODAY())
    ).fetchall()
    if not tasks:
        default_tasks = ["Breakfast", "Drink 500 ml water", "20 min walk / yoga",
                          "Lunch", "Take scheduled medicine", "Dinner"]
        for task_name in default_tasks:
            cur.execute(
                "INSERT INTO daily_tasks (user_id, task_name, completed, entry_date) VALUES (?, ?, 0, ?)",
                (target_user_id, task_name, TODAY())
            )
        conn.commit()
        tasks = cur.execute(
            "SELECT * FROM daily_tasks WHERE user_id = ? AND entry_date = ?", (target_user_id, TODAY())
        ).fetchall()

    tasks_done = sum(1 for t in tasks if t["completed"])
    tasks_total = len(tasks)
    pending_tasks = [t["task_name"] for t in tasks if not t["completed"]]

    medicines = cur.execute(
        "SELECT * FROM medicines WHERE user_id = ? AND entry_date = ?", (target_user_id, TODAY())
    ).fetchall()
    meds_taken = sum(1 for m in medicines if m["taken"])

    family_members = cur.execute(
        "SELECT * FROM family_members WHERE owner_user_id = ?", (target_user_id,)
    ).fetchall()

    conn.close()

    overall_progress = round((tasks_done / tasks_total) * 100) if tasks_total > 0 else 0

    return render_template(
        "dashboard.html",
        user=user,
        water_amount=water_amount,
        water_goal=water_goal,
        tasks=tasks,
        tasks_done=tasks_done,
        tasks_total=tasks_total,
        pending_tasks=pending_tasks,
        medicines=medicines,
        meds_taken=meds_taken,
        family_members=family_members,
        overall_progress=overall_progress,
        is_mentor="mentor_user_id" in session
    )


# =========================================================
# MEAL, EXERCISE & WATER MODULES
# =========================================================
@app.route("/meal")
def meal():
    user = database.get_or_create_demo_user()
    diet = user["diet"] if user and user["diet"] else "veg"
    goal = user["goal"] if user and user["goal"] else "general wellness"
    plan = generate_meal_plan(diet, goal)
    return render_template("meal.html", plan=plan, user=user)


@app.route("/meal/analyze", methods=["GET", "POST"])
def meal_analyze():
    result = None
    if request.method == "POST":
        uploaded_file = request.files.get("meal_photo")
        result = analyze_meal_photo(uploaded_file)
    return render_template("meal_analyze.html", result=result)


@app.route("/exercise")
def exercise():
    return render_template("exercise.html", exercises=get_exercise_plan(), yoga_poses=get_yoga_poses(), timing_guide=get_yoga_timing_guide())


@app.route("/water")
def water():
    user = database.get_or_create_demo_user()
    conn = database.get_connection()
    row = conn.execute("SELECT * FROM water_tracking WHERE user_id = ? AND entry_date = ?", (user["id"], TODAY())).fetchone()
    conn.close()
    return render_template("water.html", amount=row["amount_ml"] if row else 0, goal=row["goal_ml"] if row else 2500)


@app.route("/water/add", methods=["POST"])
def water_add():
    user = database.get_or_create_demo_user()
    ml_to_add = request.json.get("amount", 0)
    conn = database.get_connection()
    cur = conn.cursor()
    row = cur.execute("SELECT * FROM water_tracking WHERE user_id = ? AND entry_date = ?", (user["id"], TODAY())).fetchone()
    if row:
        new_amount = row["amount_ml"] + ml_to_add
        cur.execute("UPDATE water_tracking SET amount_ml = ? WHERE id = ?", (new_amount, row["id"]))
        goal = row["goal_ml"]
    else:
        new_amount = ml_to_add
        goal = 2500
        cur.execute("INSERT INTO water_tracking (user_id, entry_date, amount_ml, goal_ml) VALUES (?, ?, ?, ?)", (user["id"], TODAY(), new_amount, goal))
    conn.commit()
    conn.close()
    return jsonify({"amount_ml": new_amount, "goal_ml": goal})


# =========================================================
# MEDICINE & TASKS MODULES
# =========================================================
@app.route("/medicine", methods=["GET", "POST"])
def medicine():
    user = database.get_or_create_demo_user()
    conn = database.get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        cur.execute("""
            INSERT INTO medicines (user_id, medicine_name, dosage, time_of_day, notes, taken, entry_date)
            VALUES (?, ?, ?, ?, ?, 0, ?)
        """, (user["id"], request.form.get("medicine_name"), request.form.get("dosage"), request.form.get("time_of_day"), request.form.get("notes"), TODAY()))
        conn.commit()

    medicines = cur.execute("SELECT * FROM medicines WHERE user_id = ? AND entry_date = ? ORDER BY time_of_day", (user["id"], TODAY())).fetchall()
    conn.close()
    return render_template("medicine.html", medicines=medicines)


@app.route("/medicine/taken/<int:medicine_id>", methods=["POST"])
def medicine_taken(medicine_id):
    conn = database.get_connection()
    conn.execute("UPDATE medicines SET taken = 1 WHERE id = ?", (medicine_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("medicine"))


@app.route("/tasks/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    conn = database.get_connection()
    row = conn.execute("SELECT completed FROM daily_tasks WHERE id = ?", (task_id,)).fetchone()
    new_value = 0
    if row:
        new_value = 0 if row["completed"] else 1
        conn.execute("UPDATE daily_tasks SET completed = ? WHERE id = ?", (new_value, task_id))
        conn.commit()
    conn.close()
    return jsonify({"completed": new_value})


# =========================================================
# FAMILY & SETTINGS MODULES
# =========================================================
@app.route("/family")
def family():
    user = database.get_or_create_demo_user()
    conn = database.get_connection()
    members = conn.execute("SELECT * FROM family_members WHERE owner_user_id = ?", (user["id"],)).fetchall()
    conn.close()
    return render_template("family.html", user=user, members=members)


@app.route("/settings")
def settings():
    user = database.get_or_create_demo_user()
    return render_template("settings.html", user=user)


@app.route("/family/member/<int:member_id>")
def family_member_detail(member_id):
    user = database.get_or_create_demo_user()
    conn = database.get_connection()
    member = conn.execute("SELECT * FROM family_members WHERE id = ? AND owner_user_id = ?", (member_id, user["id"])).fetchone()
    activities = conn.execute("SELECT * FROM family_activity WHERE family_member_id = ? ORDER BY created_at DESC", (member_id,)).fetchall()
    conn.close()
    
    if not member:
        return redirect(url_for("family"))

    return render_template("family_member.html", member=member, activities=activities)


# =========================================================
# APPLICATION ENTRY POINT
# =========================================================
if __name__ == "__main__":
    database.init_db()
    app.run(debug=True)