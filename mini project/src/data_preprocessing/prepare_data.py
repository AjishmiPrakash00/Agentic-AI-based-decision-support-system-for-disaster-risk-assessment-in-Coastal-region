import pandas as pd
import numpy as np

# Define input and output paths
input_daily = r'c:\Users\User\Desktop\mini project\Daily Rainfall.csv'
output_daily = r'c:\Users\User\Desktop\mini project\Model_Ready_Daily_Data.csv'
output_annual = r'c:\Users\User\Desktop\mini project\Model_Ready_Annual_Data.csv'

print("Loading Daily Rainfall data...")
df = pd.read_csv(input_daily)

# 1. Data Cleaning
# Ensure Date column is in datetime format
df['Date'] = pd.to_datetime(df['YYYY-MM-DD'])
df = df.sort_values('Date').reset_index(drop=True)

# 2. Missing Value Handling
# Check for missing values
missing_count = df['Rainfall (mm)'].isnull().sum()
print(f"Found {missing_count} missing rainfall values.")

# Interpolate missing values or fill with 0. 
# For rainfall, missing values are usually best filled with 0 unless there's an ongoing storm. We'll fill with 0.
df['Rainfall (mm)'] = df['Rainfall (mm)'].fillna(0)

# 3. Feature Engineering
print("Engineering daily features...")

# A. Consecutive Rainy Days
# Define a rainy day as rainfall > 0 mm
df['Is_Rainy'] = df['Rainfall (mm)'] > 0
# Calculate running count of rainy days
# The trick: group by the cumulative sum of non-rainy days
df['Consecutive_Rainy_Days'] = df['Is_Rainy'].groupby((~df['Is_Rainy']).cumsum()).cumsum()

# B. Dry Spell Duration
# Define a dry day as rainfall == 0 mm
df['Is_Dry'] = df['Rainfall (mm)'] == 0
df['Dry_Spell_Duration'] = df['Is_Dry'].groupby((~df['Is_Dry']).cumsum()).cumsum()

# C. Rainfall Anomaly (Daily)
# Let's calculate the long-term mean for each specific day of the year (e.g., average rainfall on Jan 1st across all years)
df['DayOfYear'] = df['Date'].dt.dayofyear
daily_climatological_mean = df.groupby('DayOfYear')['Rainfall (mm)'].transform('mean')
df['Daily_Rainfall_Anomaly'] = df['Rainfall (mm)'] - daily_climatological_mean

# Cleanup temporary columns
df = df.drop(columns=['YYYY-MM-DD', 'Is_Rainy', 'Is_Dry', 'DayOfYear'])

# Make Date the first column
cols = ['Date'] + [col for col in df.columns if col != 'Date']
df = df[cols]

# Save daily model-ready data
print(f"Saving daily data to {output_daily}...")
df.to_csv(output_daily, index=False)

# 4. Create Annual Dataset
# Often models predict on annual aggregates, so we'll build that too
print("Engineering annual features...")
annual_df = df.groupby(df['Date'].dt.year).agg(
    Total_Rainfall=('Rainfall (mm)', 'sum'),
    Max_Daily_Rainfall=('Rainfall (mm)', 'max'),
    Max_Consecutive_Rainy_Days=('Consecutive_Rainy_Days', 'max'),
    Max_Dry_Spell_Duration=('Dry_Spell_Duration', 'max')
).reset_index()
annual_df.rename(columns={'Date': 'Year'}, inplace=True)

# Rainfall Anomaly (Annual)
long_term_annual_mean = annual_df['Total_Rainfall'].mean()
annual_df['Annual_Rainfall_Anomaly'] = annual_df['Total_Rainfall'] - long_term_annual_mean

# Save annual model-ready data
print(f"Saving annual data to {output_annual}...")
annual_df.to_csv(output_annual, index=False)

print("\n--- Data Preparation Complete ---")
print("\nDaily Data Snippet:")
print(df.head())
print("\nAnnual Data Snippet:")
print(annual_df.head())
