import pandas as pd

def check_sheets():
    file_path = r"c:\Users\User\Desktop\mini project\data\raw\Cyclone_raw.xlsx"
    xls = pd.ExcelFile(file_path)
    
    for s in xls.sheet_names:
        if str(s) >= '2016':
            try:
                df = pd.read_excel(xls, sheet_name=s)
                cols = df.columns.tolist()
                print(f"Sheet {s} cols: {cols}")
                
            except Exception as e:
                print(f"Error on {s}: {e}")

if __name__ == '__main__':
    check_sheets()
