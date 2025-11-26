from typing import Dict, Any


def compute_budget_allocation(constraints: Dict[str, Any]) -> Dict[str, int]:
    
    budget_total = constraints.get("budget_total")

    if budget_total is None:
        raise ValueError("Le budget total est manquant dans les contraintes.")

    budget_total_int = int(budget_total)

   
    lodging_ratio = 0.5
    activities_ratio = 0.3
    transport_ratio = 0.2

    max_lodging = int(budget_total_int * lodging_ratio)
    max_activities = int(budget_total_int * activities_ratio)
    max_transport = int(budget_total_int * transport_ratio)

    budget_allocation: Dict[str, int] = {
        "budget_total": budget_total_int,
        "max_lodging": max_lodging,
        "max_activities": max_activities,
        "max_transport": max_transport,
    }

    return budget_allocation
