"""
translations.py
----------------
A simple dictionary-based translation system.

HOW IT WORKS:
    - Every piece of text has a "key" (like "nav_dashboard")
    - Each key has an English and a Hindi version
    - In templates we call {{ t('nav_dashboard') }} instead of typing
      the English text directly

HOW TO ADD MORE TRANSLATIONS:
    1. Add a new key to TEXT below, with both "en" and "hi" versions
    2. Use {{ t('your_new_key') }} anywhere in your HTML templates

This starter covers the main navigation, dashboard and section titles.
Extend the same pattern to translate meal/exercise/family page text too.
"""

TEXT = {
    "app_name":        {"en": "AarogyaSaathi", "hi": "आरोग्यसाथी"},
    "tagline":         {"en": "Your Health. Your Routine. Your Saathi.",
                         "hi": "आपकी सेहत। आपकी दिनचर्या। आपका साथी।"},
    "nav_dashboard":   {"en": "Dashboard", "hi": "डैशबोर्ड"},
    "nav_meal":        {"en": "Meals", "hi": "भोजन"},
    "nav_exercise":    {"en": "Exercise & Yoga", "hi": "व्यायाम और योग"},
    "nav_water":       {"en": "Water", "hi": "पानी"},
    "nav_medicine":    {"en": "Medicine", "hi": "दवा"},
    "nav_tasks":       {"en": "Tasks", "hi": "कार्य"},
    "nav_family":      {"en": "Family", "hi": "परिवार"},
    "nav_settings":    {"en": "Settings", "hi": "सेटिंग्स"},

    "welcome_heading": {"en": "Let's understand your health and build a routine made for you.",
                         "hi": "आइए आपकी सेहत को समझें और आपके लिए एक दिनचर्या बनाएं।"},
    "begin_button":    {"en": "Let's Begin", "hi": "शुरू करें"},

    "dashboard_greeting": {"en": "Here's your health summary for today.",
                            "hi": "आज के लिए आपकी सेहत का सारांश यहाँ है।"},
    "todays_focus":    {"en": "Today's Focus", "hi": "आज का फोकस"},

    "water_goal_pending": {"en": "Your water goal is still pending.",
                            "hi": "आपका पानी पीने का लक्ष्य अभी बाकी है।"},

    "disclaimer": {
        "en": "AarogyaSaathi provides general wellness information and reminders. "
              "It is not a replacement for a qualified doctor or medical professional. "
              "For diagnosis, treatment, medication changes or urgent concerns, consult "
              "a healthcare professional.",
        "hi": "आरोग्यसाथी सामान्य स्वास्थ्य जानकारी और रिमाइंडर देता है। यह किसी योग्य "
              "डॉक्टर या चिकित्सा पेशेवर का विकल्प नहीं है। निदान, उपचार, दवा में बदलाव "
              "या तत्काल चिंता के लिए कृपया एक स्वास्थ्य विशेषज्ञ से सलाह लें।"
    }
}


def get_text(key, lang="en"):
    """Look up one piece of text by key, in the given language."""
    entry = TEXT.get(key)
    if not entry:
        return key  # fallback so a missing key never crashes the page
    return entry.get(lang, entry["en"])
