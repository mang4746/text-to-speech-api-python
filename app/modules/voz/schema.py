
# Modelos Pydantic

from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        description="Texto a convertir en voz",
        min_length=1,
        max_length=2000,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "Hola, ¿cómo estás?"
                }
            ]
        }
    }
