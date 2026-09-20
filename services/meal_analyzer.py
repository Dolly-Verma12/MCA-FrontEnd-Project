"""
meal_analyzer.py
-----------------
PLACEHOLDER for future meal-photo recognition.

Right now this does NOT use any real AI or computer vision.
It only returns a clearly-labelled demo result, so the app never
pretends to recognise food when it actually can't.

------------------------------------------------------------------
HOW TO CONNECT REAL AI LATER:

    Camera / Uploaded Photo
        -> OpenCV (read/prepare the image)
        -> YOLO or another food-recognition model (detect food items)
        -> Nutrition lookup (match detected food to a nutrition table)
        -> return real numbers instead of the demo ones below

Steps to add it yourself later:
    1. pip install opencv-python ultralytics  (or your chosen model)
    2. Load the image using OpenCV inside analyze_meal_photo()
    3. Run the model on the image to get a list of detected foods
    4. Look up each food's nutrition and add it to the totals
    5. Return real values instead of DEMO_RESULT
------------------------------------------------------------------
"""

DEMO_RESULT = {
    "is_demo": True,
    "meal_title": "Rice + Dal + Vegetables",
    "calories": 450,
    "protein": 18,
    "carbs": 65,
    "fat": 12,
    "fiber": 8,
    "minerals": ["Iron", "Calcium", "Potassium"],
    "vitamins": ["Vitamin A", "Vitamin C"],
    "health_score": 82,
    "score_label": "Good Choice",
    "reasons": [
        {"ok": True, "text": "Good protein"},
        {"ok": True, "text": "Contains vegetables"},
        {"ok": True, "text": "Good fiber"},
        {"ok": False, "text": "Carbohydrates are moderate/high"},
        {"ok": False, "text": "Portion size matters"}
    ]
}


def analyze_meal_photo(image_file):
    """
    image_file: the uploaded file (not actually analysed yet).

    Real-time AI food recognition is not implemented in this version.
    We return a clearly labelled demo analysis instead, so the app
    is always honest with the user about what it can currently do.
    """
    return DEMO_RESULT
