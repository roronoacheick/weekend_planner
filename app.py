import streamlit as st

from agents.orchestrator_agent import run_planning_pipeline


def main() -> None:
    st.set_page_config(
        page_title="Planificateur de week-end étudiant à Paris",
        page_icon="🗼",
        layout="centered",
    )

    st.title("Planificateur de week-end étudiant à Paris 🗼")
    st.write(
        "Décris ton week-end idéal (budget, envies, dates, etc.). "
        "L'assistant va te proposer des options réalistes en respectant ton budget."
    )

    user_message = st.text_area(
        "Décris ton week-end idéal :",
        placeholder=(
            "Exemple : J'ai un budget de 120€, je suis à Paris et je veux une activité fun "
            "avec des amis, si possible de la baignade et une nuit sur place."
        ),
        height=150,
    )

    if st.button("Planifier mon week-end ✨"):
        if not user_message.strip():
            st.warning("Merci de décrire ton week-end avant de lancer la planification.")
            return

        with st.spinner("Je prépare tes options de week-end..."):
            result = run_planning_pipeline(user_message)

        # On ne montre plus que ce qui est utile pour l'utilisateur
        weather_summary = result["weather_summary"]
        final_text = result["final_text"]

        # 🌤️ Bloc météo "simple mais cool"
        st.subheader("🌤️ Météo du week-end")

        location = weather_summary.get("location", "la zone")
        swimming_reco = weather_summary.get("swimming_recommendation", "Moyen")
        details = weather_summary.get("details", [])

        if swimming_reco == "OK":
            st.success(
                f"Bonne nouvelle : la météo est globalement **favorable** pour profiter de l'extérieur à {location} 🌞"
            )
        else:
            st.info(
                f"La météo est un peu mitigée autour de {location}. "
                "On mise surtout sur des activités qui restent sympas même sans grand soleil 🙂"
            )

        # Petit résumé jour par jour avec des emojis
        for day in details:
            date_str = day.get("date", "?")
            status = day.get("status", "").lower()

            if status == "ensoleillé":
                icon = "☀️"
                label = "Ensoleillé"
            elif status == "pluie":
                icon = "🌧️"
                label = "Pluie"
            else:
                icon = "⛅️"
                label = "Nuageux"

            st.markdown(f"- {icon} `{date_str}` : **{label}**")

        st.markdown("---")

        # ✨ Bloc final : proposition pour l'utilisateur
        st.subheader("✨ Tes options de week-end")

        # Le texte déjà rédigé par l'agent de présentation (LLM)
        st.markdown(final_text)


if __name__ == "__main__":
    main()
