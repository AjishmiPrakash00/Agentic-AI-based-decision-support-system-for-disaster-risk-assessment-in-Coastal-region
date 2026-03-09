import pandas as pd
import sys
import traceback

def explore_cyclone():
    file_path = r"c:\Users\User\Desktop\mini project\data\raw\Cyclone_raw.xlsx"
    try:
        xls = pd.ExcelFile(file_path)
        with open('output.txt', 'w') as f:
            f.write("Sheets: " + str(xls.sheet_names) + "\n")
            
            # Read the first sheet to understand structure
            df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
            f.write("\n--- First 30 rows of sheet 0 ---\n")
            f.write(df.head(30).to_string())
            
            f.write("\n\n--- Second sheet ---\n")
            df2 = pd.read_excel(xls, sheet_name=xls.sheet_names[1])
            f.write(df2.head(30).to_string())
    except Exception as e:
        with open('output.txt', 'w') as f:
            f.write("Error:\n")
            traceback.print_exc(file=f)

if __name__ == '__main__':
    explore_cyclone()
