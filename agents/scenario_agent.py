from typing import List, Dict, Any


def estimate_transport_cost(activity_city: str, lodging_city: str) -> int:
    
    if activity_city == lodging_city:
        return 10  # transports en commun dans la même ville
    else:
        return 20  # RER / train + métro par exemple


def build_scenarios(
    constraints: Dict[str, Any],
    budget_allocation: Dict[str, int],
    activities: List[Dict[str, Any]],
    lodgings: List[Dict[str, Any]],
    max_scenarios: int = 3,
) -> List[Dict[str, Any]]:
   
    budget_total = budget_allocation.get("budget_total", 0)

    scenarios: List[Dict[str, Any]] = []

    if not activities or not lodgings:
        return scenarios

    for lodging in lodgings:
        activity_name = lodging.get("for_activity")

        matching_activity = None
        for activity in activities:
            if activity.get("name") == activity_name:
                matching_activity = activity
                break

        if matching_activity is None:
            continue

        activity_city = matching_activity.get("city", "")
        lodging_city = lodging.get("city", "")

        transport_estimate = estimate_transport_cost(
            activity_city=activity_city,
            lodging_city=lodging_city,
        )

        activity_price = matching_activity.get("price_estimate", 0)
        lodging_total = lodging.get("total_price", 0)

        total_cost = activity_price + lodging_total + transport_estimate

        if total_cost > budget_total:
            continue

        scenario: Dict[str, Any] = {
            "label": "",  # on le remplira après tri
            "total_cost_estimate": total_cost,
            "details": {
                "activity_name": matching_activity.get("name"),
                "activity_type": matching_activity.get("type"),
                "activity_price": activity_price,
                "lodging_name": lodging.get("lodging_name"),
                "lodging_platform": lodging.get("platform"),
                "lodging_city": lodging_city,
                "lodging_total": lodging_total,
                "transport_estimate": transport_estimate,
            },
        }

        scenarios.append(scenario)

    scenarios.sort(key=lambda s: s["total_cost_estimate"])

    for index, scenario in enumerate(scenarios):
        if index == 0:
            label = "Option 1 - Économique"
        elif index == 1:
            label = "Option 2 - Confort"
        else:
            label = f"Option {index + 1}"
        scenario["label"] = label

    return scenarios[:max_scenarios]
