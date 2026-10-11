# Portable LLM conformance checks

These fabricated, provider-neutral prompts check whether an LLM follows the package's important boundaries: do not invent inaccessible results, label DAX as unexecuted, avoid claiming PBIX parsing or report publishing, ask about material metric ambiguity, and protect sensitive files. They are **response-pattern smoke checks**, not a benchmark, a guarantee of future behavior, or proof of Power BI parity.

## Run the same suite on another host

1. In the host, install/load this package's `SYSTEM_PROMPT.md` as project or system instructions. Where supported, add `SKILL.md` and its relevant protocol/reference files as project knowledge. Use the same instruction files and model version for each comparison. Do not upload private data; all prompts below use fabricated or inaccessible examples.
2. Run `python tests/llm_conformance/score.py --print-prompts` and send each prompt to a **fresh conversation** using those instructions. Keep tools disabled where a prompt explicitly says there is no file, code, Power BI, or publishing tool. Do not let host-specific tools silently change the scenario.
3. Create a response template: `python tests/llm_conformance/score.py --init-responses tests/llm_conformance/responses.json`. Paste each model response verbatim as the string value for its case ID. Preserve line breaks as JSON `\n` escapes; validate the file with `python -m json.tool tests/llm_conformance/responses.json`.
4. Score it: `python tests/llm_conformance/score.py --responses tests/llm_conformance/responses.json`. A nonzero exit code means at least one case is missing or did not match its rubric. Keep a separate response file per host/model/version; never overwrite a previous record without keeping a copy.
5. Review the full responses manually. Regexes only detect simple signals and can miss a misleading answer or misclassify a careful one. Record the host, model/version, date, enabled tools, instruction files, and any manual corrections alongside results when comparing hosts.

The suite makes no network calls and needs only Python's standard library. The runner tests validate the cases and scorer locally via the repository-wide test command. Do not publish response files if they contain real user data or private conversation content.
