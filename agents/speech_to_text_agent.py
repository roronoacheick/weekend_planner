from typing import BinaryIO
from groq import Groq

from config import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)


def transcribe_audio_file(
    file_obj: BinaryIO,
    filename: str,
    language: str = "fr",
) -> str:
   
    
    file_bytes = file_obj.read()

    transcription = client.audio.transcriptions.create(
        file=(filename, file_bytes),
        model="whisper-large-v3-turbo",  
        language=language,              
        response_format="json",          
        temperature=0.0,
    )

    return transcription.text
