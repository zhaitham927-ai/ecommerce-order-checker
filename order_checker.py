import csv


REQUIRED_FIELDS = ["order_id", "customer_name", "product", "quantity", "payment_method"]


def check_orders(filename):
    """Read orders from a CSV file and return a list of problem messages."""
    problems = []
    seen_order_ids = set()

    with open(filename, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        header = reader.fieldnames or []
        missing_columns = [field for field in REQUIRED_FIELDS if field not in header]

        if missing_columns:
            problems.append(
                f"CSV header is missing required column(s): {', '.join(missing_columns)}"
            )
            return problems

        for row_number, order in enumerate(reader, start=2):
            values = {
                field: (order[field] or "").strip()
                for field in REQUIRED_FIELDS
            }
            order_id = values["order_id"]
            quantity = values["quantity"]
            missing_fields = [
                field for field in REQUIRED_FIELDS if not values[field]
            ]

            if missing_fields:
                problems.append(
                    f"Row {row_number}: missing {', '.join(missing_fields)}"
                )

            if quantity and (not quantity.isdecimal() or int(quantity) <= 0):
                problems.append(
                    f"Row {row_number}: invalid quantity '{quantity}' "
                    "(must be a positive whole number)"
                )

            if order_id:
                if order_id in seen_order_ids:
                    problems.append(
                        f"Row {row_number}: duplicate order ID {order_id}"
                    )
                else:
                    seen_order_ids.add(order_id)

    return problems


if __name__ == "__main__":
    try:
        report = check_orders("orders.csv")
    except FileNotFoundError:
        print("Could not find 'orders.csv'. Make sure it is in the terminal's current working folder.")
        print(
            "No new report was created. If 'order_report.csv' already exists, "
            "it may contain results from an earlier run."
        )
    else:
        try:
            with open("order_report.csv", "w", newline="", encoding="utf-8") as report_file:
                writer = csv.writer(report_file)
                writer.writerow(["Problem"])

                for problem in report:
                    writer.writerow([problem])
        except OSError:
            print(
                "Could not save 'order_report.csv'. It could be incomplete or "
                "partially overwritten. The terminal report is still available. "
                "Make sure the file isn't open in Excel and that you have "
                "permission to write to this folder."
            )

        print("Order check report")
        print("------------------")

        if report:
            for problem in report:
                print(f"- {problem}")
        else:
            print("No problems found.")
