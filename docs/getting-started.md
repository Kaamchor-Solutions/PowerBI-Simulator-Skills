# Getting started

## 1. Prepare the helper

From the repository root, create a Python environment and install the optional Excel reader:

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r scripts/requirements.txt
```

The commands below use fabricated example data; relative file paths are resolved from the repository root.

## 2. Inventory the sources

```bash
python scripts/analyze.py --config examples/demo_sales/inventory-request.json --format markdown
```

Review field names, inferred types, missing values, distinct counts, and duplicates. Inferred type is a hint, not a business definition.

## 3. Check declared relationships

```bash
python scripts/analyze.py --config examples/demo_sales/model-audit-request.json
```

The demo checks customer/product one-side keys and order foreign keys. The helper's `model_audit` action does not test Power BI filter context or the whole model graph.

## 4. Compute a supported subset

```bash
python scripts/analyze.py --config examples/demo_sales/net-sales-by-category-request.json --format markdown
python scripts/analyze.py --config examples/demo_sales/west-region-request.json
```

Expected demo totals are Net Sales `1705` and Order Count `10`; West-region Net Sales is `720`. The amount has no assigned currency. These are results from the bundled arithmetic helper, not Power BI/DAX execution.

## 5. Build a reproducible report note

```bash
python scripts/bi_report.py --config examples/demo_sales/report-request.json --output demo-report.md
```

The report records successful analyses and any analysis that did not run. Review output before sharing, even with fabricated examples.

## 6. Use the LLM workflow

Use `SYSTEM_PROMPT.md` as a provider-neutral instruction fallback or install the full folder in a skills-aware coding harness. For the first conversation, ask the model to state what it can access, inventory the files, propose a model, draft measures, and label DAX as unexecuted. See [installation.md](installation.md) for chat/project and coding-harness setups.

Run the regression tests:

```bash
python -m unittest discover -s tests -v
```
