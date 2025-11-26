from groq import Groq
from pathlib import Path
from typing import Dict, Any
import json

from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

BASE_DIR = Path(__file__).resolve().parent.parent

PROMPT_FILE_PATH = BASE_DIR / "prompts" / "prompt.txt"
CONTEXT_FILE_PATH = BASE_DIR / "prompts" / "context.txt"
ANALYSIS_INSTRUCTIONS_FILE_PATH = BASE_DIR / "prompts" / "analysis_instructions.txt"


def load_text_file(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8")


def build_system_message_for_analysis() -> str:
   
    base_prompt = load_text_file(PROMPT_FILE_PATH)
    base_context = load_text_file(CONTEXT_FILE_PATH)
    analysis_instructions = load_text_file(ANALYSIS_INSTRUCTIONS_FILE_PATH)

    full_system_message = (
        base_prompt
        + "\n\n"
        + base_context
        + "\n\n"
        + analysis_instructions
    )

    return full_system_message



def analyze_user_request(user_message: str) -> Dict[str, Any]:
    
    system_message = build_system_message_for_analysis()

    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        response_format={"type": "json_object"},
    )

    json_content = chat_completion.choices[0].message.content

    constraints: Dict[str, Any] = json.loads(json_content)

    return constraints
