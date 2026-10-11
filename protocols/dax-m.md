# DAX and Power Query M protocol

## DAX

- Confirm exact table/column names, data types, grain, intended filter context, blank handling, and unit/currency before drafting a measure.
- Prefer measures for context-dependent aggregates; use calculated columns only when row-level storage is intended. State whether a formula is a measure or column.
- Use readable names and formatting. Explain row context versus filter context where relevant, and call out `CALCULATE`, iterators, relationships, and time-intelligence assumptions.
- Add a small verification recipe with expected output from a hand-checkable fixture or a Power BI visual/test page.
- Every formula must be labeled **proposed, not executed here**. The helper only evaluates arithmetic `sum_expression`; it does not parse DAX, including functions that appear in examples.

## Power Query M

- Confirm source, types, locale, header behavior, null/error policy, and refresh expectations. Outline each transformation in order and preserve source columns unless the user authorizes changes.
- Provide M as a draft with explicit step names and a validation check (row count, column types, key duplicates, or sample rows).
- The bundled helper does not run M, query folding, connectors, refresh, gateway, or credential logic. Do not include credentials in queries or ask users to paste secrets into code snippets.

Do not claim formula correctness, query performance, refresh success, or parity until tested in the intended Power BI environment.
