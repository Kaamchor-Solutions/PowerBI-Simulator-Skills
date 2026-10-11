# Semantic-model design reference

Start from business process and row grain rather than from file names. A fact table should have a precise sentence such as “one row per order line”; dimensions should have one row per durable entity key and attributes suitable for slicing. Check keys and row uniqueness before describing cardinality. Keep different grains in separate facts unless a deliberate design supports them.

A conventional star model places fact tables in the center and dimensions around them, with one-to-many, single-direction relationships from dimensions to facts. The pattern often improves reasoning and report behavior, but is not a universal requirement. Explain exceptions such as bridge tables, many-to-many relationships, role-playing dimensions, inactive relationships, and multiple filter paths rather than hiding them.

A date dimension should have one row for each date in the intended range, a unique date key, explicit calendar/fiscal attributes, and a deliberate relationship to the fact date. Timestamp normalization, timezone, fiscal boundaries, working days, and holiday definitions are business decisions. Do not assume the built-in helper's direct key check creates a date table or enables DAX time intelligence.

For each proposed relationship document:

| Property | Record |
|---|---|
| Grain | What one row on each side means |
| Key | Candidate key and foreign key, including data types |
| Cardinality | One-to-many, one-to-one, or unresolved/many-to-many |
| Direction/status | Intended filter direction; active/inactive; role-playing meaning |
| Quality | Nulls, duplicate one-side keys, orphan foreign keys |
| Decision | Why this relationship is needed and what remains unverified |

The bundled companion audits only explicitly declared direct key uniqueness and referential integrity. It does not implement Power BI's relationship graph, ambiguity rules, filter context, RLS, or storage engine.
