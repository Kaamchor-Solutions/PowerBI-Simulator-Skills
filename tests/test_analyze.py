"""Smoke and contract tests for the constrained helper (not Power BI parity tests)."""
import csv
import json
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import analyze  # noqa: E402

DEMO = ROOT / "examples" / "demo_sales"
TABLES = {
    "Orders": {"file": str(DEMO / "orders.csv")},
    "Customers": {"file": str(DEMO / "customers.csv")},
    "Products": {"file": str(DEMO / "products.csv")},
}
RELATIONSHIPS = [
    {"one_table": "Customers", "one_column": "CustomerID", "many_table": "Orders", "many_column": "CustomerID"},
    {"one_table": "Products", "one_column": "ProductID", "many_table": "Orders", "many_column": "ProductID"},
]


class AnalyzeTests(unittest.TestCase):
    def test_inventory_reports_shape_and_missingness(self):
        result = analyze.run_request({"action": "inventory", "tables": TABLES})
        self.assertTrue(result["valid"])
        self.assertEqual(result["tables"]["Orders"]["rows"], 10)
        fields = {field["name"]: field for field in result["tables"]["Orders"]["fields"]}
        self.assertEqual(fields["Quantity"]["inferred_type"], "integer")
        self.assertEqual(fields["DiscountPct"]["missing"], 0)

    def test_declared_star_relationships_pass(self):
        result = analyze.run_request({"action": "model_audit", "tables": TABLES, "relationships": RELATIONSHIPS})
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["relationships"]), 2)
        self.assertEqual(sum(item["orphan_count"] for item in result["relationships"]), 0)

    def test_orphans_are_reported_and_model_is_invalid(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "orders.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(["OrderID", "CustomerID"])
                writer.writerow(["O1", "missing-customer"])
            tables = {"Customers": TABLES["Customers"], "Orders": {"file": str(path)}}
            result = analyze.run_request({
                "action": "model_audit",
                "tables": tables,
                "relationships": [{"one_table": "Customers", "one_column": "CustomerID", "many_table": "Orders", "many_column": "CustomerID"}],
            })
        self.assertFalse(result["valid"])
        self.assertEqual(result["relationships"][0]["orphan_count"], 1)

    def test_grouped_sales_aggregate_matches_fixture(self):
        request = {
            "action": "aggregate",
            "tables": TABLES,
            "relationships": RELATIONSHIPS,
            "fact_table": "Orders",
            "group_by": [{"table": "Products", "column": "Category"}],
            "measures": [
                {"name": "Net Sales", "op": "sum_expression", "expression": "Quantity * UnitPrice * (1 - DiscountPct)"},
                {"name": "Order Count", "op": "distinct_count", "table": "Orders", "column": "OrderID"},
            ],
        }
        result = analyze.run_request(request)
        self.assertTrue(result["valid"])
        self.assertEqual(result["totals"]["Net Sales"], 1705)
        self.assertEqual(result["totals"]["Order Count"], 10)
        by_category = {row["group"]["Products.Category"]: row["measures"]["Net Sales"] for row in result["groups"]}
        self.assertEqual(by_category, {"Accessories": 635, "Computers": 595, "Software": 475})

    def test_decimal_aggregate_is_preserved_as_an_exact_json_number(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "amounts.csv"
            path.write_text("Amount\n123456789012345.6789012345\n0.0000000001\n", encoding="utf-8")
            result = analyze.run_request({
                "action": "aggregate",
                "tables": {"Sales": {"file": str(path)}},
                "fact_table": "Sales",
                "measures": [{"name": "Precise Total", "op": "sum", "table": "Sales", "column": "Amount"}],
            })
        expected = Decimal("123456789012345.6789012346")
        self.assertEqual(result["totals"]["Precise Total"], expected)
        serialized = analyze._json_dumps(result, indent=2)
        self.assertIn('"Precise Total": 123456789012345.6789012346', serialized)
        self.assertNotIn('"Precise Total": "123456789012345.6789012346"', serialized)
        decoded = json.loads(serialized, parse_float=Decimal)
        self.assertEqual(decoded["totals"]["Precise Total"], expected)

    def test_dimension_filter_is_applied_to_fact_rows(self):
        request = {
            "action": "aggregate",
            "tables": TABLES,
            "relationships": RELATIONSHIPS,
            "fact_table": "Orders",
            "filters": [{"table": "Customers", "column": "Region", "op": "eq", "value": "West"}],
            "measures": [{"name": "Net Sales", "op": "sum_expression", "expression": "Quantity * UnitPrice * (1 - DiscountPct)"}],
        }
        result = analyze.run_request(request)
        self.assertTrue(result["valid"])
        self.assertEqual(result["rows_used"], 5)
        self.assertEqual(result["totals"]["Net Sales"], 720)

    def test_expression_cannot_call_functions(self):
        with self.assertRaises(analyze.RequestError):
            analyze._compile_expression("__import__('os').system('echo unsafe')", {"Quantity"})

    def test_xlsx_named_sheet_is_read(self):
        import openpyxl
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sales.xlsx"
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Data"
            sheet.append(["Code", "Amount"])
            sheet.append(["A", 12.5])
            workbook.save(path)
            result = analyze.run_request({"action": "inventory", "tables": {"Sales": {"file": str(path), "sheet": "Data"}}})
        self.assertEqual(result["tables"]["Sales"]["rows"], 1)
        self.assertEqual(result["tables"]["Sales"]["fields"][1]["inferred_type"], "decimal")

    def test_header_only_csv_keeps_its_schema(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "empty.csv"
            path.write_text("Key,Value\n", encoding="utf-8")
            result = analyze.run_request({"action": "inventory", "tables": {"Empty": {"file": str(path)}}})
        self.assertEqual(result["tables"]["Empty"]["rows"], 0)
        self.assertEqual([field["name"] for field in result["tables"]["Empty"]["fields"]], ["Key", "Value"])

    def test_unicode_and_space_in_path(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp) / "BI data Δ"
            folder.mkdir()
            path = folder / "地域.csv"
            path.write_text("City,Amount\nMünchen,12\n", encoding="utf-8")
            result = analyze.run_request({"action": "inventory", "tables": {"Sales": {"file": str(path)}}})
        self.assertEqual(result["tables"]["Sales"]["fields"][0]["sample_values"], ["München"])

    def test_unknown_filter_column_is_a_request_error(self):
        request = {
            "action": "aggregate", "tables": TABLES, "relationships": RELATIONSHIPS,
            "fact_table": "Orders", "filters": [{"table": "Customers", "column": "NotAColumn", "value": "West"}],
            "measures": [{"name": "Rows", "op": "count_rows"}],
        }
        with self.assertRaises(analyze.RequestError):
            analyze.run_request(request)

    def test_output_cannot_overwrite_input(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source.csv"
            config = {"tables": {"Sales": {"file": str(source)}}}
            with self.assertRaises(analyze.RequestError):
                analyze.ensure_output_safe(source, Path(temp) / "request.json", config)

    def test_markdown_is_explicitly_labeled(self):
        result = analyze.run_request({"action": "inventory", "tables": TABLES})
        rendered = analyze.format_markdown(result)
        self.assertIn("not Power BI rendering or DAX evaluation", rendered)
        self.assertIn("## Orders", rendered)


if __name__ == "__main__":
    unittest.main()
