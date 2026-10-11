# Methods and limitations

This project is an independent prompt-and-helper package for LLM-guided Power BI-style analysis. It is neither affiliated with Microsoft nor a port, emulator, or replacement for Microsoft Power BI. Its LLM instructions can guide analysis in different providers; actual file/code access and model capability depend on the host.

## Bundled deterministic helper

| Area | Implemented subset | Not implemented |
|---|---|---|
| Input | CSV, TSV/TAB, `.xlsx` (cached cell values) | `.xls`, `.pbix`, `.pbip`, database/Power BI connectors |
| Inventory | Rows/columns, duplicates, inferred types, missing/distinct counts, small samples | Full schema discovery, lineage, profiling at enterprise scale |
| Model check | Explicit direct one-to-many key uniqueness and foreign-key orphans | Model-file parsing, relationship engine, ambiguous paths, RLS, filter propagation |
| Aggregates | Count rows/nonblank, distinct count, sum/mean/min/max, arithmetic `sum_expression`; direct dimension grouping and simple explicit eq/neq/in filters | DAX functions, context transition, time intelligence, ranking, percent-of-total, many-to-many semantics, calculation groups |
| Reporting | Deterministic Markdown inventory/audit/aggregate report | Native Power BI canvas/visuals, `.pbix` export, publish, refresh, workspace/tenant APIs |
| Transformation | Model and M drafting by LLM | Execution of Power Query M, query folding, refresh credentials/gateway |

The expression parser accepts only column names, finite numeric constants, parentheses, unary signs, and `+`, `-`, `*`, `/`. It is not Python `eval` and rejects arbitrary code. A numeric expression with a blank operand skips that row; division by zero is an error. The helper uses decimal arithmetic internally and emits fractional Decimal results as exact JSON number tokens (not floats or strings). Downstream readers should parse decimals as decimal values rather than binary floats when exact precision matters; division remains subject to finite Decimal precision.

The helper is intended for small, transparent checks—not large-scale or regulated production calculations. It loads data in memory. Excel formulas are not recalculated; only cached values are available. Type inference is heuristic and CSV data is initially text. Dates, locale, currency, leading-zero identifiers, blank behavior, timezone, duplicates, and grain still require review.

## LLM boundary

A chat model with only `SYSTEM_PROMPT.md` can explain, draft, and plan; it cannot automatically read local files or run this helper. If code execution is available, it must actually run the helper against the supplied data and inspect the result status before reporting numbers. DAX and M examples are proposals unless tested in a real compatible Power BI environment. A text wireframe is not a rendered report.

## Validation and privacy

The demo tests cover the helper and hand-checkable fixture totals; they do not prove Microsoft Power BI parity or verify DAX. Before business use, reconcile against an independent source calculation and validate formulas, relationships, blanks, filters, time rules, units, rounding, and report behavior in Power BI. The helper does not transmit source data, but samples/results may still be sensitive. Review outputs and follow the host model's data-handling rules.
