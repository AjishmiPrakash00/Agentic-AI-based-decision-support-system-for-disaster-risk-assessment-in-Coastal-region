import pandas as pd
import json
import codecs

def dump_columns():
    file_path = r"c:\Users\User\Desktop\mini project\data\raw\Cyclone_raw.xlsx"
    xls = pd.ExcelFile(file_path)
    
    col_dict = {}
    for s in xls.sheet_names:
        if str(s) >= '2017':
            try:
                df = pd.read_excel(xls, sheet_name=s)
                col_dict[str(s)] = df.columns.tolist()
            except Exception as e:
                col_dict[str(s)] = f"Error: {e}"
                
    with codecs.open("cols_2017_2025.json", "w", encoding="utf-8") as f:
        json.dump(col_dict, f, indent=2)

if __name__ == '__main__':
    dump_columns()
