import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "..", "data", "raw", "flood_training_data.csv")
    model_dir = os.path.join(script_dir, "..", "..", "src", "models")
    
    # Load training data
    df = pd.read_csv(data_path)

    # Features
    X = df[[
        "Predicted_Rainfall",
        "Rainfall_Anomaly",
        "Consecutive_Rainy_Days",
        "Dry_Spell_Duration"
    ]]

    # Target
    y = df["Flood_Risk"]

    # Convert labels to numbers (High, Moderate, Low -> 0, 1, 2)
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42
    )

    # Create model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    # Train model
    model.fit(X_train, y_train)

    # Save model
    model_path = os.path.join(model_dir, "flood_model.pkl")
    encoder_path = os.path.join(model_dir, "label_encoder.pkl")
    
    joblib.dump(model, model_path)
    joblib.dump(encoder, encoder_path)

    print("Flood Risk ML Model trained successfully!")
    print(f"Saved to {model_path}")

if __name__ == "__main__":
    main()
