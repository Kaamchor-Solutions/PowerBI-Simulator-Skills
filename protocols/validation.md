# Validation and reporting protocol

- Inspect the helper's `valid`/`status` before interpreting numbers. An error or invalid relationship audit is not a usable result.
- Reconcile row counts, distinct keys, total measures, and filtered subsets. For additive sums, compare grouped values with the grand total when the dimensions partition the fact rows.
- Check grain to avoid duplicate counting, particularly order-header totals repeated across lines, many-to-many bridges, and distinct counts. Confirm numeric type, blanks, signs, units, currency, rounding, and date/time zone.
- Preserve exact request JSON and the helper version/commit for reruns. State source filenames/sheets and any assumptions; never include credentials or raw personal records in a report.
- Mark DAX/M as proposed, visuals as wireframes, and any unrun output as uncomputed. A markdown report does not imply Power BI validation.
- Use a concise result block: **Inspected/computed**, **Model/report proposal**, **Proposed formulas (not executed)**, **Checks and limitations**, **Next action**. Adapt when the user asks for a narrower response.
- Do not assert Microsoft Power BI equivalence. Differences from DAX, blank handling, relationships, filter context, data types, timezone, and engine behavior are expected.
