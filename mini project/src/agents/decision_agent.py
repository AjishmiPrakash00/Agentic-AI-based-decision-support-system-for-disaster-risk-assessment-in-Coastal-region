import pandas as pd
import os

from google import genai
import time

def decision_logic(row):
    risk = row['Flood_Risk']
    probability = row['Flood_Probability']
    rainfall = row['Predicted_Rainfall']
    
    # Securely retrieve API key from environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY environment variable not found. Falling back to static rules.")
        if risk == "High" and probability > 70: return "SEND_ALERT"
        elif risk == "High" or risk == "Moderate": return "GENERATE_REPORT"
        else: return "LOG_STATUS"

    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are an expert Emergency Response AI Manager for a city. Analyze the following monthly forecast:
        - Predicted Rainfall: {rainfall} mm
        - Machine Learning Risk Assessment: {risk}
        - AI Confidence Probability: {probability}%
        
        Given this data, you must autonomously decide the single best course of action.
        You may only output EXACTLY ONE of the following precise string codes (do not output anything else, no markdown):
        1. SEND_ALERT
        2. GENERATE_REPORT
        3. MONITOR_CLOSELY
        4. LOG_STATUS
        """
        
        # Adding a small delay to avoid hitting free-tier API rate limits
        time.sleep(1)
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        decision = response.text.strip()
        
        # Validate that the LLM returned one of our allowed codes
        valid_codes = ["SEND_ALERT", "GENERATE_REPORT", "MONITOR_CLOSELY", "LOG_STATUS"]
        if decision in valid_codes:
            return decision
        else:
            print(f"Agentic System returned invalid code '{decision}', falling back to GENERATE_REPORT")
            return "GENERATE_REPORT"

    except Exception as e:
        print(f"Agentic API Error: {e}. Falling back to static rules.")
        if risk == "High" and probability > 70: return "SEND_ALERT"
        elif risk == "High" or risk == "Moderate": return "GENERATE_REPORT"
        else: return "LOG_STATUS"


def main():
    # Load Flood Risk Output
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "..", "..", "data", "processed", "flood_risk_output.csv")
    
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}. Please run flood_agent.py first.")
        return

    # Apply Decision Logic
    df['Decision'] = df.apply(decision_logic, axis=1)

    # Print Results for Testing
    print("Decision Agent Output")
    print(df.to_string(index=False))

    # Save Decision Output
    output_file = os.path.join(script_dir, "..", "..", "data", "processed", "decision_output.csv")
    df.to_csv(output_file, index=False)
    print(f"\nSaved decision output to {output_file}")

if __name__ == "__main__":
    main()
