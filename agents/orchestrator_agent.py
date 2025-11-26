from typing import Dict, Any

from agents.analysis_agent import analyze_user_request
from agents.budget_agent import compute_budget_allocation
from agents.weather_agent import summarize_weather_for_swimming
from agents.activities_agent import suggest_activities_for_weekend
from agents.lodging_agent import suggest_lodgings_for_activities
from agents.scenario_agent import build_scenarios
from agents.presentation_agent import present_scenarios_to_user


def run_planning_pipeline(user_message: str) -> Dict[str, Any]:
    
    constraints = analyze_user_request(user_message)
    budget_allocation = compute_budget_allocation(constraints)

    location = constraints.get("location") or "Paris"

    weather_summary = summarize_weather_for_swimming(
        city_name=location,
        forecast_days=2,
    )

    activities = suggest_activities_for_weekend(
        constraints=constraints,
        budget_allocation=budget_allocation,
        weather_summary=weather_summary,
        max_results=3,
    )

    lodgings = suggest_lodgings_for_activities(
        activities=activities,
        budget_allocation=budget_allocation,
        max_results_per_activity=2,
    )

    scenarios = build_scenarios(
        constraints=constraints,
        budget_allocation=budget_allocation,
        activities=activities,
        lodgings=lodgings,
        max_scenarios=3,
    )

    if scenarios:
        final_text = present_scenarios_to_user(
            constraints=constraints,
            budget_allocation=budget_allocation,
            scenarios=scenarios,
        )
    else:
        final_text = (
            "Pour l'instant, aucun scénario ne respecte ton budget "
            "avec les contraintes actuelles."
        )

    result: Dict[str, Any] = {
        "constraints": constraints,
        "budget_allocation": budget_allocation,
        "weather_summary": weather_summary,
        "activities": activities,
        "lodgings": lodgings,
        "scenarios": scenarios,
        "final_text": final_text,
    }

    return result
