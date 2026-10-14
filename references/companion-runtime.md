# Companion runtime and JSON contract

The optional Python helper makes only a small, deterministic subset of a BI workflow reproducible. It uses Python's standard library for CSV/TSV and `openpyxl` (installed from `scripts/requirements.txt`) for `.xlsx` workbooks. It does not parse `.xls`, `.pbix`, or `.pbip`. Excel is read with cached cell values (`data_only=True`); formulas are not recalculated. Run commands from the repository root because relative source paths are resolved from the current working directory.

```bash
python scripts/analyze.py --config examples/demo_sales/inventory-request.json
python scripts/analyze.py --config examples/demo_sales/model-audit-request.json
python scripts/analyze.py --config examples/demo_sales/net-sales-by-category-request.json --format markdown
python scripts/bi_report.py --config examples/demo_sales/report-request.json --output report.md
python scripts/bi_report.py --config examples/demo_sales/report-request.json --output report-strict.md --fail-on-invalid
```

## Request actions

Top-level keys are action-specific: `inventory` accepts `action`, `tables`, `include_samples`, and `sample_limit`; `model_audit` also accepts `relationships`; `aggregate` also accepts `relationships`, `fact_table`, `group_by`, `filters`, and `measures`. The two sample-policy keys are accepted by all actions. Unknown top-level keys are rejected before source files are opened, with a spelling suggestion when available. This intentionally changes the previous behavior that silently ignored extra keys; for example, `filter` is rejected with a suggestion to use `filters`.

JSON request objects must have unique member names at every nesting level. Duplicate keys are rejected instead of silently keeping the last value; this applies to analyzer requests, nested table/analysis objects, and report requests. Requests that previously relied on last-key-wins parsing must be corrected.

An `inventory` request has `action` and a non-empty `tables` map. Each table has a `file` path and, for `.xlsx`, an optional `sheet` name or zero-based index. The helper returns rows/columns, duplicate rows, inferred field types, and missing/distinct counts.

Raw sample arrays are suppressed by default. Set `include_samples: true` to include inventory `sample_values` and model-audit duplicate/orphan key examples; `sample_limit` controls their maximum count from 0 to 5 (default 5). This intentionally changes the previous behavior, where inventory samples were included automatically. Counts are unchanged when samples are suppressed. This option controls only those explicit sample fields; it is not general PII detection, per-column suppression, or sanitization of arbitrary values in errors or other result fields. Review outputs before sharing.

A `model_audit` request adds `relationships`, each declared as `{ "one_table": "Customers", "one_column": "CustomerID", "many_table": "Orders", "many_column": "CustomerID" }`. The audit checks null and duplicate keys on the declared one side and orphan nonblank foreign keys on the many side. It does not validate every Power BI relationship property or implement filter propagation. A failed integrity check returns `valid: false`; direct-audit Markdown preserves per-relationship null, duplicate, and orphan counts. Raw examples remain omitted unless explicitly enabled under the sample policy above.

An `aggregate` request also supplies `fact_table`, optional `group_by`, optional `filters`, and a non-empty `measures` list. Group/filter fields use `{ "table": "Products", "column": "Category" }`. A dimension field must belong to exactly one directly declared relationship to the fact table. Multi-hop and competing relationship paths are not implemented.

Aggregate collection types and nested field shapes are checked before source files are opened. `group_by`, `filters`, and `measures` must be lists; field references require non-empty string `table` and `column` values. Each `filters[i].op` must be the string `eq`, `neq`, or `in` (omitting it defaults to `eq`); each `measures[i].op` must be a supported operation string. Every filter requires a `value` field: explicit JSON `null` remains an explicit blank filter and is distinct from omitting `value`. An `in` filter requires a list `value`. Measure names must be non-empty and unique, and `sum_expression` requires a non-empty string expression. Malformed types, unsupported operations, and duplicate names produce a `RequestError` with an indexed field path such as `measures[0].op`, rather than an uncaught type error. Table/column existence and relationship checks still depend on loaded tables.

For handled JSON parse and request-validation failures in the analyzer CLI's default JSON mode, the JSON result retains the human-readable `error` message and also includes a stable `error_code`; field-specific validation adds `error_path`. Current codes include `invalid_type`, `invalid_value`, `missing_field`, `unsupported_value`, `unsupported_operation`, `duplicate_name`, `unknown_field`, `duplicate_json_key`, `invalid_json_constant`, `invalid_json`, `input_error`, `resource_limit`, and the fallback `invalid_request`. The JSON result is written to stdout and the human diagnostic to stderr.

Supported measure examples:

```json
{"name":"Net Sales","op":"sum_expression","expression":"Quantity * UnitPrice * (1 - DiscountPct)"}
{"name":"Order Count","op":"distinct_count","table":"Orders","column":"OrderID"}
{"name":"Rows","op":"count_rows"}
{"name":"Known Amounts","op":"count_nonblank","table":"Orders","column":"Amount"}
```

Other supported `op` values are `sum`, `mean`, `min`, and `max`. The expression parser accepts only fact-column identifiers, finite numeric constants, parentheses, unary `+`/`-`, and `+ - * /`. It rejects functions, attributes, subscripts, imports, and arbitrary code. Expressions are limited to 4096 characters, 1024 AST nodes, and AST depth 64; these fixed helper limits fail with the stable `resource_limit` code and are not request-adjustable. A blank operand skips that row for `sum_expression`; division by zero is an error. Boolean values are not treated as numeric 0/1 for numeric filters or measures.

Simple explicit filters use `op` `eq`, `neq`, or `in`, for example `{ "table":"Customers", "column":"Region", "op":"eq", "value":"West" }`. A numeric filter is parsed using the detected numeric type; text values should match source values.

## Output and status

`bi_report.py` is tolerant by default: it keeps successful analyses and labels the report `COMPLETE`, `PARTIAL`, `FAILED`, or `EMPTY` with succeeded/invalid/error/skipped counts. Therefore, a default-mode exit code of `0` means the report was written, not that every analysis succeeded. With `--fail-on-invalid`, the report is still written for inspection, but the command exits `2` unless the report is non-empty and every analysis succeeds. Report-configuration, unsafe-output, and report-write errors exit `2` in either mode; individual analysis errors are counted and force `2` only in strict mode. In-process callers can use `build_report_result()` for `(markdown, summary)`; `build_report()` remains a Markdown-string compatibility wrapper.

`--format json` is the stable machine-oriented result; `--format markdown` formats the same result for review. The top-level `valid` and `status` must be checked before interpretation. A failed request—including an unreadable or malformed workbook—exits nonzero and emits a concise error; a model-integrity failure returns an explicit invalid result and no aggregate. XLSX packages are rejected with `resource_limit` when their declared cumulative uncompressed ZIP-member size exceeds the fixed 256 MiB cap, checked before `openpyxl` loads the workbook. `rows_input`, `rows_used`, `rows_filtered_out`, `measure_audit`, group rows, and totals are the provenance needed to describe the calculation.

JSON request integer and fractional tokens are parsed without a binary-float conversion; integers too long for Python's configured `int` string limit are kept as `Decimal`. A numeric token longer than 100,000 characters, a decimal token outside the supported Decimal exponent range, and non-standard constants such as `NaN` are rejected with a request error. Finite additions, subtractions, multiplications, and sums are exact up to the documented 100,000-digit operation bound. Division and means use 50 significant digits with `ROUND_HALF_EVEN` (round to nearest, ties to even), independent of the caller's active Decimal rounding mode. Aggregate results are emitted as exact JSON number tokens rather than quoted strings or binary floats. Consumers that need to retain all digits should parse both integer and fractional tokens as decimal values (for example, in Python use `json.loads(text, parse_int=Decimal, parse_float=Decimal)`); consumers that convert JSON numbers to IEEE-754 binary floats may round them. `run_request()` returns fractional Decimal values to Python callers.

The helper does not retain, upload, or transmit the source data. Inventory samples and derived values can still be sensitive; review them before sharing. It is an independent helper, not Microsoft software or a compatible Power BI engine. It does not execute DAX or M, create native visuals, implement DAX blank/context semantics, read model metadata, or promise performance/parity. These limitations are part of the result contract, not optional caveats.
