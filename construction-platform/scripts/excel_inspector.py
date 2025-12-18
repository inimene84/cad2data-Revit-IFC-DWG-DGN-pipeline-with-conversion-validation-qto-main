import pandas as pd
import sys
import os

def inspect_excel(file_path):
    """
    Reads an Excel file and prints its column headers and the first 5 rows.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        return

    try:
        print(f"Reading file: {file_path}")
        # Reading only the first 5 rows to get a sample of the data and headers quickly
        df = pd.read_excel(file_path, nrows=5)
        print("\nColumn Headers:")
        print(df.columns.tolist())
        print("\nFirst 5 rows of data:")
        print(df.to_string())
    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python excel_inspector.py <path_to_excel_file>")
        sys.exit(1)
    
    excel_file_path = sys.argv[1]
    inspect_excel(excel_file_path)
