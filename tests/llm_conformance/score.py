#!/usr/bin/env python3
"""Score recorded LLM responses against portable, regex-based conformance checks."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
DEFAULT_CASES = HERE / "cases.json"


def load_cases(path: Path = DEFAULT_CASES) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    cases = payload.get("cases") if isinstance(payload, dict) else None
    if not isinstance(cases, list) or not cases:
        raise ValueError("Cases file must contain a non-empty 'cases' list")
    ids = [case.get("id") for case in cases if isinstance(case, dict)]
    if len(ids) != len(cases) or len(ids) != len(set(ids)) or any(not item for item in ids):
        raise ValueError("Each case must be an object with a unique, non-empty id")
    for case in cases:
        if not isinstance(case.get("prompt"), str) or not isinstance(case.get("title"), str):
            raise ValueError(f"Case {case['id']!r} must include a title and prompt")
        for key in ("required", "forbidden"):
            if not isinstance(case.get(key), list) or any(not isinstance(item, str) for item in case[key]):
                raise ValueError(f"Case {case['id']!r} must have a string-list {key!r}")
        for pattern in case["required"] + case["forbidden"]:
            re.compile(pattern)
    return cases


def evaluate_case(case: dict[str, Any], response: str | None) -> tuple[str, list[str]]:
    if not isinstance(response, str) or not response.strip():
        return "MISSING", ["No non-empty response recorded"]
    problems = []
    for index, pattern in enumerate(case["required"], start=1):
        if re.search(pattern, response) is None:
            problems.append(f"Missing required behavior check {index}")
    for index, pattern in enumerate(case["forbidden"], start=1):
        if re.search(pattern, response) is not None:
            problems.append(f"Matched forbidden behavior check {index}")
    return ("PATTERN_PASS", []) if not problems else ("FAIL", problems)


def score_responses(cases: list[dict[str, Any]], responses: dict[str, Any]) -> list[tuple[str, str, list[str]]]:
    return [(case["id"], *evaluate_case(case, responses.get(case["id"]))) for case in cases]


def print_prompts(cases: list[dict[str, Any]]) -> None:
    for case in cases:
        print(f"[{case['id']}] {case['title']}\n{case['prompt']}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES, help="Case definition JSON (default: cases.json beside this script)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--print-prompts", action="store_true", help="Print all prompts for manual testing in a host")
    group.add_argument("--init-responses", type=Path, help="Create a blank response JSON file without overwriting an existing file")
    group.add_argument("--responses", type=Path, help="Score a JSON object mapping case IDs to verbatim response strings")
    args = parser.parse_args(argv)
    try:
        cases = load_cases(args.cases)
        if args.print_prompts:
            print_prompts(cases)
            return 0
        if args.init_responses:
            target = args.init_responses
            if target.exists():
                raise FileExistsError(f"Refusing to overwrite existing response file: {target}")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps({case["id"]: "" for case in cases}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"Created response template: {target}")
            return 0
        with args.responses.open("r", encoding="utf-8") as handle:
            responses = json.load(handle)
        if not isinstance(responses, dict):
            raise ValueError("Responses JSON must be an object mapping case IDs to strings")
        unknown_ids = sorted(set(responses) - {case["id"] for case in cases})
        if unknown_ids:
            raise ValueError(f"Responses contain unknown case IDs: {unknown_ids}")
        results = score_responses(cases, responses)
    except (OSError, json.JSONDecodeError, ValueError, re.error) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    for case_id, status, reasons in results:
        suffix = "" if not reasons else " — " + "; ".join(reasons)
        print(f"{status:7} {case_id}{suffix}")
    passed = sum(status == "PATTERN_PASS" for _, status, _ in results)
    print(f"\n{passed}/{len(results)} pattern checks passed. A PATTERN_PASS is not a semantic judgment or proof; manually review every full response, including passes.")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
