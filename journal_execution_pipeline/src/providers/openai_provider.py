from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib import error, request

from .base import Provider


def _extract_text(payload: dict[str, Any]) -> str:
    if payload.get("output_text"):
        return str(payload["output_text"])

    chunks: list[str] = []
    for item in payload.get("output", []) or []:
        for content in item.get("content", []) or []:
            text = content.get("text")
            if text:
                chunks.append(text)
    return "".join(chunks)


@dataclass
class OpenAIProvider(Provider):
    model: str
    instructions: str
    max_output_tokens: int = 512
    temperature: float | None = None
    top_p: float | None = None
    timeout_seconds: int = 120
    reasoning_effort: str | None = None
    api_key: str | None = None
    last_usage: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        self.api_key = self.api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not set.")

    def generate(self, prompt: str) -> str:
        body: dict[str, Any] = {
            "model": self.model,
            "input": prompt,
            "instructions": self.instructions,
            "max_output_tokens": self.max_output_tokens,
        }

        if self.temperature is not None:
            body["temperature"] = self.temperature
        if self.top_p is not None:
            body["top_p"] = self.top_p
        if self.reasoning_effort:
            body["reasoning"] = {"effort": self.reasoning_effort}

        req = request.Request(
            "https://api.openai.com/v1/responses",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenAI request failed: {detail}") from exc

        self.last_usage = payload.get("usage") or {}
        return _extract_text(payload).strip()
