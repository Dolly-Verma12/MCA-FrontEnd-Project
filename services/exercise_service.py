"""
exercise_service.py
--------------------
Provides two things:

1. get_exercise_plan()  -> a short list of general, beginner-friendly
   exercises (walking, stretching, bodyweight movements).

2. get_yoga_poses()     -> a list of beginner yoga poses, each with
   step-by-step instructions, benefits and a caution note. This is the
   data used by the Yoga section on the Exercise page, shown as
   click-to-open popups.

This file does NOT do any real computer vision. The "AI Exercise Coach"
(pose detection, rep counting) is a placeholder for now - see the
"Coming Soon" card on the exercise page, and the notes in README.md
about where to plug in OpenCV / MediaPipe later.
"""


def get_exercise_plan():
    """Return a short list of general beginner exercises."""
    return [
        {
            "name": "Walking",
            "duration": "20 minutes",
            "difficulty": "Beginner",
            "why": "Walking may support general fitness and can help improve mood and stamina."
        },
        {
            "name": "Stretching",
            "duration": "10 minutes",
            "difficulty": "Beginner",
            "why": "Gentle stretching can help improve flexibility and may help maintain mobility."
        },
        {
            "name": "Bodyweight Exercise",
            "duration": "10 minutes",
            "difficulty": "Beginner",
            "why": "Simple bodyweight moves (like squats or wall push-ups) may support general strength."
        }
    ]


def get_yoga_poses():
    """
    Return beginner yoga poses as a list of dictionaries.
    'svg' holds a small hand-drawn illustration (no external images needed,
    so the page always loads instantly and works offline).
    """
    return [
        {
            "name": "Mountain Pose",
            "sanskrit": "Tadasana",
            "svg": '<svg viewBox="0 0 100 100" fill="none" stroke="#2E7D5B" stroke-width="5" stroke-linecap="round"><circle cx="50" cy="16" r="9" fill="#2E7D5B" stroke="none"/><path d="M50 25v40M50 32l-14 12M50 32l14 12M50 65l-10 28M50 65l10 28"/></svg>',
            "steps": [
                "Stand with your feet together, weight spread evenly on both feet.",
                "Engage your thighs gently and lengthen your spine upward.",
                "Let your arms rest by your sides or reach overhead, palms facing in.",
                "Relax your shoulders down and breathe slowly for 5-8 breaths."
            ],
            "benefits": ["Improves posture and balance", "Builds body awareness", "Calms the mind before other poses"],
            "caution": "Avoid locking your knees. If balance is difficult, stand with feet hip-width apart."
        },
        {
            "name": "Tree Pose",
            "sanskrit": "Vrikshasana",
            "svg": '<svg viewBox="0 0 100 100" fill="none" stroke="#2E7D5B" stroke-width="5" stroke-linecap="round"><circle cx="50" cy="16" r="9" fill="#2E7D5B" stroke="none"/><path d="M50 25v42M50 34l-14 10M50 34l14 10M50 67l-8 25M50 67l12-4 8-22"/></svg>',
            "steps": [
                "Stand tall and shift your weight onto one foot.",
                "Place the sole of your other foot on your inner calf or thigh (not directly on the knee).",
                "Bring your palms together at your chest, or raise your arms overhead.",
                "Pick a still point ahead to focus on, and hold for 20-30 seconds. Repeat on the other side."
            ],
            "benefits": ["Builds balance and focus", "Strengthens the standing leg and ankle", "Improves concentration"],
            "caution": "If you wobble, keep a hand on a wall for support. Never rest your foot directly on the knee joint."
        },
        {
            "name": "Cobra Pose",
            "sanskrit": "Bhujangasana",
            "svg": '<svg viewBox="0 0 100 100" fill="none" stroke="#2E7D5B" stroke-width="5" stroke-linecap="round"><path d="M18 82h64M22 82 C22 62 34 46 50 44 C66 42 76 28 76 16"/><circle cx="78" cy="12" r="9" fill="#2E7D5B" stroke="none"/></svg>',
            "steps": [
                "Lie face down with your legs together and the tops of your feet on the mat.",
                "Place your palms under your shoulders, elbows close to your body.",
                "Press into your hands and gently lift your chest, keeping your hips grounded.",
                "Keep your elbows slightly bent, hold for 15-30 seconds, then lower down slowly."
            ],
            "benefits": ["Opens the chest and shoulders", "Gently strengthens the back", "Improves spine mobility"],
            "caution": "Do not force the lift. Stop if you feel any pinching pain in your lower back."
        },
        {
            "name": "Child's Pose",
            "sanskrit": "Balasana",
            "svg": '<svg viewBox="0 0 100 100" fill="none" stroke="#2E7D5B" stroke-width="5" stroke-linecap="round"><path d="M20 84 C20 60 40 60 40 84"/><path d="M40 84 L80 60"/><circle cx="82" cy="56" r="9" fill="#2E7D5B" stroke="none"/></svg>',
            "steps": [
                "Kneel on the mat with your big toes touching, knees apart.",
                "Sit back onto your heels, then fold your torso forward between your thighs.",
                "Stretch your arms forward or rest them alongside your body.",
                "Rest your forehead on the mat and breathe slowly for 1-3 minutes."
            ],
            "benefits": ["Releases tension in the back", "Calms the nervous system", "A gentle resting pose between others"],
            "caution": "If it's uncomfortable on the knees, place a folded blanket underneath them."
        },
        {
            "name": "Seated Forward Bend",
            "sanskrit": "Paschimottanasana",
            "svg": '<svg viewBox="0 0 100 100" fill="none" stroke="#2E7D5B" stroke-width="5" stroke-linecap="round"><path d="M16 82 L62 82"/><path d="M16 82 C16 70 28 68 32 80"/><path d="M16 82 C40 80 56 60 68 28"/><circle cx="70" cy="22" r="9" fill="#2E7D5B" stroke="none"/></svg>',
            "steps": [
                "Sit with your legs extended straight in front of you.",
                "Inhale and lengthen your spine upward.",
                "Exhale and hinge forward from your hips, reaching toward your feet.",
                "Keep your back long rather than rounding it, and hold for 30-60 seconds."
            ],
            "benefits": ["Stretches the hamstrings and lower back", "Calms the mind", "Improves flexibility over time"],
            "caution": "Bend your knees slightly if your hamstrings feel tight. Never force the stretch."
        },
        {
            "name": "Corpse Pose",
            "sanskrit": "Shavasana",
            "svg": '<svg viewBox="0 0 100 100" fill="none" stroke="#2E7D5B" stroke-width="5" stroke-linecap="round"><path d="M14 60 L86 60"/><circle cx="20" cy="60" r="9" fill="#2E7D5B" stroke="none"/><path d="M38 60 L34 70M50 60 L50 72M62 60 L66 70"/></svg>',
            "steps": [
                "Lie flat on your back with your legs relaxed, slightly apart.",
                "Let your arms rest by your sides, palms facing up.",
                "Close your eyes and let your whole body go loose.",
                "Breathe naturally and stay still for 3-5 minutes to finish your practice."
            ],
            "benefits": ["Lets the body absorb the effects of practice", "Deep relaxation", "Lowers stress before returning to the day"],
            "caution": "If lying flat is uncomfortable, place a rolled towel under your knees."
        }
    ]


def get_yoga_timing_guide():
    """Return the 'when to practice / when to avoid' guidance shown on the page."""
    return {
        "good_times": [
            "Early morning, on an empty stomach",
            "Evening, 2-3 hours after a meal",
            "Same time every day, to build a habit",
            "A quiet, well-ventilated space",
            "Wearing loose, comfortable clothes"
        ],
        "avoid_times": [
            "Right after a heavy meal",
            "During high fever or illness",
            "With a fresh injury or sharp pain",
            "During pregnancy, without a doctor's guidance",
            "After surgery, until a doctor clears you",
            "If you feel dizzy or extremely tired - rest instead"
        ]
    }
