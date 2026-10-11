# Companion runtime and JSON contract

The optional Python helper makes only a small, deterministic subset of a BI workflow reproducible. It uses Python's standard library for CSV/TSV and `openpyxl` (installed from `scripts/requirements.txt`) for `.xlsx` workbooks. It does not parse `.xls`, `.pbix`, or `.pbip`. Excel is read with cached cell values (`data_only=True`); formulas are not recalculated. Run commands from the repository root because relative source paths are resolved from the current working directory.

```bash
python scripts/analyze.py --config examples/demo_sales/inventory-request.json
python scripts/analyze.py --config examples/demo_sales/model-audit-request.json
python scripts/analyze.py --config examples/demo_sales/net-sales-by-category-request.json --format markdown
python scripts/bi_report.py --config examples/demo_sales/report-request.json --output report.md
```

## Request actions

An `inventory` request has `action` and a non-empty `tables` map. Each table has a `file` path and, for `.xlsx`, an optional `sheet` name or zero-based index. The helper returns rows/columns, duplicate rows, inferred field types, missing/distinct counts, and up to five sample values per field.

A `model_audit` request adds `relationships`, each declared as `{ "one_table": "Customers", "one_column": "CustomerID", "many_table": "Orders", "many_column": "CustomerID" }`. The audit checks null and duplicate keys on the declared one side and orphan nonblank foreign keys on the many side. It does not validate every Power BI relationship property or implement filter propagation. A failed integrity check returns `valid: false`.

An `aggregate` request also supplies `fact_table`, optional `group_by`, optional `filters`, and a non-empty `measures` list. Group/filter fields use `{ "table": "Products", "column": "Category" }`. A dimension field must belong to exactly one directly declared relationship to the fact table. Multi-hop and competing relationship paths are not implemented.

Supported measure examples:

```json
{"name":"Net Sales","op":"sum_expression","expression":"Quantity * UnitPrice * (1 - DiscountPct)"}
{"name":"Order Count","op":"distinct_count","table":"Orders","column":"OrderID"}
{"name":"Rows","op":"count_rows"}
{"name":"Known Amounts","op":"count_nonblank","table":"Orders","column":"Amount"}
```

Other supported `op` values are `sum`, `mean`, `min`, and `max`. The expression parser accepts only fact-column identifiers, finite numeric constants, parentheses, unary `+`/`-`, and `+ - * /`. It rejects functions, attributes, subscripts, imports, and arbitrary code. A blank operand skips that row for `sum_expression`; division by zero is an error.

Simple explicit filters use `op` `eq`, `neq`, or `in`, for example `{ "table":"Customers", "column":"Region", "op":"eq", "value":"West" }`. A numeric filter is parsed using the detected numeric type; text values should match source values.

## Output and status

`--format json` is the stable machine-oriented result; `--format markdown` formats the same result for review. The top-level `valid` and `status` must be checked before interpretation. A failed request exits nonzero and emits an error; a model-integrity failure returns an explicit invalid result and no aggregate. `rows_input`, `rows_used`, `rows_filtered_out`, `measure_audit`, group rows, and totals are the provenance needed to describe the calculation.

Fractional aggregate results are kept as `Decimal` values internally and emitted by the JSON CLI as exact JSON number tokens rather than binary floats or quoted strings. JSON consumers that need to retain all digits should parse fractional tokens as decimal values (for example, in Python use `json.loads(text, parse_float=Decimal)`); a consumer that converts JSON numbers to IEEE-754 binary floats may round them. Integral Decimal results are emitted as integer tokens. `run_request()` returns fractional Decimal values to Python callers.

The helper does not retain, upload, or transmit the source data. Inventory samples and derived values can still be sensitive; review them before sharing. It is an independent helper, not Microsoft software or a compatible Power BI engine. It does not execute DAX or M, create native visuals, implement DAX blank/context semantics, read model metadata, or promise performance/parity. These limitations are part of the result contract, not optional caveats.
