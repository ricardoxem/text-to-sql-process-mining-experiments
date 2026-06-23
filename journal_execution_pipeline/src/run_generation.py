from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:  # Allow both `python -m ...` and direct script execution.
    from .io_utils import append_line, load_json, write_json
    from .normalize_sql import normalize_sql_output
except ImportError:  # pragma: no cover - fallback for direct script execution.
    from io_utils import append_line, load_json, write_json
    from normalize_sql import normalize_sql_output


ROOT = Path(__file__).resolve().parents[2]


def resolve_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return (ROOT / path).resolve()


def load_env_file(path: Path = ROOT / ".env") -> None:
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def build_provider(run: dict[str, Any], request_cfg: dict[str, Any]):
    provider = run["provider"].lower()
    common = {
        "model": run["model"],
        "instructions": request_cfg["instructions"],
        "max_output_tokens": int(request_cfg.get("max_output_tokens", 512)),
        "temperature": request_cfg.get("temperature"),
        "top_p": request_cfg.get("top_p"),
        "timeout_seconds": int(request_cfg.get("timeout_seconds", 120)),
    }

    if provider == "openai":
        from .providers.openai_provider import OpenAIProvider

        reasoning_effort = run.get("reasoning_effort")
        if reasoning_effort:
            common["reasoning_effort"] = reasoning_effort
        api_key = run.get("api_key")
        if api_key:
            common["api_key"] = api_key
        return OpenAIProvider(**common)

    if provider == "gemini":
        from .providers.gemini_provider import GeminiProvider

        api_key = run.get("api_key")
        if api_key:
            common["api_key"] = api_key
        return GeminiProvider(**common)

    if provider == "ollama":
        from .providers.ollama_provider import OllamaProvider

        ollama_cfg = run.get("ollama", {})
        return OllamaProvider(
            base_url=ollama_cfg.get("base_url", "http://localhost:11434"),
            **common,
        )

    raise ValueError(f"Unknown provider: {provider}")


def existing_question_ids(output_path: Path) -> set[str]:
    responses_path = output_path / "responses.jsonl"
    if not responses_path.exists():
        return set()

    seen: set[str] = set()
    with responses_path.open(encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue
            seen.add(json.loads(line)["id"])
    return seen


def empty_usage() -> dict[str, float]:
    return {
        "input_tokens": 0.0,
        "output_tokens": 0.0,
        "reasoning_tokens": 0.0,
        "estimated_cost_usd": 0.0,
    }


def existing_usage(output_path: Path) -> dict[str, float]:
    responses_path = output_path / "responses.jsonl"
    totals = empty_usage()
    if not responses_path.exists():
        return totals

    with responses_path.open(encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue
            payload = json.loads(line)
            usage = payload.get("usage") or {}
            for key in totals:
                totals[key] += float(usage.get(key, 0) or 0)
    return totals


def usage_with_cost(provider: Any, run: dict[str, Any]) -> dict[str, float]:
    raw_usage = getattr(provider, "last_usage", None) or {}
    output_details = raw_usage.get("output_tokens_details") or {}
    input_tokens = int(raw_usage.get("input_tokens", 0) or 0)
    output_tokens = int(raw_usage.get("output_tokens", 0) or 0)
    reasoning_tokens = int(output_details.get("reasoning_tokens", 0) or 0)

    pricing = run.get("pricing_per_million_tokens") or {}
    input_price = float(pricing.get("input", 0) or 0)
    output_price = float(pricing.get("output", 0) or 0)
    estimated_cost = (
        input_tokens * input_price + output_tokens * output_price
    ) / 1_000_000

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "reasoning_tokens": reasoning_tokens,
        "estimated_cost_usd": estimated_cost,
    }


def select_runs(
    runs: list[dict[str, Any]],
    providers: list[str] | None,
    run_names: list[str] | None,
    models: list[str] | None,
) -> list[dict[str, Any]]:
    selected = []
    provider_set = {item.lower() for item in providers or []}
    run_name_set = set(run_names or [])
    model_set = set(models or [])

    for run in runs:
        if provider_set and run["provider"].lower() not in provider_set:
            continue
        if run_name_set and run["name"] not in run_name_set:
            continue
        if model_set and run["model"] not in model_set:
            continue
        selected.append(run)

    return selected


def run_once(run: dict[str, Any], config: dict[str, Any], limit: int | None, resume: bool) -> None:
    questions_path = resolve_path(run["questions_path"])
    payload = load_json(questions_path)
    questions = payload.get("questions", [])
    if limit is not None:
        questions = questions[:limit]

    output_root = resolve_path(config["output_root"])
    output_dir = output_root / run["name"]
    output_dir.mkdir(parents=True, exist_ok=True)

    model_name = run["model"].replace("/", "_")
    predictions_path = output_dir / f"RESULTS_MODEL-{model_name}.txt"
    responses_path = output_dir / "responses.jsonl"
    metadata_path = output_dir / "run_metadata.json"

    if not resume:
        predictions_path.unlink(missing_ok=True)
        responses_path.unlink(missing_ok=True)
        metadata_path.unlink(missing_ok=True)

    provider = build_provider(run, config["request"])
    completed = existing_question_ids(output_dir) if resume else set()
    totals = existing_usage(output_dir) if resume else empty_usage()

    metadata = {
        "run": run,
        "questions_path": str(questions_path),
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "request": config["request"],
        "total_questions": len(questions),
    }
    write_json(metadata_path, metadata)

    max_retries = int(config["request"].get("max_retries", 3))
    sleep_seconds = float(config["request"].get("sleep_between_requests_seconds", 0.0))

    for idx, question in enumerate(questions, start=1):
        qid = question["id"]
        if qid in completed:
            continue

        prompt = question["prompt"]
        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                raw = provider.generate(prompt)
                sql = normalize_sql_output(raw)
                usage = usage_with_cost(provider, run)
                for key in totals:
                    totals[key] += usage[key]
                append_line(predictions_path, sql)
                append_line(
                    responses_path,
                    json.dumps(
                        {
                            "id": qid,
                            "index": idx,
                            "provider": run["provider"],
                            "model": run["model"],
                            "language": run.get("language"),
                            "prompt": prompt,
                            "raw_output": raw,
                            "normalized_sql": sql,
                            "usage": usage,
                            "created_at_utc": datetime.now(timezone.utc).isoformat(),
                        },
                        ensure_ascii=False,
                    ),
                )
                break
            except Exception as exc:  # runtime API/network handling
                last_error = exc
                if attempt == max_retries:
                    raise
                time.sleep(min(2**attempt, 30))

        if last_error is None and sleep_seconds > 0:
            time.sleep(sleep_seconds)

        if idx % 25 == 0:
            print(
                f"{run['name']}: {idx}/{len(questions)} "
                f"| estimated cost: US${totals['estimated_cost_usd']:.4f}",
                flush=True,
            )

    metadata["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    metadata["usage_totals"] = totals
    write_json(metadata_path, metadata)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument(
        "--provider",
        action="append",
        default=None,
        help="Run only this provider. Can be repeated, e.g. --provider ollama --provider openai.",
    )
    parser.add_argument(
        "--run-name",
        action="append",
        default=None,
        help="Run only this named configuration. Can be repeated.",
    )
    parser.add_argument(
        "--model",
        action="append",
        default=None,
        help="Run only this model name. Can be repeated.",
    )
    args = parser.parse_args()

    load_env_file()
    config = load_json(args.config)
    resume = not args.no_resume
    runs = select_runs(config.get("runs", []), args.provider, args.run_name, args.model)
    if not runs:
        raise SystemExit("No runs matched the selected filters.")

    for run in runs:
        try:
            run_once(run, config, args.limit, resume)
        except Exception as exc:
            print(f"Run failed for {run['name']}: {exc}", file=sys.stderr)
            raise


if __name__ == "__main__":
    main()
