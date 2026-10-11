# Demo sales simulation

All names and records in this directory are fabricated for demonstration. The three CSV files contain 10 order rows covering 2025; the numeric amounts have no stated currency.

## Try the deterministic helper

Run these commands from the repository root:

```bash
python scripts/analyze.py --config examples/demo_sales/inventory-request.json
python scripts/analyze.py --config examples/demo_sales/model-audit-request.json
python scripts/analyze.py --config examples/demo_sales/net-sales-by-category-request.json --format markdown
python scripts/analyze.py --config examples/demo_sales/west-region-request.json
python scripts/bi_report.py --config examples/demo_sales/report-request.json --output demo-report.md
```

This companion computes the listed inventory, declared key checks, and supported aggregate operations. It is not a DAX/M interpreter or a Power BI engine. Run `python -m unittest discover -s tests -v` to check the fixture and helper.

## Try the LLM skill

Upload `customers.csv`, `products.csv`, and `orders.csv` to an LLM configured with `SYSTEM_PROMPT.md`, then ask:

> Simulate a Power BI sales overview for these files. State each table's grain, propose relationships and a date table, write Net Sales, Order Count, and Average Order Value measures, and mock up an overview page with monthly trend, category comparison, and customer-region breakdown. Clearly label which values the bundled helper computed and which DAX is only proposed.

## Reference model

- `Orders`: one row per order line (one line per order in this fixture); candidate key `OrderID`.
- `Customers`: one row per `CustomerID`.
- `Products`: one row per `ProductID`.
- Proposed relationships: `Customers[CustomerID]` 1-to-many `Orders[CustomerID]`; `Products[ProductID]` 1-to-many `Orders[ProductID]`; a continuous calendar date table 1-to-many `Orders[OrderDate]`. Use single-direction filtering from dimensions to `Orders` by default.

## Example measures (proposed DAX)

```DAX
Net Sales :=
SUMX (
    Orders,
    Orders[Quantity]
        * Orders[UnitPrice]
        * ( 1 - COALESCE ( Orders[DiscountPct], 0 ) )
)

Order Count :=
DISTINCTCOUNT ( Orders[OrderID] )

Average Order Value :=
DIVIDE ( [Net Sales], [Order Count] )
```

These formulas are examples, not executed by this repository. Confirm the business definition of sales, number/currency format, data types, and DAX locale in a real model.

## Fixture reference totals

Using each row's `Quantity * UnitPrice * (1 - DiscountPct)`:

| Check | Expected value |
|---|---:|
| Order rows | 10 |
| Net Sales | 1705.00 |
| Order Count | 10 |
| Average Order Value | 170.50 |
| Net Sales — Computers | 595.00 |
| Net Sales — Accessories | 635.00 |
| Net Sales — Software | 475.00 |
| Net Sales — West | 720.00 |
| Net Sales — East | 335.00 |
| Net Sales — South | 100.00 |
| Net Sales — North | 550.00 |

These reference values are independently calculated from the included fabricated rows. The accompanying tests validate the CSV fixture arithmetic and helper behavior; they do **not** validate DAX, Power BI behavior, or Microsoft product parity.
