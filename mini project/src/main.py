import os
import pandas as pd
import sys

# Add the src folder to Python path so we can import our modules
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

from models.rainfall_forecast_model import main as run_rainfall_model
from agents.flood_agent import main as run_flood_agent
from agents.decision_agent import main as run_decision_agent
from agents.alert_agent import send_alert

def main():
    print("\nRunning Rainfall Forecast Model")
    run_rainfall_model()
    
    print("\nRunning Flood Risk Agent ---")
    run_flood_agent()
    
    print("\nStep 3: Running Decision Agent")
    run_decision_agent()
    
    print("\nStep 4: Running Alert Agent\n")
    decision_file = os.path.join(script_dir, "..", "data", "processed", "decision_output.csv")
    
    try:
        df = pd.read_csv(decision_file)
        
        alerts_sent = 0
        for index, row in df.iterrows():
            if row['Decision'] == 'SEND_ALERT':
                send_alert(row['Month'], row['Predicted_Rainfall'], row['Flood_Risk'])
                alerts_sent += 1
                
        if alerts_sent == 0:
            print("No action required. All predicted months are at a safe risk level.")
            
    except FileNotFoundError:
        print(f"Error: Could not find {decision_file}. Run the pipeline again.")

if __name__ == "__main__":
    main()
