from agents.orchestrator_agent import run_planning_pipeline


def main() -> None:
    print("=== Planificateur de week-end pour étudiants à Paris ===")
    user_message = input(
        "Décris ton week-end idéal (budget, envies, dates, etc.) :\n> "
    )

    result = run_planning_pipeline(user_message)

    constraints = result["constraints"]
    budget_allocation = result["budget_allocation"]
    weather_summary = result["weather_summary"]
    activities = result["activities"]
    lodgings = result["lodgings"]
    scenarios = result["scenarios"]
    final_text = result["final_text"]

    print("\nContraintes extraites par l'agent :")
    print(constraints)

    print("\nRépartition du budget :")
    print(budget_allocation)

    print("\nRésumé météo :")
    print(weather_summary)

    print("\nActivités suggérées :")
    if not activities:
        print("- Aucune activité trouvée avec ce budget et ces contraintes.")
    else:
        for activity in activities:
            print(
                f"- {activity['name']} "
                f"({activity['type']}) ~ {activity['price_estimate']}€"
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

    print("\n=== Proposition finale ===")
    print(final_text)


if __name__ == "__main__":
    main()
