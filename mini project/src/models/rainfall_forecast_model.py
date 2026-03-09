import pandas as pd
from prophet import Prophet
import os

def main():
    print("Loading data...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "..", "data", "processed", "Monthly Rainfall.csv")
    df = pd.read_csv(data_path)
    
    # Drop rows where 'Year' is missing or just the Annual summary row
    df = df.dropna(subset=['Year'])
    
    # The columns are Year, Jan, Feb, ..., Dec, Annual
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    print("Converting wide monthly format to long format...")
    # Melt the dataframe from wide to long format
    df_long = df.melt(id_vars=['Year'], value_vars=months, var_name='Month_Str', value_name='Rainfall')
    
    # Map month strings to numbers
    month_map = {m: i+1 for i, m in enumerate(months)}
    df_long['Month_Num'] = df_long['Month_Str'].map(month_map)
    
    # Create ds (datetime) column
    df_long['Year'] = df_long['Year'].astype(int)
    df_long['ds'] = pd.to_datetime(df_long['Year'].astype(str) + '-' + df_long['Month_Num'].astype(str) + '-01')
    
    # Sort chronologically
    df_long = df_long.sort_values('ds').reset_index(drop=True)

    monthly = df_long[['ds', 'Rainfall']].copy()
    monthly.columns = ["ds", "y"]
    monthly = monthly.dropna()

 
    print("Training Prophet model...")
    model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    model.fit(monthly)


    print("Predicting future rainfall...")
    future = model.make_future_dataframe(periods=3, freq='MS')
    forecast = model.predict(future)


    next_3_months = forecast[['ds', 'yhat']].tail(3).copy()
    next_3_months['Month'] = next_3_months['ds'].dt.strftime('%Y-%m')
    next_3_months['Predicted_Rainfall'] = next_3_months['yhat'].round(0).astype(int)
    
    # Generate Synthetic Features for ML model (Normally you calculate this from actual recent data)
    # We add dummy variations based on rainfall amount
    next_3_months['Rainfall_Anomaly'] = next_3_months['Predicted_Rainfall'] - 60 # Assume 60 is normal
    next_3_months['Consecutive_Rainy_Days'] = (next_3_months['Predicted_Rainfall'] / 20).astype(int)
    next_3_months['Dry_Spell_Duration'] = (10 - next_3_months['Consecutive_Rainy_Days']).clip(lower=0)
    
    # Save to CSV for the ML Flood Agent (Using the new wide feature format)
    output_path = os.path.join(script_dir, "..", "..", "data", "processed", "rainfall_forecast_features.csv")
    cols_to_save = ['Month', 'Predicted_Rainfall', 'Rainfall_Anomaly', 'Consecutive_Rainy_Days', 'Dry_Spell_Duration']
    next_3_months[cols_to_save].to_csv(output_path, index=False)
    print(f"\nSaved ML forecast features to {output_path}")

if __name__ == "__main__":
    main()
