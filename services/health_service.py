"""
health_service.py
------------------
Simple health-related calculations, kept separate from app.py
so the routes file stays easy to read.
"""


def calculate_bmi(weight_kg, height_cm):
    """
    Calculate BMI using the user's weight (kg) and height (cm).
    Formula: weight (kg) / height (m) squared
    """
    if not weight_kg or not height_cm:
        return None
    height_m = height_cm / 100
    bmi = weight_kg / (height_m * height_m)
    return round(bmi, 1)


def bmi_category(bmi):
    """
    Return a simple, non-diagnostic label for a BMI value.
    This is general wellness information, not a medical diagnosis.
    """
    if bmi is None:
        return ""
    if bmi < 18.5:
        return "Below healthy range"
    elif bmi < 25:
        return "Healthy range"
    elif bmi < 30:
        return "Above healthy range"
    else:
        return "Well above healthy range"
