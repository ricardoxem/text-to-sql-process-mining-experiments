from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_ROOT = ROOT / "journal_execution_pipeline" / "evaluation_outputs"
TOOL_ROOT = ROOT / "journal_execution_pipeline" / "evaluation_tools"


LANGUAGE_CONFIG = {
    "en": {
        "tool_dir": TOOL_ROOT / "test-suite-sql-eval-en",
        "gold": ROOT / "dataset" / "gold_en.txt",
    },
    "pt": {
        "tool_dir": TOOL_ROOT / "test-suite-sql-eval-pt",
        "gold": ROOT / "dataset" / "gold_pt.txt",
    },
}


def resolve_path(path_value: str | None, default: Path | None = None) -> Path:
    if path_value is None:
        if default is None:
            raise ValueError("Path value is required.")
        return default
    path = Path(path_value)
    if path.is_absolute():
        return path
    return (ROOT / path).resolve()


def copy_if_exists(source: Path, target: Path) -> None:
    if source.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def ensure_nltk_resources() -> None:
    try:
        import nltk
        from nltk.data import find
    except ImportError as exc:
        raise RuntimeError(
            "The evaluator requires nltk. Install dependencies with: "
            "pip install -r journal_execution_pipeline/requirements.txt"
        ) from exc

    for resource in ("punkt", "punkt_tab"):
        try:
            find(f"tokenizers/{resource}")
        except LookupError:
            nltk.download(resource, quiet=True)


def run_evaluation(
    language: str,
    predictions: Path,
    gold: Path,
    output_dir: Path,
    etype: str,
    keep_distinct: bool,
    plug_value: bool,
    limit: int | None,
) -> None:
    cfg = LANGUAGE_CONFIG[language]
    tool_dir = cfg["tool_dir"]
    if not tool_dir.exists():
        raise FileNotFoundError(f"Evaluation tool directory not found: {tool_dir}")
    if not predictions.exists():
        raise FileNotFoundError(f"Predictions file not found: {predictions}")
    if not gold.exists():
        raise FileNotFoundError(f"Gold file not found: {gold}")

    ensure_nltk_resources()

    output_dir.mkdir(parents=True, exist_ok=True)
    runtime_tool_dir = output_dir / "_runtime_tool"
    if runtime_tool_dir.exists():
        shutil.rmtree(runtime_tool_dir)
    shutil.copytree(tool_dir, runtime_tool_dir)

    work_gold = output_dir / "gold.txt"
    work_pred = output_dir / "predict.txt"

    gold_lines = gold.read_text(encoding="utf-8").splitlines()
    pred_lines = predictions.read_text(encoding="utf-8").splitlines()
    if limit is not None:
        gold_lines = gold_lines[:limit]
        pred_lines = pred_lines[:limit]

    if len(gold_lines) != len(pred_lines):
        raise ValueError(
            f"Gold and prediction files must have the same number of lines. "
            f"Got gold={len(gold_lines)} and predictions={len(pred_lines)}."
        )

    work_gold.write_text("\n".join(gold_lines) + "\n", encoding="utf-8")
    work_pred.write_text("\n".join(pred_lines) + "\n", encoding="utf-8")

    cmd = [
        sys.executable,
        "evaluation.py",
        "--gold",
        str(work_gold),
        "--pred",
        str(work_pred),
        "--db",
        "database",
        "--etype",
        etype,
    ]
    if etype in {"all", "match"}:
        cmd.extend(["--table", "evaluation_examples/tables.json"])
    if keep_distinct:
        cmd.append("--keep_distinct")
    if plug_value:
        cmd.append("--plug_value")

    log_path = output_dir / "evaluation.log"
    env = os.environ.copy()
    with log_path.open("w", encoding="utf-8") as log:
        completed = subprocess.run(
            cmd,
            cwd=runtime_tool_dir,
            stdout=log,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
            env=env,
        )
    if completed.returncode != 0:
        raise RuntimeError(f"Evaluation failed. See log: {log_path}")

    copy_if_exists(runtime_tool_dir / "evaluation_examples" / "score.tsv", output_dir / "score.tsv")
    copy_if_exists(runtime_tool_dir / "evaluation_examples" / "score_time.tsv", output_dir / "score_time.tsv")

    print(f"Evaluation finished: {output_dir}")
    print(f"Log: {log_path}")
    if (output_dir / "score.tsv").exists():
        print(f"Scores: {output_dir / 'score.tsv'}")
    if (output_dir / "score_time.tsv").exists():
        print(f"Execution times: {output_dir / 'score_time.tsv'}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", choices=sorted(LANGUAGE_CONFIG), required=True)
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--gold", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--etype", choices=("exec", "match", "all"), default="exec")
    parser.add_argument("--keep-distinct", action="store_true")
    parser.add_argument("--plug-value", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    cfg = LANGUAGE_CONFIG[args.language]
    predictions = resolve_path(args.predictions)
    gold = resolve_path(args.gold, cfg["gold"])
    output_dir = resolve_path(
        args.output_dir,
        DEFAULT_OUTPUT_ROOT / f"{args.language}_{predictions.stem}_{args.etype}",
    )

    run_evaluation(
        language=args.language,
        predictions=predictions,
        gold=gold,
        output_dir=output_dir,
        etype=args.etype,
        keep_distinct=args.keep_distinct,
        plug_value=args.plug_value,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()
