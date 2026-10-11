# Power BI Simulator Skills

**A provider-neutral LLM skill for Power BI-style analytics, paired with a small deterministic Python helper.** This is a local, unpublished draft intended as a sibling to [Kaamchor-Solutions/SPSS-Simulator-Skills](https://github.com/Kaamchor-Solutions/SPSS-Simulator-Skills). Its proposed destination is [Kaamchor-Solutions/PowerBI-Simulator-Skills](https://github.com/Kaamchor-Solutions/PowerBI-Simulator-Skills); neither the exact public package nor its license has been approved for release.

> **What this is:** an LLM-guided simulation for inspecting accessible tables, proposing a semantic model, drafting DAX/Power Query M, planning report pages, and computing a narrow set of transparent table operations. **What this is not:** Microsoft Power BI Desktop/Service, a DAX or Power Query engine, a `.pbix`/`.pbip` parser, or a clone/replacement for Microsoft's proprietary software. It cannot connect to a tenant, refresh/publish a model, render native visuals, or establish Power BI parity.

## What is included

- `SKILL.md`: detailed Agent Skill with task routing, workflow, guardrails, and protocol links.
- `SYSTEM_PROMPT.md`: copy-paste fallback for chat LLMs that do not load skill folders.
- `scripts/analyze.py`: deterministic inventory, explicit relationship key audit, and constrained aggregates from CSV/TSV/TAB/`.xlsx`.
- `scripts/bi_report.py`: combines multiple supported requests into a reproducible Markdown note.
- `protocols/` and `references/`: on-demand guidance for data audit, semantic models, aggregate boundaries, DAX/M drafting, report design, validation, and runtime schema.
- `examples/demo_sales/`: fabricated tables, runnable JSON requests, and hand-checkable totals.
- `tests/` and `.github/workflows/tests.yml`: helper/fixture tests, a portable LLM conformance suite, and Python CI.

## Quick start from a local checkout

Install the optional Excel reader and run the examples from the repository root:

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r scripts/requirements.txt
python scripts/analyze.py --config examples/demo_sales/inventory-request.json --format markdown
python scripts/analyze.py --config examples/demo_sales/model-audit-request.json
python scripts/analyze.py --config examples/demo_sales/net-sales-by-category-request.json
python scripts/bi_report.py --config examples/demo_sales/report-request.json --output demo-report.md
python -m unittest discover -s tests -v
```

For CSV/TSV-only requests, Python's standard library is enough; `openpyxl` is needed for `.xlsx`. Example totals: Net Sales `1705`, Order Count `10`, and West-region Net Sales `720` (no currency is assigned). The helper uses its own bounded operations; it does **not** run the accompanying DAX examples.

## Use with an LLM

For ChatGPT, Claude, or another chat-first model, use [`SYSTEM_PROMPT.md`](SYSTEM_PROMPT.md) as the project/custom instruction where supported. Add `SKILL.md` and the relevant protocols/references as project knowledge or attach them to a task. Upload data only through a host workflow you are authorized to use. See [`docs/installation.md`](docs/installation.md) and [`docs/using-with-llms.md`](docs/using-with-llms.md).

For exact helper results, an execution environment must be able to access both the repository and the input files, and must actually run `scripts/analyze.py`. A prompt alone does not install code, grant file access, or provide computation. Without such a tool, the LLM can still explain concepts, draft formulas, propose a model, mock a report page, or interpret supplied output—but must not invent results.

## Check LLM behavior across hosts

The package includes a provider-neutral response-pattern suite; it makes no model/API calls and is not a benchmark or parity claim. Follow [`tests/llm_conformance/README.md`](tests/llm_conformance/README.md) to load the same instructions in each host, run the prompts in fresh chats, record verbatim responses, and score them locally. From the repository root, use `python tests/llm_conformance/score.py --print-prompts`, then create a response file with `python tests/llm_conformance/score.py --init-responses /tmp/llm-responses.json`, fill it with the host's outputs, and run `python tests/llm_conformance/score.py --responses /tmp/llm-responses.json`. Review the rubric results and full responses manually.

## Simulation contract

Keep **proposed** DAX/M separate from **executed** helper calculations, and keep a textual/wireframe report simulation separate from a real Power BI report. Never claim that a query ran, DAX compiled, a model refreshed, or a report was published unless a compatible authorized tool performed that exact action and confirmed it. The bundled helper supports only a documented subset; see [`docs/methods-and-limitations.md`](docs/methods-and-limitations.md) and [`references/companion-runtime.md`](references/companion-runtime.md).

## Repository map

```text
SKILL.md                          Agent Skill instructions
SYSTEM_PROMPT.md                  Chat-first system-prompt fallback
scripts/analyze.py                Bounded JSON-in/JSON-out helper
scripts/bi_report.py              Multi-analysis Markdown report builder
scripts/requirements.txt           Optional Excel reader
protocols/                        On-demand task procedures
references/                       Model and runtime guidance
docs/                             Install, setup, limits, sample output
examples/demo_sales/              Fabricated CSVs and runnable requests
templates/workspace-state.md      Portable simulation continuity template
tests/                            Fixture tests and portable LLM conformance suite
.github/workflows/tests.yml        Python CI
```

## Development

```bash
python -m pip install -r scripts/requirements.txt
python -m unittest discover -s tests -v
```

Tests cover the helper's stated behavior, small fabricated fixtures, and local response-pattern checks; they do not prove DAX execution or Microsoft product equivalence. The conformance suite does not contact a model host. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before submitting changes.

## Privacy, affiliation, and license

This independent project is not affiliated with or endorsed by Microsoft. “Power BI” and related marks belong to their respective owners. LLM file access, execution, context size, retention, and connectors depend on the selected host. Do not upload confidential data without authorization; helper samples and derived summaries may still be sensitive. The license is pending approval and the local draft grants no publication or distribution rights. See [`docs/release-review.md`](docs/release-review.md) for status and repository identity; no GitHub changes or publication are part of this package.
