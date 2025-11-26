from agents.analysis_agent import analyze_user_request
from agents.budget_agent import compute_budget_allocation
from agents.weather_agent import summarize_weather_for_swimming
from agents.activities_agent import suggest_activities_for_weekend
from agents.lodging_agent import suggest_lodgings_for_activities
from agents.scenario_agent import build_scenarios


def main() -> None:
    print("=== Planificateur de week-end pour étudiants à Paris ===")
    user_message = input(
        "Décris ton week-end idéal (budget, envies, dates, etc.) :\n> "
    )

    # Agent 1 : Analyse de la demande
    constraints = analyze_user_request(user_message)
    print("\nContraintes extraites par l'agent :")
    print(constraints)

    # Agent 2 : Budget & contraintes
    budget_allocation = compute_budget_allocation(constraints)
    print("\nRépartition du budget :")
    print(budget_allocation)

    # Agent 3 : Météo (pour l'instant, on force Paris)
    weather_summary = summarize_weather_for_swimming(
        city_name="Paris",
        forecast_days=2,
    )
    print("\nRésumé météo :")
    print(weather_summary)

    # Agent 4 : Activités compatibles
    activities = suggest_activities_for_weekend(
        constraints=constraints,
        budget_allocation=budget_allocation,
        weather_summary=weather_summary,
        max_results=3,
    )

    print("\nActivités suggérées :")
    if not activities:
        print("- Aucune activité trouvée avec ce budget et ces contraintes.")
    else:
        for activity in activities:
            print(
                f"- {activity['name']} "
                f"({activity['type']}) ~ {activity['price_estimate']}€"
            )

    # Agent 5 : Logements possibles proches des activités
    lodgings = suggest_lodgings_for_activities(
        activities=activities,
        budget_allocation=budget_allocation,
        max_results_per_activity=2,
    )

    print("\nLogements suggérés :")
    if not lodgings:
        print("- Aucun logement trouvé avec ce budget pour les activités proposées.")
    else:
        for lodging in lodgings:
            print(
                f"- Pour l'activité '{lodging['for_activity']}' : "
                f"{lodging['lodging_name']} à {lodging['city']} "
                f"({lodging['platform']}), "
                f"{lodging['price_per_night']}€/nuit x {lodging['nights']} nuit(s) "
                f"= {lodging['total_price']}€ "
                f"[note {lodging['rating']}]"
            )

    # Agent 6 : Construction de scénarios complets
    scenarios = build_scenarios(
        constraints=constraints,
        budget_allocation=budget_allocation,
        activities=activities,
        lodgings=lodgings,
        max_scenarios=3,
    )

    print("\nScénarios proposés :")
    if not scenarios:
        print("- Aucun scénario complet possible avec ce budget et ces contraintes.")
    else:
        for scenario in scenarios:
            details = scenario["details"]
            print(f"\n{scenario['label']} (≈ {scenario['total_cost_estimate']}€)")
            print(
                f"  - Activité : {details['activity_name']} "
                f"({details['activity_type']}) ~ {details['activity_price']}€"
            )
            print(
                f"  - Logement : {details['lodging_name']} à {details['lodging_city']} "
                f"({details['lodging_platform']}) ~ {details['lodging_total']}€"
            )
            print(
                f"  - Transport estimé : {details['transport_estimate']}€"
            )


if __name__ == "__main__":
    main()
