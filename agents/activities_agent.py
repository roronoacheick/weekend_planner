from typing import List, Dict, Any


CANDIDATE_ACTIVITIES: List[Dict[str, Any]] = [
    {
        "name": "Piscine municipale pas chère",
        "city": "Paris",
        "price_estimate": 6,
        "type": "piscine intérieure",
        "is_outdoor": False,
        "duration_hours": 2,
    },
    {
        "name": "Aquaboulevard",
        "city": "Paris",
        "price_estimate": 35,
        "type": "parc aquatique",
        "is_outdoor": True,
        "duration_hours": 4,
    },
    {
        "name": "Soirée bowling étudiant",
        "city": "Paris",
        "price_estimate": 15,
        "type": "bowling",
        "is_outdoor": False,
        "duration_hours": 3,
    },
    {
        "name": "Escape game entre amis",
        "city": "Paris",
        "price_estimate": 25,
        "type": "escape game",
        "is_outdoor": False,
        "duration_hours": 1.5,
    },
]


def suggest_activities_for_weekend(
    constraints: Dict[str, Any],
    budget_allocation: Dict[str, int],
    weather_summary: Dict[str, Any],
    max_results: int = 3,
) -> List[Dict[str, Any]]:
    
    max_activities_budget = budget_allocation.get("max_activities", 0)
    user_preferences = constraints.get("preferences", [])
    location = constraints.get("location", "Paris")

    swimming_recommendation = weather_summary.get("swimming_recommendation", "Moyen")

    filtered_activities: List[Dict[str, Any]] = []

    for activity in CANDIDATE_ACTIVITIES:
        if activity["price_estimate"] > max_activities_budget:
            continue

        if activity["city"] not in (location, "Paris"):
            continue

        is_swimming_activity = "piscine" in activity["type"] or "baignade" in activity["type"]

        if is_swimming_activity and activity["is_outdoor"] and swimming_recommendation != "OK":
            continue

        if user_preferences:
            preferences_text = " ".join(user_preferences).lower()
            type_text = activity["type"].lower()

            if (
                "baignade" in preferences_text
                or "piscine" in preferences_text
                or "se baigner" in preferences_text
            ):
                if not is_swimming_activity:
                    continue
            elif (
                "sortir" in preferences_text
                or "amis" in preferences_text
                or "soirée" in preferences_text
            ):
                if not (
                    "bowling" in type_text
                    or "escape game" in type_text
                ):
                    continue

        filtered_activities.append(activity)

        if len(filtered_activities) >= max_results:
            break

    return filtered_activities
