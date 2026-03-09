import pandas as pd

input_file = r'c:\Users\User\Desktop\mini project\Sheet1.csv'
output_file = r'c:\Users\User\Desktop\mini project\Cleaned_Annual_Rainfall.csv'

print(f"Reading {input_file}...")
try:
    df = pd.read_csv(input_file)
    
    # Extract the first two columns which contain the full sequence of years and rainfall
    cleaned_df = df.iloc[:, [0, 1]].copy()
    cleaned_df.columns = ['Year', 'Annual Rainfall (mm)']
    
    # Drop rows where 'Year' is NaN to remove trailing summary rows or empty rows
    cleaned_df = cleaned_df.dropna(subset=['Year'])
    
    # Convert Year to integer formatting
    cleaned_df['Year'] = cleaned_df['Year'].astype(int)
    
    # Save the cleaned dataframe
    cleaned_df.to_csv(output_file, index=False)
    print(f"Cleaned data successfully saved to {output_file}!")
    print(cleaned_df.head(5).to_string(index=False))
except Exception as e:
    print(f"Error: {e}")
