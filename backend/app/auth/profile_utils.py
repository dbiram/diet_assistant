def compute_daily_targets(profile_data: dict):
    weight = profile_data["weight_kg"]
    activity = profile_data["activity_level"]

    # Caloric multiplier
    base_cal = 24 * weight  # Basal metabolic rate
    multiplier = {
        "low": 1.3,
        "moderate": 1.55,
        "high": 1.75
    }[activity]

    maintenance = base_cal * multiplier
    deficit = (profile_data["weight_kg"] - profile_data["target_weight_kg"]) * 7700 / profile_data["timeframe_weeks"] / 7

    # Day-based calories
    cal_rest = int(maintenance - deficit)
    cal_workout = int(maintenance - deficit + 200)  # Small boost on workout days

    # Protein = 1.8g/kg on workout days, 1.2g/kg otherwise
    prot_workout = int(1.8 * weight)
    prot_rest = int(1.2 * weight)

    return {
        "calories_workout_day": cal_workout,
        "calories_rest_day": cal_rest,
        "protein_grams_workout_day": prot_workout,
        "protein_grams_rest_day": prot_rest,
    }
