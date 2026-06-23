from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib import error, request

from .base import Provider


@dataclass
class OllamaProvider(Provider):
    model: str
    instructions: str
    base_url: str = "http://localhost:11434"
    max_output_tokens: int = 512
    temperature: float | None = None
    top_p: float | None = None
    timeout_seconds: int = 120

    def generate(self, prompt: str) -> str:
        options: dict[str, Any] = {
            "num_predict": self.max_output_tokens,
        }
        if self.temperature is not None:
            options["temperature"] = self.temperature
        if self.top_p is not None:
            options["top_p"] = self.top_p

        body = {
            "model": self.model,
            "prompt": f"{self.instructions}\n\n{prompt}",
            "stream": False,
            "options": options,
        }

        req = request.Request(
            f"{self.base_url.rstrip('/')}/api/generate",
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Ollama request failed: {detail}") from exc

        return str(payload.get("response", "")).strip()
