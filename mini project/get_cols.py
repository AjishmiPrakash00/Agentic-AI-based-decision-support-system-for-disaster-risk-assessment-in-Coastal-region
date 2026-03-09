import pandas as pd
import json

def get_cols():
    file_path = r"c:\Users\User\Desktop\mini project\data\raw\Cyclone_raw.xlsx"
    xls = pd.ExcelFile(file_path)
    col_dict = {}
    for s in xls.sheet_names:
        if str(s) >= '2017':
            df = pd.read_excel(xls, sheet_name=s)
            col_dict[str(s)] = df.columns.tolist()
            
    with open('cols.json', 'w') as f:
        json.dump(col_dict, f, indent=2)

if __name__ == '__main__':
    get_cols()
