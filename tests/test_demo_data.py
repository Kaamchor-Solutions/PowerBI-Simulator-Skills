"""Validate the synthetic demo fixture only; this is not a DAX/Power BI engine."""
import csv
import unittest
from decimal import Decimal
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "examples" / "demo_sales"


def read_csv(name):
    with (DATA / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class DemoDataTests(unittest.TestCase):
    def test_keys_and_foreign_keys(self):
        customers = read_csv("customers.csv")
        products = read_csv("products.csv")
        orders = read_csv("orders.csv")

        customer_ids = [row["CustomerID"] for row in customers]
        product_ids = [row["ProductID"] for row in products]
        order_ids = [row["OrderID"] for row in orders]

        self.assertEqual(len(customer_ids), len(set(customer_ids)))
        self.assertEqual(len(product_ids), len(set(product_ids)))
        self.assertEqual(len(order_ids), len(set(order_ids)))
        self.assertTrue({row["CustomerID"] for row in orders} <= set(customer_ids))
        self.assertTrue({row["ProductID"] for row in orders} <= set(product_ids))

    def test_reference_totals(self):
        customers = {row["CustomerID"]: row for row in read_csv("customers.csv")}
        products = {row["ProductID"]: row for row in read_csv("products.csv")}
        orders = read_csv("orders.csv")
        total = Decimal("0")
        by_category = {}
        by_region = {}

        for row in orders:
            amount = (
                Decimal(row["Quantity"])
                * Decimal(row["UnitPrice"])
                * (Decimal("1") - Decimal(row["DiscountPct"]))
            )
            category = products[row["ProductID"]]["Category"]
            region = customers[row["CustomerID"]]["Region"]
            total += amount
            by_category[category] = by_category.get(category, Decimal("0")) + amount
            by_region[region] = by_region.get(region, Decimal("0")) + amount

        self.assertEqual(len(orders), 10)
        self.assertEqual(total, Decimal("1705.00"))
        self.assertEqual(total / Decimal(len(orders)), Decimal("170.50"))
        self.assertEqual(
            by_category,
            {
                "Computers": Decimal("595.00"),
                "Accessories": Decimal("635.00"),
                "Software": Decimal("475.00"),
            },
        )
        self.assertEqual(
            by_region,
            {
                "West": Decimal("720.00"),
                "East": Decimal("335.00"),
                "South": Decimal("100.00"),
                "North": Decimal("550.00"),
            },
        )


if __name__ == "__main__":
    unittest.main()
