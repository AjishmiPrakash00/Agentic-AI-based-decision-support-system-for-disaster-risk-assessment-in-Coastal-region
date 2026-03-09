import os
import pandas as pd
import joblib

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(script_dir, "..", "models")
    input_file = os.path.join(script_dir, "..", "..", "data", "processed", "rainfall_forecast_features.csv")
    output_file = os.path.join(script_dir, "..", "..", "data", "processed", "flood_risk_output.csv")
    
    try:
        # Load trained ML model and encoder
        model = joblib.load(os.path.join(model_dir, "flood_model.pkl"))
        encoder = joblib.load(os.path.join(model_dir, "label_encoder.pkl"))
    except FileNotFoundError:
        print("Error: Model files not found. Please run flood_risk_model.py first.")
        return

    try:
        # Load forecast data features
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}. Please run rainfall_forecast_model.py first.")
        return

    features = df[[
        "Predicted_Rainfall",
        "Rainfall_Anomaly",
        "Consecutive_Rainy_Days",
        "Dry_Spell_Duration"
    ]]

    # Predict flood risk using ML model
    predictions = model.predict(features)
    
    # Predict probabilities
    probabilities = model.predict_proba(features)

    # Convert numeric prediction back to labels (High, Moderate, Low)
    df["Flood_Risk"] = encoder.inverse_transform(predictions)
    
    # Get highest probability and convert to percentage
    df["Flood_Probability"] = (probabilities.max(axis=1) * 100).round(2)

    # Print Results
    print("\n--- AI Flood Risk Results (RandomForest Model) ---")
    print(df.to_string(index=False))

    # Save output for the Decision Agent
    df.to_csv(output_file, index=False)
    print(f"\nSaved ML flood prediction to {output_file}")

if __name__ == "__main__":
    main()
