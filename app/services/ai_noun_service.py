import json
import os

from openai import OpenAI

from pathlib import Path

from dotenv import load_dotenv

project_root = Path(__file__).resolve().parents[1]

load_dotenv(project_root / ".env")




VALID_GENDERS = ["m", "f", "n"]

def resolve_noun_with_ai(word):
    client = OpenAI(
        #os.getenv("OPENAI_API_KEY")
    )
    """
    Returns:
    {
        "status" : "found",
        "word" : str,
        "genders" : list[str]
    }

    or:

    {
        "status": "not_a_noun",
        "word": str
    }
    """
    try:
        response = client.responses.create(
            model="gpt-5.6-luna",
            input = f"""
            You are validating German nouns.
            
            Word: {word}
            
            Return JSON only.
            
            Return the Nominativ version of the noun.
            Return the singular form of the noun if exists.
            
            If the word is a German noun:
            {{
                "status": "found",
                "word": "{word}",
                "genders": ["m"]
            }}
            
            Valid genders are:
            m = masculine
            f = feminine
            n = neuter
            
            If multiple genders are valid, include all of them.
            
            If the word is not a German noun:
            {{
                "status": "not_a_noun",
                "word": "{word}"
            }}
            """
        )

        return parse_ai_noun_response(
            response.output_text
        )
    except Exception:
        return {
            "status": "ai_error"
        }



def parse_ai_noun_response(output_text):
    result = json.loads(output_text)

    if not isinstance(result, dict):
        raise ValueError("AI response must be a JSON object")

    status = result.get("status")

    if status == "found":
        word = result.get("word")
        genders = result.get("genders")

        if not isinstance(word, str) or not word:
            raise ValueError("AI response contains an invalid word")

        if not isinstance(genders, list) or len(genders) == 0:
            raise ValueError("AI response must contain a non-empty genders list")

        if not all(gender in VALID_GENDERS for gender in genders):
            raise ValueError("AI response contains an invalid gender")

        return {
            "status": "found",
            "word": word,
            "genders": list(dict.fromkeys(genders))
        }

    elif status == "not_a_noun":
        word = result.get("word")

        if not isinstance(word, str) or not word:
            raise ValueError("AI response contains an invalid word")

        return {
            "status": "not_a_noun",
            "word": word
        }

    else:
        raise ValueError("AI response contains an invalid status")






