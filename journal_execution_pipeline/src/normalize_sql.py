from __future__ import annotations

import re


_CODE_FENCE_RE = re.compile(r"```(?:sql|sqlite)?\s*(.*?)```", re.IGNORECASE | re.DOTALL)


def strip_code_fence(text: str) -> str:
    match = _CODE_FENCE_RE.search(text)
    if match:
        return match.group(1).strip()
    return text.strip()


def normalize_sql_output(text: str) -> str:
    sql = strip_code_fence(text)
    sql = sql.replace("\r\n", "\n").replace("\r", "\n").strip()
    sql = "\n".join(line.strip() for line in sql.splitlines() if line.strip())

    if not sql:
        return ""

    select_pos = sql.upper().find("SELECT")
    with_pos = sql.upper().find("WITH")
    candidates = [pos for pos in [select_pos, with_pos] if pos >= 0]
    if candidates:
        sql = sql[min(candidates):]
    elif not sql.upper().startswith(("SELECT", "WITH")):
        sql = "SELECT " + sql

    sql = " ".join(sql.split())
    if sql and not sql.endswith(";"):
        sql += ";"
    return sql
