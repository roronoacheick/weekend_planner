from typing import List, Dict, Any
from pathlib import Path
import json

from groq import Groq

from config import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)

BASE_DIR = Path(__file__).resolve().parent.parent

PROMPT_FILE_PATH = BASE_DIR / "prompts" / "prompt.txt"
CONTEXT_FILE_PATH = BASE_DIR / "prompts" / "context.txt"
ACTIVITIES_INSTRUCTIONS_FILE_PATH = (
    BASE_DIR / "prompts" / "activities_web_instructions.txt"
)


def load_text_file(file_path: Path) -> str:
    
    return file_path.read_text(encoding="utf-8")


def build_system_message_for_activities() -> str:
    
    base_prompt = load_text_file(PROMPT_FILE_PATH)
    base_context = load_text_file(CONTEXT_FILE_PATH)
    activities_instructions = load_text_file(ACTIVITIES_INSTRUCTIONS_FILE_PATH)

    full_system_message = (
        base_prompt
        + "\n\n"
        + base_context
        + "\n\n"
        + activities_instructions
    )

    return full_system_message


def suggest_activities_for_weekend(
    constraints: Dict[str, Any],
    budget_allocation: Dict[str, int],
    weather_summary: Dict[str, Any],
    max_results: int = 3,
) -> List[Dict[str, Any]]:
    
    system_message = build_system_message_for_activities()

    # On envoie au modèle un contexte structuré
    context_payload = {
        "constraints": constraints,
        "budget_allocation": budget_allocation,
        "weather_summary": weather_summary,
        "max_results": max_results,
    }

    user_content = (
        "Voici les données JSON du contexte (contraintes, budget, météo) "
        "pour proposer des activités adaptées :\n\n"
        + json.dumps(context_payload, ensure_ascii=False, indent=2)
    )

    # ⚡ On utilise groq/compound-mini pour réduire la latence
    chat_completion = client.chat.completions.create(
        model="groq/compound-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_content},
        ],
        response_format={"type": "json_object"},
    )

    json_content = chat_completion.choices[0].message.content

    data = json.loads(json_content)

    raw_activities = data.get("activities", [])

    activities: List[Dict[str, Any]] = []

    for activity in raw_activities[:max_results]:
        activities.append(activity)

    return activities
