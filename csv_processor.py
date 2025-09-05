"""
csv_processor.py

A command-line tool for analyzing and summarizing CSV files.

Features:
1. Reads CSV files and shows basic information (rows, columns).
2. Calculates statistics for numeric columns (mean, min, max, etc.).
3. Shows the count of unique values for text-based columns.
4. Detects and reports missing values per column.
5. Can export the summary to a new CSV file.
6. Handles different CSV formats by allowing delimiter specification.

Usage:
python csv_processor.py <path_to_file.csv> [--delimiter <char>] [--output <output_path.csv>]

Example:
python csv_processor.py data.csv --delimiter ';' --output summary.csv
"""

import argparse
import pandas as pd
import numpy as np
import sys

def analyze_csv(filepath: str, delimiter: str, output_path: str = None):
    """
    Analyzes a CSV file, prints a summary, and optionally exports it.

    Args:
        filepath (str): The path to the input CSV file.
        delimiter (str): The delimiter used in the CSV file (e.g., ',', ';').
        output_path (str, optional): The path to save the summary CSV. Defaults to None.
    """
    try:
        # Try to load CSV with UTF-8, fallback to UTF-8-SIG if needed
        try:
            df = pd.read_csv(filepath, delimiter=delimiter, encoding="utf-8")
            print("Successfully loaded the CSV file (UTF-8).")
        except UnicodeDecodeError:
            df = pd.read_csv(filepath, delimiter=delimiter, encoding="utf-8-sig")
            print("Successfully loaded the CSV file (UTF-8 with BOM).")

        # --- 1. Basic Info ---
        rows, cols = df.shape
        print(f"\n--- Basic Information ---")
        print(f"Total Rows: {rows}")
        print(f"Total Columns: {cols}")
        print(f"\nColumn Data Types:")
        print(df.dtypes)

        # Initialize a dictionary to hold the summary data
        summary_data = {
            'Column': [],
            'DataType': [],
            'MissingValues': [],
            'UniqueValues': [],
            'Mean': [],
            'Min': [],
            'Max': [],
        }

        # --- 2. Missing Values Detection ---
        missing_values = df.isnull().sum()
        print(f"\n--- Missing Values Report ---")
        for col, count in missing_values.items():
            print(f"'{col}': {count} missing value(s)")
            summary_data['Column'].append(col)
            summary_data['DataType'].append(str(df[col].dtype))
            summary_data['MissingValues'].append(count)
            summary_data['UniqueValues'].append(df[col].nunique())
            summary_data['Mean'].append(np.nan)
            summary_data['Min'].append(np.nan)
            summary_data['Max'].append(np.nan)
        
        # --- 3. Statistics & Unique Values ---
        print(f"\n--- Column Statistics ---")
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                # Numeric column
                print(f"\nNumeric Column: '{col}'")
                desc = df[col].describe()
                print(f"  Mean: {desc['mean']:.2f}")
                print(f"  Min: {desc['min']:.2f}")
                print(f"  Max: {desc['max']:.2f}")
                
                # Update summary data for numeric columns
                idx = summary_data['Column'].index(col)
                summary_data['Mean'][idx] = desc['mean']
                summary_data['Min'][idx] = desc['min']
                summary_data['Max'][idx] = desc['max']
            else:
                # Non-numeric (text/object) column
                print(f"\nText Column: '{col}'")
                unique_count = df[col].nunique()
                print(f"  Unique Values Count: {unique_count}")

        # --- 4. Export Summary ---
        if output_path:
            summary_df = pd.DataFrame(summary_data)
            try:
                summary_df.to_csv(output_path, index=False)
                print(f"\n--- Summary Exported ---")
                print(f"Summary report has been saved to '{output_path}'.")
            except IOError as e:
                print(f"Error: Could not save the output file at '{output_path}'.")
                print(f"Details: {e}", file=sys.stderr)

    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def main():
    """
    Main function to parse command-line arguments and run the analysis.
    """
    parser = argparse.ArgumentParser(
        description="A command-line tool for analyzing and summarizing CSV files."
    )
    parser.add_argument(
        'filepath',
        type=str,
        help='The path to the input CSV file.'
    )
    parser.add_argument(
        '--delimiter',
        '-d',
        type=str,
        default=',',
        help='The delimiter character used in the CSV file. Defaults to ",".'
    )
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        help='Optional path to save the summary to a new CSV file.'
    )

    args = parser.parse_args()
    
    # Run the analysis with the provided arguments
    analyze_csv(args.filepath, args.delimiter, args.output)

if __name__ == "__main__":
    main()
