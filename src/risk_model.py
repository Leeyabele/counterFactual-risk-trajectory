import pandas as pd

def calculate_risk(df):

    # Work on a copy to avoid modifying original dataset 
    df = df.copy()

    # Compute synthetic risk score from physiological variables
    # Higher heart rate and respiratory rate increase risk
    # Lower oxygen saturation increases risk
    # This is a simplified linear model for demonstration purposes

    df["risk"] = (
        (df["heart_rate"] - 80) * 0.05 +
        (df["resp_rate"] - 16) * 0.25 +
        (98 - df["oxygen_sat"]) * 0.60
    )

    return df

