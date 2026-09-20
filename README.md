# 🌿 AarogyaSaathi

**Your Health. Your Routine. Your Saathi.**

A beginner-friendly Flask + SQLite wellness app: profile & BMI, a simple
meal plan, an exercise plan with a full **Yoga** section (pose popups with
step-by-step instructions), a water tracker, medicine reminders, daily
tasks, and a simplified Family Health Circle.

This is a **real, running Flask application** — not a static mockup.

---

## What's implemented vs. placeholder

| Feature | Status |
|---|---|
| Profile, BMI, health conditions, goal | ✅ Working |
| Rule-based meal plan + "Why?" popup | ✅ Working |
| Meal photo upload | ✅ Upload works, analysis is a **labelled demo** (see below) |
| Exercise plan (walking/stretching/etc.) | ✅ Working |
| Yoga: when to/not to practice, 6 poses with popup instructions | ✅ Working |
| AI Exercise Coach (camera, pose detection) | 🚧 "Coming Soon" placeholder |
| Water tracker with +250/+500 ml buttons | ✅ Working (AJAX, no page reload) |
| Medicine reminders (add / mark taken) | ✅ Working |
| Daily tasks checklist + pending-task popup | ✅ Working |
| Family Health Circle (add member, sharing permissions, activity) | ✅ Simplified working version — see note below |
| English / Hindi language switch | ✅ Working for navigation & key headings — see note below |

**Honesty notes (please read):**
- **Meal photo analysis** does not use real AI/computer vision yet. It
  clearly labels its result as a **demo analysis** — see
  `services/meal_analyzer.py` for exactly where to plug in a real model.
- **Family Health Circle** in this version does **not** use real
  multi-user logins. You add a family member as a profile on your own
  account (with sharing toggles and demo activity numbers), which is
  the simplest way to demonstrate the feature for a college project.
  Real family-to-family syncing would need a login system
  (e.g. Flask-Login) — a great "Phase 2" addition.
- **Hindi translation** covers navigation, the welcome page, and the
  dashboard headings, using a simple dictionary system
  (`translations.py`). It is NOT yet translated line-by-line across
  every single page — extending it is described below.

---

## Project Structure

```
AarogyaSaathi/
│
├── app.py                  # All Flask routes (pages) live here
├── database.py              # Creates SQLite tables + demo user helper
├── translations.py          # English/Hindi text dictionary
├── requirements.txt
├── README.md
│
├── templates/                # HTML pages (Jinja2)
│   ├── base.html             # Shared layout: navbar, footer, language switch
│   ├── index.html            # Welcome screen
│   ├── profile.html
│   ├── dashboard.html
│   ├── meal.html
│   ├── meal_analyze.html
│   ├── exercise.html         # Includes the full Yoga section
│   ├── water.html
│   ├── medicine.html
│   ├── family.html
│   ├── family_member.html
│   └── settings.html
│
├── static/
│   ├── css/style.css         # All styling, one file, CSS variables at top
│   ├── js/app.js             # Small shared helpers (popup close on Esc)
│   └── images/
│
├── uploads/                  # Where meal photos are saved (created empty)
│
└── services/                 # "Business logic", kept separate from routes
    ├── health_service.py     # calculate_bmi()
    ├── meal_service.py       # generate_meal_plan()
    ├── exercise_service.py   # get_exercise_plan(), get_yoga_poses()
    └── meal_analyzer.py      # Placeholder for future photo AI
```

---

## Installation

```bash
python -m venv venv
```

Activate it:

- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Open your browser at: **http://127.0.0.1:5000**

The first time you run it, `aarogyasaathi.db` (a SQLite file) is created
automatically in the project folder — you don't need to set up a database
yourself.

---

## How to modify things

**Change the meal plan** → edit `services/meal_service.py`. The
`VEG_MEALS` and `NONVEG_MEALS` dictionaries hold the meal text and
nutrition numbers.

**Change the exercises or yoga poses** → edit
`services/exercise_service.py`. Each yoga pose is one dictionary with
`name`, `sanskrit`, `svg` (the little illustration), `steps`,
`benefits`, and `caution`. Copy an existing block to add a new pose.

**Change Hindi/English text** → edit `translations.py`. Add a new key
with both `"en"` and `"hi"` versions, then use `{{ t('your_key') }}`
in any template.

**Change the water goal** → the default (2500 ml) is set in
`app.py`, inside the `water_add()` function and `database.py`'s
`water_tracking` table default. Change `2500` there.

**Change how medicine reminders work** → see the `/medicine` route in
`app.py`. Reminders are only ever what the user typed in — the app
never suggests or changes dosages.

**Change how family connections work** → see the `/family/add` route
in `app.py` and the `family_members` table in `database.py`. Sharing
permission checkboxes control which stats show on that member's card.

---

## Where to add real AI later

- **`services/meal_analyzer.py`** — this is where OpenCV + a food
  recognition model (like YOLO) would go. The function
  `analyze_meal_photo()` currently returns a clearly labelled demo
  result; swap it for real detection + a nutrition lookup table.

- **AI Exercise Coach** (not yet built) — the plan is:
  `Camera → OpenCV → MediaPipe Pose → joint angles → rep counting → form feedback`.
  The "Coming Soon" card on the Exercise page marks exactly where this
  would appear once built.

---

## ⚠️ Disclaimer

AarogyaSaathi provides general wellness information and reminders. It
is not a replacement for a qualified doctor or medical professional.
For diagnosis, treatment, medication changes, or urgent concerns,
consult a healthcare professional. Medicine reminders only reflect
information entered by the user — the app never prescribes or changes
medication.
