# Demo sales overview

> Deterministic helper report; not Power BI output or DAX evaluation.

## Data inventory

> Helper output; not Power BI rendering or DAX evaluation.

## Orders

Rows: 10 · Columns: 7 · Duplicate rows: 0

| Column | Inferred type | Nonmissing | Missing | Distinct | Sample values |
|---|---|---:|---:|---:|---|
| OrderID | text or mixed | 10 | 0 | 10 | O1001, O1002, O1003, O1004, O1005 |
| OrderDate | date/datetime | 10 | 0 | 10 | 2025-01-15, 2025-02-07, 2025-03-12, 2025-04-02, 2025-05-20 |
| CustomerID | text or mixed | 10 | 0 | 5 | C01, C02, C03, C01, C04 |
| ProductID | text or mixed | 10 | 0 | 4 | P01, P02, P01, P03, P02 |
| Quantity | integer | 10 | 0 | 5 | 2, 3, 1, 4, 2 |
| UnitPrice | integer | 10 | 0 | 4 | 100, 50, 100, 25, 50 |
| DiscountPct | decimal | 10 | 0 | 4 | 0, 0.10, 0.05, 0, 0 |

## Customers

Rows: 5 · Columns: 4 · Duplicate rows: 0

| Column | Inferred type | Nonmissing | Missing | Distinct | Sample values |
|---|---|---:|---:|---:|---|
| CustomerID | text or mixed | 5 | 0 | 5 | C01, C02, C03, C04, C05 |
| CustomerName | text or mixed | 5 | 0 | 5 | Northwind Retail, Contoso Works, Fabrikam Group, Adventure Outfitters, Wide World Imports |
| Segment | text or mixed | 5 | 0 | 3 | Retail, Small Business, Enterprise, Small Business, Retail |
| Region | text or mixed | 5 | 0 | 4 | West, East, West, South, North |

## Products

Rows: 4 · Columns: 3 · Duplicate rows: 0

| Column | Inferred type | Nonmissing | Missing | Distinct | Sample values |
|---|---|---:|---:|---:|---|
| ProductID | text or mixed | 4 | 0 | 4 | P01, P02, P03, P04 |
| ProductName | text or mixed | 4 | 0 | 4 | Trail Laptop, Wireless Mouse, Desk Lamp, Design Suite |
| Category | text or mixed | 4 | 0 | 3 | Computers, Accessories, Accessories, Software |

## Model audit

> Helper output; not Power BI rendering or DAX evaluation.

Status: **valid**

| One side | Many side | Valid | Duplicate one keys | Orphan many keys | Null many keys |
|---|---|---:|---:|---:|---:|
| Customers.CustomerID | Orders.CustomerID | True | 0 | 0 | 0 |
| Products.ProductID | Orders.ProductID | True | 0 | 0 | 0 |

Checks declared direct key uniqueness and referential integrity only; it does not implement Power BI relationship or filter propagation.

## Net sales by category

> Helper output; not Power BI rendering or DAX evaluation.

Fact table: `Orders` · Rows used: 10 / 10 · Filtered out: 0

## Totals

| Measure | Value | Values used | Blank/skipped |
|---|---:|---:|---:|
| Net Sales | 1705 | 10 | 0 |
| Order Count | 10 | 10 | 0 |

## Groups

| Products.Category | Net Sales | Order Count | Rows |
|---|---|---|---|
| Accessories | 635 | 5 | 5 |
| Computers | 595 | 3 | 3 |
| Software | 475 | 2 | 2 |

Only declared direct fact-to-dimension lookups, explicit filters, and listed aggregation operations are implemented; no DAX context, M query, or Power BI engine is present.

## Limitations

The helper computes only its documented inventory, declared-key audits, and simple aggregate operations. It does not execute DAX or Power Query M, implement Power BI filter context, render visuals, or access a Power BI tenant. Review the linked method limits before relying on results.
