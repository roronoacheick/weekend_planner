from agents.analysis_agent import analyze_user_request
from agents.budget_agent import compute_budget_allocation


def main():
    print("=== Planificateur de week-end pour étudiants à Paris ===")
    user_message = input("Décris ton week-end idéal (budget, envies, dates, etc.) :\n> ")

    constraints = analyze_user_request(user_message)

    print("\nContraintes extraites par l'agent :")
    print(constraints)

    budget_allocation = compute_budget_allocation(constraints)

    print("\nRépartition du budget :")
    print(budget_allocation)


if __name__ == "__main__":
    main()
