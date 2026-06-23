from __future__ import annotations

import os
from dataclasses import dataclass

import google.generativeai as genai

from .base import Provider


@dataclass
class GeminiProvider(Provider):
    model: str
    instructions: str
    max_output_tokens: int = 512
    temperature: float | None = None
    top_p: float | None = None
    api_key: str | None = None

    def __post_init__(self) -> None:
        self.api_key = self.api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise RuntimeError("GOOGLE_API_KEY is not set.")
        genai.configure(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        config = {
            "max_output_tokens": self.max_output_tokens,
        }
        if self.temperature is not None:
            config["temperature"] = self.temperature
        if self.top_p is not None:
            config["top_p"] = self.top_p

        model = genai.GenerativeModel(
            model_name=self.model,
            system_instruction=self.instructions,
        )
        response = model.generate_content(
            prompt,
            generation_config=config,
        )
        text = getattr(response, "text", None)
        if text:
            return str(text).strip()
        chunks: list[str] = []
        for candidate in getattr(response, "candidates", []) or []:
            content = getattr(candidate, "content", None)
            parts = getattr(content, "parts", []) or []
            for part in parts:
                part_text = getattr(part, "text", None)
                if part_text:
                    chunks.append(str(part_text))
        return "".join(chunks).strip()
