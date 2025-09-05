test
# csv_processor.py
# A script to read, analyze, and summarize CSV files from the command line.

import argparse
import pandas as pd
import numpy as np
import os
import sys

def analyze_csv(filepath, delimiter):
    """
    Reads a CSV file and performs a comprehensive analysis.

    Args:
        filepath (str): The path to the CSV file.
        delimiter (str): The delimiter used in the CSV file (e.g., ',', ';').

    Returns:
        pd.DataFrame: A DataFrame containing the analysis results, or None if an error occurs.
    """
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(filepath, sep=delimiter)
        
        # --- Basic Information ---
        print(f"\n--- Analysis for: {os.path.basename(filepath)} ---")
        print(f"File path: {filepath}")
        print(f"Delimiter: '{delimiter}'")
        print(f"Total rows: {len(df)}")
        print(f"Total columns: {len(df.columns)}")
        print("\n--- Column Details & Data Types ---")
        print(df.info())

        # --- Statistics and Unique Values ---
        summary_data = []
        numeric_columns = df.select_dtypes(include=np.number).columns
        text_columns = df.select_dtypes(include='object').columns
        
        # Numeric columns
        if not numeric_columns.empty:
            print("\n--- Numeric Column Statistics ---")
            for col in numeric_columns:
                mean_val = df[col].mean()
                min_val = df[col].min()
                max_val = df[col].max()
                
                print(f"Column '{col}':")
                print(f"  - Mean: {mean_val:.2f}")
                print(f"  - Min: {min_val}")
                print(f"  - Max: {max_val}")
                
                summary_data.append({
                    'Column': col,
                    'Type': 'Numeric',
                    'Mean': mean_val,
                    'Min': min_val,
                    'Max': max_val,
                    'Unique Values': 'N/A',
                    'Missing Values': df[col].isnull().sum()
                })
        
        # Text/Categorical columns
        if not text_columns.empty:
            print("\n--- Text Column Unique Values ---")
            for col in text_columns:
                unique_count = df[col].nunique()
                print(f"Column '{col}':")
                print(f"  - Unique values count: {unique_count}")

                summary_data.append({
                    'Column': col,
                    'Type': 'Text',
                    'Mean': 'N/A',
                    'Min': 'N/A',
                    'Max': 'N/A',
                    'Unique Values': unique_count,
                    'Missing Values': df[col].isnull().sum()
                })

        # --- Missing Values Detection ---
        print("\n--- Missing Values Report ---")
        missing_values_count = df.isnull().sum()
        if missing_values_count.sum() > 0:
            print("Detected missing values:")
            print(missing_values_count[missing_values_count > 0].to_string())
        else:
            print("No missing values detected.")
            
        return pd.DataFrame(summary_data)

    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None
    except pd.errors.ParserError:
        print(f"Error: Could not parse '{filepath}'. Check the file format and delimiter.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="CSV File Processor and Analyzer")
    parser.add_argument("filepath", type=str, help="Path to the CSV file to process.")
    parser.add_argument("-d", "--delimiter", type=str, default=",",
                        help="The delimiter used in the CSV file (e.g., ',', ';'). Default is a comma.")
    parser.add_argument("-o", "--output", type=str,
                        help="Optional output path for a summary CSV file.")

    args = parser.parse_args()

    # Perform the analysis and get the summary DataFrame
    summary_df = analyze_csv(args.filepath, args.delimiter)

    # Export summary to a new CSV if specified
    if args.output and summary_df is not None:
        try:
            summary_df.to_csv(args.output, index=False)
            print(f"\nSummary successfully exported to '{args.output}'")
        except Exception as e:
            print(f"Error: Could not write summary to '{args.output}': {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
