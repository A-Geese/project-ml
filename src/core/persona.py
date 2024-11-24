"""
Define persona creation here
"""

from .constants import SYSTEM_PROMPT, USER_PROMPT
from .traits import Characteristics
from openai import OpenAI
import instructor


def get_persona_traits(persona_prompt: str) -> dict:
    client = instructor.from_openai(
        OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        ),
        mode=instructor.Mode.JSON,
    )

    persona_traits = {}
    for field_name, field in Characteristics.model_fields.items():
        while True:
            try:
                response = client.chat.completions.create(
                    model="llama3.2",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {
                            "role": "user",
                            "content": USER_PROMPT.format(persona=persona_prompt),
                        },
                    ],
                    response_model=field.annotation,
                )
            except Exception:
                print(f"Retrying structured outputs on: {field.annotation}")
                continue

            persona_traits[field_name] = response.model_dump()
            break

    return persona_traits
