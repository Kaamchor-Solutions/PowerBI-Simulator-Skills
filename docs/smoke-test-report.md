# 360-Degree Smoke-Test Report

**Date:** 2026-10-12  
**Target:** exact public-release source tree at `/workspace/powerbi-simulator-skills`  
**Environment:** Ubuntu 24.04; Python 3.12.3; pytest 9.1.1; openpyxl 3.1.5

## Results

| Area | Status | What was exercised |
|---|---|---|
| LLM skill and fallback prompt | **PASS — static review** | Reviewed [`SKILL.md`](../SKILL.md), [`SYSTEM_PROMPT.md`](../SYSTEM_PROMPT.md), provider-neutral installation/use guidance, all task protocols, and privacy/security notes. Scope, data-access, DAX/M, report-rendering, and Power BI-parity boundaries are stated consistently. This is not a live model test. |
| Helper and report-builder CLIs | **PASS** | Compiled implementation/tests; ran `--help` for analyzer, report builder, scorer, and archive builder. Ran every one of the five example requests: inventory, relationship audit, category aggregate, West-region aggregate, and report generation. Checked JSON and Markdown outputs, file output, clean failure exit behavior, and an existing-directory output target (exit 2, concise error, no traceback). |
| Examples and independent reconciliation | **PASS** | Recomputed results directly from fabricated CSV source text with `Decimal`: total Net Sales **1705**; category totals Accessories **635**, Computers **595**, Software **475**; region totals West **720**, East **335**, South **100**, North **550**. All nine demo files had unchanged SHA-256 hashes after runs. Generated report exactly matches `docs/sample-output.md`. |
| Input formats and aggregates | **PASS** | CSV examples; `.tsv` and `.tab` inventory; named-sheet `.xlsx`; all documented aggregate operations; `eq`, `neq`, and `in` filters; blank measure handling; direct dimension filtering; grouped totals; boolean/numeric mismatch rejection. Corrupt `.xlsx` returns a concise request error through both CLIs. |
| JSON and precision | **PASS** | Strict JSON rejection of non-standard constants; decimal-token preservation through analyzer and report builder; 5,000-digit integer input/output; extreme-exponent clean error; exact add/subtract/multiply/sums beyond the default Decimal context; ambient precision/trap independence; bounded 50-significant-digit division; 100,000-digit safety cap; exact JSON number-token round-trip. |
| Errors and edge cases | **PASS** | Malformed JSON; missing file; unsupported extension; duplicate headers; ragged CSV row; division by zero; invalid relationship audit; unknown filter; boolean supplied to numeric filter/measure; report-builder partial failure; unwritable CLI output target. Errors are explicit and do not leak Python tracebacks in the exercised cases. |
| Safety, privacy, and overwrite boundaries | **PASS** | Static AST audit found no HTTP/socket/request imports in helper scripts. Tested output/request anti-overwrite protections and scorer response-template no-overwrite behavior. Confirmed demo sources were not modified. Synthetic/fabricated data only; no model API calls or data uploads were made. |
| Documentation and links | **PASS** | All repository JSON files parse; all **27 relative Markdown links and anchors** resolve; generated report matches the documented sample; methods/runtime/changelog text reflects precision and error behavior. External URL reachability was not checked. |
| Automated suites | **PASS** | `python -m pytest -v`: **47 passed, 40 subtests passed**. `python -m unittest discover -s tests -v`: **47 passed**. Python compilation and each CLI help surface passed. Regression tests exercise **29** adversarial response fixtures, including all **16** exact independent-review probes and related numeric-result variants, plus **11** safe-caveat controls. The scorer CLI accepts **7/7** curated safe strings and rejects **7/7** reviewer-style adversarial strings. |
| Git/release boundary | **PASS — release scope approved** | The user approved public MIT publication to Kaamchor-Solutions/PowerBI-Simulator-Skills; the connected GitHub account is active. Preflight found no resolvable target repository, so no existing contents were in scope to overwrite. This report records local pre-push checks; the final publication URL and commit SHA are reported in task delivery. CI declares Python 3.10–3.13, but only Python 3.12.3 was run locally. |
| Archive/extraction/reproducibility | **PASS** | `python scripts/build_archive.py --verify-reproducible` built the 47-file source ZIP twice with identical bytes on the current Python/zlib runtime. Integrity, safe paths, and byte-for-byte comparison against all 47 eligible source files passed; the extracted archive was an exact match and passed pytest and unittest. On the source tree, all four helper/scorer/archive `--help` surfaces and all five demo requests passed, and generated output matched `docs/sample-output.md`. The final ZIP SHA-256 is reported separately in task delivery. Cross-Python/zlib compressed bytes are not promised identical. |
| Live provider/model conformance | **NOT RUN** | No live model/provider was evaluated. Offline synthetic prompts and adversarial scorer tests are lexical/pattern smoke checks only—not semantic validation, a benchmark, or evidence that any LLM passed. |

## Remaining limits

- No Python 3.10/3.11/3.13, Windows, macOS, or live GitHub Actions run was available in this environment.
- The helper remains a constrained simulation; it does not execute general DAX or Power Query M, parse `.pbix`/`.pbip`, render native Power BI visuals, or establish Microsoft Power BI parity.
- Exact add/subtract/multiply/sum operations are bounded at 100,000 digits; division and means are rounded to 50 significant digits. Excel formulas are read from cached values, not recalculated.
- The conformance scorer checks text patterns only and cannot establish semantic consistency. Any host/model evaluation needs real responses and manual review of full outputs.

## Independent quality rating

The final independent read-only review scored this package **9.0/10**; the requested 9/10 threshold was met and judged defensible. It rechecked the quoted-currency and approximate compact-number probes, nearby variants, safe controls, and the canonical archive. Residual limitation: no live model/provider was evaluated, and the response scorer remains lexical rather than semantic.
