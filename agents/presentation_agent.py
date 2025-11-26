from typing import Dict, Any, List
from pathlib import Path
import json

from groq import Groq

from config import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)

BASE_DIR = Path(__file__).resolve().parent.parent

PROMPT_FILE_PATH = BASE_DIR / "prompts" / "prompt.txt"
CONTEXT_FILE_PATH = BASE_DIR / "prompts" / "context.txt"
PRESENTATION_INSTRUCTIONS_FILE_PATH = (
    BASE_DIR / "prompts" / "presentation_instructions.txt"
)


def load_text_file(file_path: Path) -> str:
    
    return file_path.read_text(encoding="utf-8")


def build_system_message_for_presentation() -> str:
    
    base_prompt = load_text_file(PROMPT_FILE_PATH)
    base_context = load_text_file(CONTEXT_FILE_PATH)
    presentation_instructions = load_text_file(PRESENTATION_INSTRUCTIONS_FILE_PATH)

    full_system_message = (
        base_prompt
        + "\n\n"
        + base_context
        + "\n\n"
        + presentation_instructions
    )

    return full_system_message


def present_scenarios_to_user(
    constraints: Dict[str, Any],
    budget_allocation: Dict[str, int],
    scenarios: List[Dict[str, Any]],
) -> str:
    
    system_message = build_system_message_for_presentation()

    payload = {
        "constraints": constraints,
        "budget_allocation": budget_allocation,
        "scenarios": scenarios,
    }

    user_content = (
        "Voici les données JSON des scénarios à présenter à l'utilisateur :\n\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
    )

    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_content},
        ],
    )

    assistant_message = chat_completion.choices[0].message.content

    return assistant_message
