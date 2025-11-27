import streamlit as st

from agents.orchestrator_agent import run_planning_pipeline
from agents.speech_to_text_agent import transcribe_audio_file


def main() -> None:
    st.set_page_config(
        page_title="Planificateur de week-end étudiant à Paris",
        page_icon="🗼",
        layout="centered",
    )

    st.title("Planificateur de week-end étudiant à Paris 🗼")
    st.write(
        "Décris ton week-end idéal (budget, envies, dates, etc.) "
        "ou parle directement au micro. "
        "L'assistant va te proposer des options réalistes en respectant ton budget."
    )

    # 📝 Zone texte classique
    user_message = st.text_area(
        "Décris ton week-end idéal :",
        placeholder=(
            "Exemple : J'ai un budget de 120€, je suis à Paris et je veux une activité fun "
            "avec des amis, si possible de la baignade et une nuit sur place."
        ),
        height=150,
    )

    # 🎙️ Enregistrement direct au micro (pas besoin d'uploader un fichier)
    mic_audio = st.audio_input("…ou clique ici et parle directement 🎙️")

    if st.button("Planifier mon week-end ✨"):
        if not user_message.strip() and mic_audio is None:
            st.warning(
                "Écris ton message OU parle dans le micro avant de lancer la planification 🙂"
            )
            return

        final_user_text = user_message.strip()

        # Si pas de texte mais un enregistrement micro → on fait la transcription
        if not final_user_text and mic_audio is not None:
            with st.spinner("Je transcris ton message vocal avec Groq... 🎧"):
                mic_audio.seek(0)
                transcript = transcribe_audio_file(
                    file_obj=mic_audio,
                    filename="mic_recording.webm",  # nom arbitraire
                    language="fr",
                )
            st.info(f"Transcription de ton vocal :\n\n> {transcript}")
            final_user_text = transcript

        if not final_user_text:
            st.error(
                "Je n'ai pas réussi à récupérer de texte. "
                "Réessaie en dictant plus clairement ou en écrivant ton message."
            )
            return

        with st.spinner("Je prépare tes options de week-end..."):
            result = run_planning_pipeline(final_user_text)

        weather_summary = result["weather_summary"]
        final_text = result["final_text"]

        # 🌤️ Bloc météo "simple mais cool"
        st.subheader("🌤️ Météo du week-end")

        location = weather_summary.get("location", "la zone")
        swimming_reco = weather_summary.get("swimming_recommendation", "Moyen")
        details = weather_summary.get("details", [])

        if swimming_reco == "OK":
            st.success(
                f"Bonne nouvelle : la météo est globalement **favorable** "
                f"pour profiter de l'extérieur à {location} 🌞"
            )
        else:
            st.info(
                f"La météo est un peu mitigée autour de {location}. "
                "On mise surtout sur des activités qui restent sympas même sans grand soleil 🙂"
            )

        # Petit résumé jour par jour avec des emojis + températures
        for day in details:
            date_str = day.get("date", "?")
            status = day.get("status", "").lower()
            max_temp_c = day.get("max_temp_c", "?")

            if status == "ensoleillé":
                icon = "☀️"
                label = "Ensoleillé"
            elif status == "pluie":
                icon = "🌧️"
                label = "Pluie"
            else:
                icon = "⛅️"
                label = "Nuageux"

            st.markdown(
                f"- {icon} `{date_str}` : **{label}** — **{max_temp_c}°C**"
            )

        st.markdown("---")

        # ✨ Bloc final : proposition pour l'utilisateur
        st.subheader("✨ Tes options de week-end")

        st.markdown(final_text)


if __name__ == "__main__":
    main()
