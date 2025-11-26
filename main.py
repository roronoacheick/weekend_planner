from groq import Groq
from config import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)

def run_groq_test():
    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Tu es un assistant qui parle français simplement."
            },
            {
                "role": "user",
                "content": "Dis bonjour à un étudiant qui veut organiser un week-end à Paris."
            }
        ],
    )

    assistant_message = chat_completion.choices[0].message.content
    print("Réponse du modèle :")
    print(assistant_message)


if __name__ == "__main__":
    run_groq_test()
