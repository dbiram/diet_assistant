import re
from typing import List, Dict
from app.vision.nutrition_lookup import get_nutrition

def parse_meal_prompt(prompt: str) -> List[Dict]:
    """
    Extracts food items from prompt and returns nutrition estimates.
    Very basic NLP for now.
    """
    # Naive split by 'and', commas etc.
    food_items = re.split(r",|\band\b", prompt.lower())
    parsed = []
    for item in food_items:
        item = item.strip()
        if not item:
            continue
        nutrition = get_nutrition(item)
        if nutrition.get("calories") == "unknown":
            continue
        parsed.append({
            "food_name": item,
            "calories": float(nutrition.get("calories", 0) or 0),
            "protein": float(nutrition.get("protein", 0) or 0)
        })
    return parsed

def parse_workout_prompt(prompt: str) -> List[Dict]:
    """
    Very naive rule-based parser: looks for activity + duration pattern.
    """
    workout_data = []
    prompt = prompt.lower()

    # e.g., "30 minutes of running", "ran for 20 minutes", "15 min pushups"
    matches = re.findall(
        r"(\d{1,3})\s*(?:minutes|min)?(?:\s*of)?\s*([a-zA-Z ]+?)(?=,|\band\b|\.|$)",
        prompt
    )

    METS = {
        "running": 9.8,
        "jogging": 7.0,
        "walking": 3.5,
        "cycling": 7.5,
        "pushups": 5.0,
        "yoga": 3.0,
        "weight lifting": 6.0
        # Add more if needed
    }

    for duration, activity in matches:
        activity = activity.strip()
        if activity not in METS:
            continue
        duration = float(duration)
        met = METS.get(activity, 5.0)  # default if unknown

        calories_burned = (met * 3.5 * 70 / 200) * duration  # 70kg person
        workout_data.append({
            "workout_type": activity,
            "duration_minutes": duration,
            "calories_burned": round(calories_burned, 2)
        })

    return workout_data

def detect_intent(prompt: str) -> str:
    prompt = prompt.lower()

    # Summary request
    if any(kw in prompt for kw in ["how did i do", "what's my progress", "how am i doing", "summary"]):
        return "summary"

    # Suggestion request
    if any(kw in prompt for kw in ["what should i eat", "recommend", "suggest", "dinner", "lunch idea"]):
        return "suggestion"

    # Meal logging
    if any(kw in prompt for kw in ["i ate", "i had", "for breakfast", "for lunch", "for dinner"]):
        return "meal_log"
    if parse_meal_prompt(prompt):
        return "meal_log"

    # Workout logging
    if any(kw in prompt for kw in ["i did", "i worked out", "exercise", "training", "gym"]):
        return "workout_log"
    if parse_workout_prompt(prompt):
        return "workout_log"

    # Fallback → general question
    return "rag_question"
