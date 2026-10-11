# Data audit protocol

1. Confirm each source actually available to the LLM/runtime. Record filename, sheet/table, encoding, and read errors. Do not imply a direct Power BI connector.
2. Preserve the source. Do not overwrite files, normalize values, remove rows, or fill nulls as part of an inspection.
3. When the companion is available, create an `inventory` JSON request and run `python scripts/analyze.py --config <request.json>`. Check the returned action and `valid` status. The helper reads CSV, TSV/TAB, and `.xlsx` only; its Excel reader uses cached values and does not recalculate workbook formulas.
4. Report table grain candidates, row/column counts, field names and inferred types, missing counts, distinct counts, sample values, and duplicate rows. Explicitly label types/roles as inferred. Protect identifiers and sensitive sample values.
5. Investigate likely IDs, blank keys, duplicate keys, mixed numeric/text columns, leading zeros, dates/time zones, sentinel values, and impossible ranges. Do not infer that 0, 99, or another code means missing.
6. Ask only for unresolved definitions that affect the requested model or metric. If no code/file access exists, request a small privacy-safe sample and codebook or give the user a reproducible local command.

A profile is not proof that the source is correct. State checks not performed and keep original data untouched.
