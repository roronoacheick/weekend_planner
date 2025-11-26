from agents.analysis_agent import analyze_user_request
from agents.budget_agent import compute_budget_allocation
from agents.weather_agent import summarize_weather_for_swimming


def main():
    print("=== Planificateur de week-end pour étudiants à Paris ===")
    user_message = input("Décris ton week-end idéal (budget, envies, dates, etc.) :\n> ")

    constraints = analyze_user_request(user_message)

    print("\nContraintes extraites par l'agent :")
    print(constraints)

    budget_allocation = compute_budget_allocation(constraints)

    print("\nRépartition du budget :")
    print(budget_allocation)

    weather_summary = summarize_weather_for_swimming(city_name="Paris", forecast_days=2)

    print("\nRésumé météo :")
    print(weather_summary)


if __name__ == "__main__":
    main()
