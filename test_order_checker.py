import csv
import tempfile
import unittest
from pathlib import Path

from order_checker import REQUIRED_FIELDS, check_orders


class TestOrderChecker(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.temp_path = Path(self.temp_dir.name)

    def write_csv(self, columns, rows, filename="orders.csv"):
        """Write test orders to a temporary CSV file and return its path."""
        file_path = self.temp_path / filename

        with file_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(columns)
            writer.writerows(rows)

        return file_path

    def test_valid_orders_have_no_problems(self):
        file_path = self.write_csv(
            REQUIRED_FIELDS,
            [["EG2001", "Mona", "Scarf", "2", "Cash"]],
        )

        self.assertEqual(check_orders(file_path), [])

    def test_duplicate_order_id_is_reported(self):
        file_path = self.write_csv(
            REQUIRED_FIELDS,
            [
                ["EG2001", "Mona", "Scarf", "2", "Cash"],
                ["EG2001", "Ali", "Mug", "1", "Wallet"],
            ],
        )

        self.assertIn("Row 3: duplicate order ID EG2001", check_orders(file_path))

    def test_missing_required_value_is_reported(self):
        file_path = self.write_csv(
            REQUIRED_FIELDS,
            [["EG2001", "", "Scarf", "2", "Cash"]],
        )

        self.assertIn("Row 2: missing customer_name", check_orders(file_path))

    def test_invalid_quantities_are_reported(self):
        invalid_quantities = ["abc", "0", "-5", "2.5"]

        for quantity in invalid_quantities:
            with self.subTest(quantity=quantity):
                file_path = self.write_csv(
                    REQUIRED_FIELDS,
                    [["EG2001", "Mona", "Scarf", quantity, "Cash"]],
                )

                self.assertIn(
                    f"Row 2: invalid quantity '{quantity}' (must be a positive whole number)",
                    check_orders(file_path),
                )

    def test_missing_required_column_is_reported(self):
        columns = [field for field in REQUIRED_FIELDS if field != "product"]
        file_path = self.write_csv(columns, [])

        self.assertEqual(
            check_orders(file_path),
            ["CSV header is missing required column(s): product"],
        )

    def test_multiple_missing_columns_are_reported(self):
        columns = [field for field in REQUIRED_FIELDS if field not in ["product", "quantity"]]
        file_path = self.write_csv(columns, [])

        self.assertEqual(
            check_orders(file_path),
            ["CSV header is missing required column(s): product, quantity"],
        )

    def test_nonexistent_input_file_raises_file_not_found_error(self):
        file_path = self.temp_path / "does_not_exist.csv"

        with self.assertRaises(FileNotFoundError):
            check_orders(file_path)

    def test_incomplete_row_reports_missing_fields(self):
        file_path = self.write_csv(
            ["customer_name", "product", "payment_method", "order_id", "quantity"],
            [
                ["Mona", "Scarf", "Cash"],
                ["Ali", "Mug", "Wallet", "EG2002", "1"],
            ],
        )

        self.assertEqual(
            check_orders(file_path),
            ["Row 2: missing order_id, quantity"],
        )

    def test_utf8_bom_header_is_read_correctly(self):
        file_path = self.temp_path / "orders_with_bom.csv"
        file_path.write_text(
            ",".join(REQUIRED_FIELDS) + "\nEG2001,Mona,Scarf,2,Cash\n",
            encoding="utf-8-sig",
        )

        self.assertEqual(check_orders(file_path), [])


if __name__ == "__main__":
    unittest.main()
