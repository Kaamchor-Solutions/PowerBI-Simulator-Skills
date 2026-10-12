#!/usr/bin/env python3
"""Build a concise Markdown report from multiple helper requests; no Power BI rendering."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import analyze


def build_report_result(config: dict) -> tuple[str, dict[str, int | str]]:
    """Return the Markdown report and machine-readable aggregate status."""
    if not isinstance(config, dict) or not isinstance(config.get("analyses"), list):
        raise analyze.RequestError("Report request must contain an 'analyses' list")
    title = config.get("title", "Power BI-style analysis report")
    counts = {"succeeded": 0, "invalid": 0, "errors": 0, "skipped": 0}
    lines = [f"# {title}", "", "", "", "> Deterministic helper report; not Power BI output or DAX evaluation.", ""]
    for index, item in enumerate(config["analyses"], start=1):
        if not isinstance(item, dict) or not isinstance(item.get("request"), dict):
            counts["skipped"] += 1
            lines.extend([f"## Analysis {index}", "", "**Did not run:** each analysis needs a request object; its name is optional.", ""])
            continue
        name = item.get("name") or f"Analysis {index}"
        lines.extend([f"## {name}", ""])
        try:
            result = analyze.run_request(item["request"])
        except (OSError, analyze.RequestError) as exc:
            counts["errors"] += 1
            lines.append(f"**Did not run:** {exc}")
        else:
            if result.get("valid") is True:
                counts["succeeded"] += 1
            else:
                counts["invalid"] += 1
            rendered_lines = analyze.format_markdown(result).splitlines()
            if rendered_lines and rendered_lines[0].startswith("# Power BI-style "):
                rendered_lines = rendered_lines[1:]
            while rendered_lines and not rendered_lines[0].strip():
                rendered_lines.pop(0)
            lines.append("\n".join(rendered_lines).rstrip())
        lines.append("")
    lines.extend(["## Limitations", "", "The helper computes only its documented inventory, declared-key audits, and simple aggregate operations. It does not execute DAX or Power Query M, implement Power BI filter context, render visuals, or access a Power BI tenant. Review the linked method limits before relying on results.", ""])

    if not config["analyses"]:
        status = "empty"
    elif counts["invalid"] + counts["errors"] + counts["skipped"] == 0:
        status = "complete"
    elif counts["succeeded"] > 0:
        status = "partial"
    else:
        status = "failed"
    summary: dict[str, int | str] = {"status": status, "total": len(config["analyses"]), **counts}
    lines[2] = (
        f"**REPORT STATUS: {status.upper()}** — "
        f"{counts['succeeded']} succeeded; {counts['invalid']} invalid; "
        f"{counts['errors']} errors; {counts['skipped']} skipped."
        if status != "empty"
        else "**REPORT STATUS: EMPTY** — No analyses were provided."
    )
    return "\n".join(lines).rstrip() + "\n", summary


def build_report(config: dict) -> str:
    """Compatibility wrapper returning only the rendered Markdown."""
    report, _ = build_report_result(config)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="UTF-8 JSON report request")
    parser.add_argument("--output", required=True, help="Markdown output path")
    parser.add_argument(
        "--fail-on-invalid",
        action="store_true",
        help="Exit 2 if any analysis is invalid, errors, is skipped, or the request is empty (report is still written)",
    )
    args = parser.parse_args(argv)
    config_path = Path(args.config).expanduser()
    target = Path(args.output).expanduser()
    try:
        with config_path.open("r", encoding="utf-8") as handle:
            config = analyze.load_json(handle)
        analyze.ensure_output_safe(target, config_path, config)
        report, summary = build_report_result(config)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(report, encoding="utf-8")
    except (OSError, json.JSONDecodeError, analyze.RequestError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(f"Wrote Markdown report: {target}")
    if args.fail_on_invalid and summary["status"] != "complete":
        print("Error: report is not complete; inspect the report status and per-analysis results.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
