import pandas as pd

file = "Analyses_Rainfall_Nagapattinam_Lat10p77_Lon79p84 (2).xls"

# Read all sheets
sheets = pd.read_excel(file, sheet_name=None)

# Convert each sheet to CSV
for sheet_name, df in sheets.items():
    df.to_csv(f"{sheet_name}.csv", index=False)

print("All sheets converted to CSV")