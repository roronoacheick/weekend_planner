from typing import List, Dict, Any


CANDIDATE_LODGINGS: List[Dict[str, Any]] = [
    {
        "lodging_name": "Auberge de jeunesse Porte de Versailles",
        "city": "Paris",
        "near_activity": "Aquaboulevard",
        "platform": "Booking",
        "price_per_night": 35,
        "nights": 1,
        "rating": 7.8,
    },
    {
        "lodging_name": "Studio Airbnb près de la base de loisirs",
        "city": "Cergy",
        "near_activity": "Base de loisirs de Cergy",
        "platform": "Airbnb",
        "price_per_night": 45,
        "nights": 1,
        "rating": 4.6,
    },
    {
        "lodging_name": "Auberge étudiante République",
        "city": "Paris",
        "near_activity": None,
        "platform": "Auberge",
        "price_per_night": 30,
        "nights": 1,
        "rating": 8.2,
    },
    {
        "lodging_name": "Chambre simple près d'un bowling",
        "city": "Paris",
        "near_activity": "Soirée bowling étudiant",
        "platform": "Booking",
        "price_per_night": 40,
        "nights": 1,
        "rating": 7.5,
    },
]


def suggest_lodgings_for_activities(
    activities: List[Dict[str, Any]],
    budget_allocation: Dict[str, int],
    max_results_per_activity: int = 2,
) -> List[Dict[str, Any]]:
   
    max_lodging_budget = budget_allocation.get("max_lodging", 0)

    suggested_lodgings: List[Dict[str, Any]] = []

    if not activities:
        return suggested_lodgings

    for activity in activities:
        activity_city = activity.get("city")
        activity_name = activity.get("name")

        lodgings_for_activity: List[Dict[str, Any]] = []

        for lodging in CANDIDATE_LODGINGS:
            if lodging["city"] != activity_city:
                continue

            total_price = lodging["price_per_night"] * lodging["nights"]

            if total_price > max_lodging_budget:
                continue

            near_activity = lodging.get("near_activity")

            if near_activity is not None and near_activity != activity_name:
                continue

            lodging_option: Dict[str, Any] = {
                "for_activity": activity_name,
                "lodging_name": lodging["lodging_name"],
                "platform": lodging["platform"],
                "city": lodging["city"],
                "price_per_night": lodging["price_per_night"],
                "nights": lodging["nights"],
                "total_price": total_price,
                "rating": lodging["rating"],
            }

            lodgings_for_activity.append(lodging_option)

            if len(lodgings_for_activity) >= max_results_per_activity:
                break

        suggested_lodgings.extend(lodgings_for_activity)

    return suggested_lodgings
