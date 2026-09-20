"""
meal_service.py
----------------
Generates a simple, rule-based daily meal plan.

This is NOT real AI - it just picks from a few pre-written meal
options based on the user's diet preference (veg / non-veg) and
goal. This keeps the logic easy to read and easy to change.

To edit the meals: just change the text inside VEG_MEALS / NONVEG_MEALS.
"""

VEG_MEALS = {
    "breakfast": {
        "title": "Poha with peanuts and vegetables",
        "calories": 280, "protein": 7, "carbs": 45, "fat": 8, "fiber": 5
    },
    "lunch": {
        "title": "2 Roti, Dal, Mixed Vegetable, Salad",
        "calories": 420, "protein": 17, "carbs": 58, "fat": 10, "fiber": 9
    },
    "snack": {
        "title": "Roasted chana with a cup of tea",
        "calories": 150, "protein": 8, "carbs": 20, "fat": 4, "fiber": 6
    },
    "dinner": {
        "title": "Vegetable khichdi with curd",
        "calories": 380, "protein": 12, "carbs": 55, "fat": 9, "fiber": 7
    }
}

NONVEG_MEALS = {
    "breakfast": {
        "title": "Boiled eggs with whole wheat toast",
        "calories": 300, "protein": 16, "carbs": 30, "fat": 12, "fiber": 4
    },
    "lunch": {
        "title": "2 Roti, Chicken curry, Salad",
        "calories": 460, "protein": 28, "carbs": 45, "fat": 14, "fiber": 6
    },
    "snack": {
        "title": "Sprouts salad with lemon",
        "calories": 140, "protein": 9, "carbs": 18, "fat": 3, "fiber": 6
    },
    "dinner": {
        "title": "Grilled fish with steamed vegetables",
        "calories": 400, "protein": 30, "carbs": 30, "fat": 14, "fiber": 6
    }
}

MEAL_LABELS = {
    "breakfast": "Breakfast",
    "lunch": "Lunch",
    "snack": "Evening Snack",
    "dinner": "Dinner"
}


def generate_meal_plan(diet, goal):
    """
    Return a simple 4-meal plan (breakfast/lunch/snack/dinner).
    diet: 'veg' or 'non-veg'
    goal: the user's main wellness goal (used only for the "why" text)
    """
    base = NONVEG_MEALS if diet == "non-veg" else VEG_MEALS

    plan = []
    for key, label in MEAL_LABELS.items():
        meal = dict(base[key])  # copy so we don't change the original
        meal["label"] = label
        meal["why"] = build_why_text(goal)
        plan.append(meal)

    return plan


def build_why_text(goal):
    """Build a short, friendly explanation for the 'Why?' popup."""
    if not goal:
        goal = "general wellness"
    return (
        f"Your goal is {goal}. This meal provides a balance of protein, "
        f"carbohydrates and fiber. Portion size and your overall daily diet "
        f"matter too - this is general guidance, not a medical prescription."
    )
