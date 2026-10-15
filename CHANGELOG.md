# Changelog

## 0.1.0 — 2026-10-12

- Add provider-neutral Power BI-style LLM skill and copy-paste system prompt.
- Add bounded Python helper for CSV/TSV/XLSX inventory, declared relationship audits, and constrained aggregates.
- Add Markdown multi-analysis report builder, protocols, references, installation guidance, and fabricated sales fixture.
- Add helper/fixture tests and CI workflow.
- Preserve fractional Decimal aggregates in JSON without converting them to binary floats; add a precision regression test.
- Make finite decimal addition, subtraction, multiplication, and sums context-independent and exact within an explicit 100,000-digit safety bound; use documented 50-significant-digit division and preserve JSON number tokens without float parsing.
- Normalize malformed workbook errors, reject boolean-to-number coercion, and add coverage for all aggregate operations, filters, TSV/TAB inputs, and report-builder failure paths.
- Normalize analyzer output-write failures into concise nonzero CLI errors instead of tracebacks.
- Add a portable, offline LLM conformance prompt suite and scorer for comparing host behavior.
- Expand adversarial contradiction cases and explicitly report lexical pattern passes as non-semantic checks, not proof of model correctness.
- Add regression probes for number words, implied DAX success, invented PBIX inventories, passive uploads, assumed metric rules, unsupported report completion, and claimed Power BI rendering/refresh.
- Add safe-refusal and negative-wording controls to constrain false positives from those lexical checks.
- Catch quoted number-word totals, implied DAX success, “contains” PBIX inventories, incomplete/ready report claims, passive upload modifiers, and past-tense refresh claims.
- Catch common numeric-result constructions such as “comes to,” “amounts to,” “totals,” and “works out to,” with a safe no-result control.
- Catch quoted currency values and approximate compact numbers such as `$4.2k`, while keeping explicit no-result refusals as controls.
- Add a configurable per-request source-file byte limit with a 128 MiB default and 256 MiB hard maximum; reject oversized inputs before parsing.
- Add a configurable per-file row-record limit (100,000 default; 250,000 maximum), enforced during CSV/XLSX iteration, and avoid materializing a second XLSX row list.
- Add a configurable header-width limit (256 columns default; 4,096 maximum), rejected before CSV/XLSX data rows are read.
- Add a standard-library deterministic archive builder with fixed metadata, sorted paths, exclusions, atomic output, and repeat-build verification; cover it with unit tests and README instructions.
- Add a local 360-degree smoke-test record with exercised checks, unrun platform/model gaps, and release boundaries.
- Finalize the release citation metadata and standard MIT license; publish the package at Kaamchor-Solutions/PowerBI-Simulator-Skills.
- Explicitly exclude DAX/M execution, Power BI engine parity, native visuals, tenant integration, and `.pbix`/`.pbip` support.
