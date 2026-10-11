# Aggregation protocol

Use this protocol only when the bundled helper can run on the actual source files. Read [../references/companion-runtime.md](../references/companion-runtime.md) for request schema and precise behavior.

1. Confirm the fact grain and define every measure in business language, including units, filter policy, blank behavior, and distinct-count key.
2. Build an `aggregate` request with `fact_table`, optional `group_by`/`filters`, declared `relationships`, and explicit `measures`. Use fully specified field objects: `{"table":"Orders","column":"Amount"}`.
3. Supported measure ops: `count_rows`, `count_nonblank`, `distinct_count`, `sum`, `mean`, `min`, `max`, and `sum_expression`. Expression sums allow only arithmetic over fact-table column identifiers and numeric constants. They do not implement DAX functions.
4. Supported filters: `eq`, `neq`, and `in`. A group/filter field may be in the fact table or in one directly related dimension on the one side. Multi-hop paths and competing paths are unsupported.
5. Run `python scripts/analyze.py --config request.json`; inspect `valid`, `rows_input`, `rows_used`, `rows_filtered_out`, totals, groups, and measure audit. Never hide blanks or filtered rows.
6. Compare totals to a hand-checkable independent calculation or a reconciled source total. Check that aggregations fit the grain (e.g., summing a repeated order-header amount at line grain can double-count).
7. Present the exact helper result as a constrained simulation, not Power BI output. Explain that DAX blank semantics, filter context, relationships, and engine behavior are not being emulated.

If the requested calculation needs unsupported DAX, time intelligence, many-to-many filtering, ranking, percent-of-total, calculation groups, or complex context, do not approximate it through the helper. Draft the DAX for the user to run or ask for a verified export.
