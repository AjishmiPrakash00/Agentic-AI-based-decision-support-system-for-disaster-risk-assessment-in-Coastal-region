import pandas as pd

input_file = r'c:\Users\User\Desktop\mini project\Max-Rainfall_Per_Year_With_Dat.csv'
output_file = r'c:\Users\User\Desktop\mini project\Cleaned_Max_Rainfall_Per_Year.csv'

print(f"Reading {input_file}...")
try:
    df = pd.read_csv(input_file)
    
    # Extract only the first three relevant columns
    cleaned_df = df[['Date', 'Rainfall (mm)', 'Year']].copy()
    
    # Drop rows where 'Date' or 'Year' might be NaN
    cleaned_df = cleaned_df.dropna(subset=['Date', 'Year'])
    
    # Convert Year to integer formatting
    cleaned_df['Year'] = cleaned_df['Year'].astype(int)
    
    # Save the cleaned dataframe
    cleaned_df.to_csv(output_file, index=False)
    print(f"Cleaned data successfully saved to {output_file}!")
    print(cleaned_df.head(5).to_string(index=False))
except Exception as e:
    print(f"Error: {e}")
