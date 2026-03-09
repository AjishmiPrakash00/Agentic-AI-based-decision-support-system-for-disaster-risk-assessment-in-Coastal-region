import pandas as pd
import numpy as np
import os
import re

def process_cyclones():
    file_path = r"c:\Users\User\Desktop\mini project\data\raw\Cyclone_raw.xlsx"
    out_dir = r"c:\Users\User\Desktop\mini project\data\processed"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "cyclone_filtered_new.csv")
    
    print(f"Reading {file_path}...")
    xls = pd.ExcelFile(file_path)
    all_filtered_rows = []
    
    for sheet_name in xls.sheet_names:
        try:
            # Read without assuming header=0, to help find headers pushed down
            df_raw = pd.read_excel(xls, sheet_name=sheet_name, header=None)
        except Exception as e:
            print(f"Error reading sheet {sheet_name}: {e}")
            continue
            
        if df_raw.empty:
            continue
            
        # Find the header row
        header_idx = -1
        for idx, row in df_raw.iterrows():
            row_str = " ".join([str(val).lower() for val in row.values])
            if 'lat' in row_str and 'lon' in row_str:
                header_idx = idx
                break
                
        if header_idx == -1:
            print(f"Sheet {sheet_name}: Could not find Latitude/Longitude header row. Skipping.")
            continue
            
        # Set the columns
        df = df_raw.iloc[header_idx + 1:].copy()
        df.columns = df_raw.iloc[header_idx]
        
        # Standardize columns
        rename_map = {}
        for col in df.columns:
            c = str(col).lower().strip()
            if 'lat' in c and 'Latitude' not in rename_map.values():
                rename_map[col] = 'Latitude'
            elif 'lon' in c and 'Longitude' not in rename_map.values():
                rename_map[col] = 'Longitude'
            elif 'serial' in c and 'Cyclone_ID' not in rename_map.values():
                rename_map[col] = 'Cyclone_ID'
            elif 'date' in c and 'Date' not in rename_map.values():
                rename_map[col] = 'Date'
            elif 'name' in c and 'Name' not in rename_map.values():
                rename_map[col] = 'Name'
            elif 'wind' in c and 'Wind_Speed' not in rename_map.values():
                rename_map[col] = 'Wind_Speed'
            elif ('pressure' in c or 'e.c.p' in c) and 'Pressure' not in rename_map.values():
                if 'drop' not in c:
                    rename_map[col] = 'Pressure'
            elif 'grade' in c:
                rename_map[col] = 'Grade'
        
        df = df.rename(columns=rename_map)
        
        if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
            print(f"Sheet {sheet_name} missing Lat/Lon columns after rename. Skipping.")
            continue
            
        df['Year'] = sheet_name
        
        def clean_coord(val):
            if pd.isna(val):
                return np.nan
            val_str = str(val).upper().strip()
            # extract numeric part
            m = re.search(r'([+\-]?\d+\.?\d*)', val_str)
            if m:
                return float(m.group(1))
            return np.nan

        df['Latitude'] = df['Latitude'].apply(clean_coord)
        df['Longitude'] = df['Longitude'].apply(clean_coord)
        
        if 'Cyclone_ID' in df.columns:
            df['Cyclone_ID'] = pd.to_numeric(df['Cyclone_ID'], errors='coerce')
        else:
            df['Cyclone_ID'] = np.nan
        
        # Drop rows missing coordinates.
        df_clean = df.dropna(subset=['Latitude', 'Longitude'])
        
        # Nagapattinam is approx 10.77 N, 79.84 E.
        # Filter for lat 9-12 and lon 78-82.
        mask = (
            (df_clean['Latitude'] >= 9.0) & (df_clean['Latitude'] <= 12.0) &
            (df_clean['Longitude'] >= 78.0) & (df_clean['Longitude'] <= 82.0)
        )
        
        filtered_points = df_clean[mask]
        
        if not filtered_points.empty:
            # Find all unique Cyclone_IDs in this sheet that passed near Nagapattinam
            valid_ids = filtered_points['Cyclone_ID'].dropna().unique()
            
            # If standard Cyclone_IDs are missing/nan but it's clearly one cyclone, fallback to name or just take the rows
            if len(valid_ids) > 0:
                cyclone_mask = df_clean['Cyclone_ID'].isin(valid_ids)
                cyclone_data = df_clean[cyclone_mask].copy()
            else:
                if 'Name' in filtered_points.columns:
                    valid_names = filtered_points['Name'].dropna().unique()
                    cyclone_mask = df_clean['Name'].isin(valid_names)
                    cyclone_data = df_clean[cyclone_mask].copy()
                else:
                    cyclone_data = filtered_points.copy()
            
            all_filtered_rows.append(cyclone_data)
            
    if all_filtered_rows:
        res_df = pd.concat(all_filtered_rows, ignore_index=True)
        # Select important columns and put them first
        cols_priority = ['Year', 'Cyclone_ID', 'Name', 'Date', 'Latitude', 'Longitude', 'Wind_Speed', 'Pressure', 'Grade']
        existing_priority = [c for c in cols_priority if c in res_df.columns]
        other_cols = [c for c in res_df.columns if c not in existing_priority]
        final_cols = existing_priority + other_cols
        res_df = res_df[final_cols]
        
        res_df.to_csv(out_path, index=False)
        print(f"Successfully processed {file_path}")
        print(f"Saved filtered data to {out_path}")
        print(f"Total rows kept: {len(res_df)}")
        print(f"From {len(all_filtered_rows)} year sheets with relevant cyclones")
        
        # Verify years
        print("Years with cyclones found:", res_df['Year'].unique())
        
    else:
        print("No records found passing near Nagapattinam.")

if __name__ == '__main__':
    process_cyclones()
