from typing import List, Dict, Any
from pathlib import Path
import json

from groq import Groq

from config import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)

BASE_DIR = Path(__file__).resolve().parent.parent

PROMPT_FILE_PATH = BASE_DIR / "prompts" / "prompt.txt"
CONTEXT_FILE_PATH = BASE_DIR / "prompts" / "context.txt"
LODGING_INSTRUCTIONS_FILE_PATH = (
    BASE_DIR / "prompts" / "lodging_web_instructions.txt"
)


def load_text_file(file_path: Path) -> str:
    
    return file_path.read_text(encoding="utf-8")


def build_system_message_for_lodging() -> str:
   
    base_prompt = load_text_file(PROMPT_FILE_PATH)
    base_context = load_text_file(CONTEXT_FILE_PATH)
    lodging_instructions = load_text_file(LODGING_INSTRUCTIONS_FILE_PATH)

    full_system_message = (
        base_prompt
        + "\n\n"
        + base_context
        + "\n\n"
        + lodging_instructions
    )

    return full_system_message


def suggest_lodgings_for_activities(
    activities: List[Dict[str, Any]],
    budget_allocation: Dict[str, int],
    max_results_per_activity: int = 2,
) -> List[Dict[str, Any]]:
   
    if not activities:
        return []

    system_message = build_system_message_for_lodging()

    max_lodging_budget = budget_allocation.get("max_lodging", 0)

    context_payload = {
        "activities": activities,
        "budget_allocation": budget_allocation,
        "max_lodging_budget": max_lodging_budget,
        "max_results_per_activity": max_results_per_activity,
    }

    user_content = (
        "Voici les données JSON du contexte (activités, budget logement) "
        "pour proposer des logements adaptés :\n\n"
        + json.dumps(context_payload, ensure_ascii=False, indent=2)
    )

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

    raw_lodgings = data.get("lodgings", [])

    lodgings: List[Dict[str, Any]] = []

    for lodging in raw_lodgings:
        nights = lodging.get("nights", 1)
        price_per_night = lodging.get("price_per_night", 0)
        total_price = lodging.get("total_price", price_per_night * nights)

        lodging_option: Dict[str, Any] = {
            "for_activity": lodging.get("for_activity"),
            "lodging_name": lodging.get("lodging_name"),
            "platform": lodging.get("platform"),
            "city": lodging.get("city"),
            "price_per_night": price_per_night,
            "nights": nights,
            "total_price": total_price,
            "rating": lodging.get("rating", 0),
            # on garde aussi l'URL si on veut l'utiliser plus tard dans l'UI
            "url": lodging.get("url"),
        }

        lodgings.append(lodging_option)

    return lodgings
