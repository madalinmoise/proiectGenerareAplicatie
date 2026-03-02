import pandas as pd
import os

data_file = "temp_uploads/fisier_excel.xlsx"
try:
    xl = pd.ExcelFile(data_file)
    print(f"Sheets: {xl.sheet_names}")
    df = pd.read_excel(data_file, sheet_name=0)
    print(f"Rows: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"First 2 rows:\n{df.head(2)}")
except Exception as e:
    print(f"Error: {e}")
