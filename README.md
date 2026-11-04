# E-commerce Order Checker

A small Python tool that checks an order CSV file for common data-entry problems and writes the findings to a report file. This is an early portfolio and learning project.

## Business problem

Online stores may receive order data with missing details, invalid quantities, or repeated order IDs. These problems can require manual review before staff can process the orders.

The Order Checker scans a CSV file and lists the issues it finds, helping make that review easier. It flags problems for a person to inspect; it does not correct orders or process them.

## Implemented features

- Reads `orders.csv` from the terminal's current folder.
- Checks that the required CSV columns are present.
- Reports blank values in required fields.
- Reports quantities that are not positive whole numbers.
- Detects repeated, non-empty order IDs.
- Writes each detected problem to `order_report.csv`.
- Prints a brief result summary to the terminal.

## Technologies

- Python 3
- Python standard library:
  - `csv` for reading and writing CSV files
  - `unittest`, `tempfile`, and `pathlib` for automated tests

No third-party packages are required.

## Run the order checker

1. Open a terminal in the project folder.
2. Make sure `orders.csv` is in that folder.
3. Run:

   ```text
   python order_checker.py
   ```

   On Windows, if `python` is not recognized, try:

   ```text
   py order_checker.py
   ```

The program prints a summary and saves `order_report.csv` in the terminal's current folder. A successful save replaces the previous report.

If `orders.csv` is missing, the checker warns that an existing report may be from an earlier run. If saving fails, the checker still prints the findings in the terminal and warns that the CSV report may be incomplete.

## Run the automated tests

From the project folder, run:

```text
python -m unittest -v
```

On Windows, if `python` is not recognized, try:

```text
py -m unittest -v
```

The tests use temporary, fictional CSV files and remove them after each test. They test valid orders, duplicate IDs, missing values, invalid quantities, missing columns, and a missing input file. They do not use the project's `orders.csv` or write to `order_report.csv`.

## Input CSV format

The input file must be named `orders.csv` and contain these column names:

```csv
order_id,customer_name,product,quantity,payment_method
EG2001,Mona,Scarf,2,Cash
```

Each data row represents one order. All five columns are required, and every field must contain a value. `quantity` must be a positive whole number, such as `1` or `12`.

## Generated report

The program creates `order_report.csv` with one column named `Problem`. Each detected issue is written on its own row. For example:

```csv
Problem
Row 3: duplicate order ID EG2001
Row 4: invalid quantity '0' (must be a positive whole number)
```

If no problems are found, the report contains the `Problem` header and no issue rows.

## Example demonstration

The `examples` folder contains a fictional order file with four deliberate errors. From the project folder, run these commands in PowerShell:

```powershell
cd examples
python ..\order_checker.py
```

The checker reads `examples/orders.csv` and generates `examples/order_report.csv` with four findings:

- A duplicate order ID
- A missing customer name
- An invalid quantity (`abc`)
- A missing order ID

You can open the generated CSV report in Microsoft Excel to review the findings.

## Limitations and possible next steps

This project currently:

- Supports CSV input only; it does not read Excel files.
- Uses the fixed filenames `orders.csv` and `order_report.csv`.
- Checks whether required values are blank but does not verify customer or product records.
- Does not validate payment methods against a list of allowed options.
- Reports issues but does not correct orders, calculate sales totals, track inventory, or reconcile deliveries and payments.

Possible future improvements include configurable input and output filenames, additional validation rules, a more detailed report, and support for Excel files. These are not currently implemented.

This project is a learning and portfolio demonstration, not commercial-grade software.
