import sys
import csv
import statistics
import argparse
from pathlib import Path

def detect_delimiter(file_path, sample_size=1024):
    """Try to detect delimiter (comma or semicolon)."""
    with open(file_path, "r", encoding="utf-8") as f:
        sample = f.read(sample_size)
        if sample.count(";") > sample.count(","):
            return ";"
        return ","


def analyze_csv(file_path, export_path=None):
    if not Path(file_path).exists():
        print(f"Error: File '{file_path}' not found.")
        return

    delimiter = detect_delimiter(file_path)

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        rows = list(reader)

    if not rows:
        print("The CSV file is empty.")
        return

    columns = reader.fieldnames
    print(f"\nFile: {file_path}")
    print(f"Rows: {len(rows)}")
    print(f"Columns: {len(columns)} -> {columns}\n")

    summary = []
    for col in columns:
        values = [row[col].strip() for row in rows if row[col] is not None]
        missing = sum(1 for v in values if v == "")
        non_empty = [v for v in values if v != ""]

        # Try numeric conversion
        numeric_vals = []
        for v in non_empty:
            try:
                numeric_vals.append(float(v))
            except ValueError:
                pass

        if numeric_vals and len(numeric_vals) == len(non_empty):
            # Pure numeric column
            stats = {
                "column": col,
                "type": "Numeric",
                "count": len(values),
                "missing": missing,
                "unique": len(set(numeric_vals)),
                "min": min(numeric_vals),
                "max": max(numeric_vals),
                "mean": statistics.mean(numeric_vals)
            }
            print(f"{col} (Numeric): min={stats['min']}, max={stats['max']}, mean={stats['mean']:.2f}, "
                  f"missing={missing}")
        else:
            # Text column
            stats = {
                "column": col,
                "type": "Text",
                "count": len(values),
                "missing": missing,
                "unique": len(set(non_empty))
            }
            print(f"{col} (Text): {stats['unique']} unique values, missing={missing}")

        summary.append(stats)

    # Export summary if requested
    if export_path:
        with open(export_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=summary[0].keys())
            writer.writeheader()
            writer.writerows(summary)
        print(f"\nSummary exported to: {export_path}")


def main():
    parser = argparse.ArgumentParser(description="CSV Processor Script")
    parser.add_argument("csv_file", help="Path to CSV file to process")
    parser.add_argument("-o", "--output", help="Export summary to CSV file", default=None)
    args = parser.parse_args()

    try:
        analyze_csv(args.csv_file, args.output)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
