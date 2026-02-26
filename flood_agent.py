class FloodRiskAgent:

    def __init__(self):
        pass

    def calculate_rainfall_score(self, monthly_rainfall):
        if monthly_rainfall < 200:
            return 0   # Low
        elif 200 <= monthly_rainfall < 350:
            return 1   # Moderate
        elif 350 <= monthly_rainfall < 500:
            return 2   # High
        else:
            return 3   # Disaster

    def calculate_consecutive_score(self, consecutive_days):
        if consecutive_days >= 3:
            return 1
        return 0

    def calculate_anomaly_score(self, forecast, normal):
        anomaly_percent = ((forecast - normal) / normal) * 100
        if anomaly_percent > 25:
            return 1
        return 0

    def predict(self, monthly_rainfall, consecutive_days, normal_rainfall):
        rainfall_score = self.calculate_rainfall_score(monthly_rainfall)
        consecutive_score = self.calculate_consecutive_score(consecutive_days)
        anomaly_score = self.calculate_anomaly_score(monthly_rainfall, normal_rainfall)

        flood_score = (
            0.5 * rainfall_score +
            0.3 * consecutive_score +
            0.2 * anomaly_score
        )

        # Classification
        if flood_score <= 1:
            risk_level = "Low"
        elif flood_score <= 2:
            risk_level = "Moderate"
        elif flood_score <= 3:
            risk_level = "High"
        else:
            risk_level = "Disaster"

        return {
            "flood_score": round(flood_score, 2),
            "risk_level": risk_level
        }
