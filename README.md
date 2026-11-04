# E-commerce Order Checker

I built this Python tool to check e-commerce order data for common errors, including missing information, duplicate order IDs, and invalid quantities. It reads CSV files and generates a report that can be opened in Excel.

## Business problem

An order spreadsheet can contain missing details, repeated order IDs, or incorrect quantities. This tool lists those problems so someone can review them before processing the orders.

## Implemented features

- Reads `orders.csv` from the terminal's current folder.
- Checks for missing required columns.
- Reports blank required fields, including values omitted from incomplete rows.
- Checks that quantities are positive whole numbers.
- Detects repeated, non-empty order IDs.
- Reads UTF-8 CSV files with or without a byte-order mark (BOM).
- Writes the findings to `order_report.csv` and prints them in the terminal.

## Technologies

The project uses Python 3 and its standard library.

- `csv` reads and writes the order files.
- `unittest` runs the automated tests.
- `tempfile` and `pathlib` help create temporary test files.

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

The checker prints its findings and saves `order_report.csv` in the terminal's current folder. A successful save replaces the previous report.

If the input file is missing, the checker warns that an existing report may be from an earlier run. If saving fails, it still prints the findings and warns that the CSV report may be incomplete.

## Run the automated tests

From the project folder, run:

```text
python -m unittest -v
```

On Windows, if `python` is not recognized, try:

```text
py -m unittest -v
```

The nine tests cover valid orders, duplicate IDs, missing values and columns, invalid quantities, incomplete rows, a missing input file, and UTF-8 BOM support.

Each test uses temporary fictional data. The temporary files are removed after the test finishes.

## Input CSV format

The input file must be named `orders.csv` and include these column names:

```csv
order_id,customer_name,product,quantity,payment_method
EG2001,Mona,Scarf,2,Cash
```

Each data row represents one order. All five fields need a value. The quantity must be a positive whole number, such as `1` or `12`.

## Generated report

The report has one column named `Problem`, with one issue per row. For example:

```csv
Problem
Row 3: duplicate order ID EG2001
Row 4: invalid quantity '0' (must be a positive whole number)
```

Row numbers count the CSV header as row 1.

If the checker finds no problems, the report contains only the `Problem` header.

## Example demonstration

The `examples` folder contains fictional orders with four deliberate errors.

From the project folder, run these commands in PowerShell:

```powershell
cd examples
python ..\order_checker.py
```

This reads `examples/orders.csv` and saves `examples/order_report.csv`. The report lists four problems:

- A duplicate order ID
- A missing customer name
- An invalid quantity (`abc`)
- A missing order ID

You can open the generated CSV report in Microsoft Excel to review the findings.

## Limitations and possible next steps

The checker uses fixed filenames and supports CSV input only. It checks required values but does not verify customer or product records, or check payment methods against an allowed list.

It reports problems for manual review. Order correction, sales calculations, inventory tracking, and payment reconciliation are outside its current scope.

Possible next steps include choosing input and output filenames, adding validation rules, and supporting Excel files.
