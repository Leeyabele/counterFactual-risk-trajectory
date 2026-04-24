# Intervention Module
# This function simulates a clinical intervention applied
# to deteriorating patients after a specified day.

# The intervention improves physiological parameters:
# - reduces heart rate
# - reduces respiratory rate
# - increases oxygen saturation

# This represents a simplified model of treatment response.


def apply_intervention(df, intervention_day=45):

    # Create a copy to avoid modifying original dataset
    df = df.copy()

    # Loop through each row (each patient-day observation)
    for i in range(len(df)):

        # Apply intervention only to deteriorating patients
        # and only after the intervention day
        if df.loc[i, "group"] == "deteriorating" and df.loc[i, "day"] >= intervention_day:

            # Calculate how long since intervention started
            days_since_intervention = df.loc[i, "day"] - intervention_day

            # Gradual effect scaling (treatment effect builds over time)
            effect_scale = min(1, days_since_intervention / 10)

            # Apply intervention effects
            # Reduced heart rate → improved cardiovascular stability
            df.loc[i, "heart_rate"] -= 1.0 * effect_scale

            # Reduced respiratory rate → improved respiratory function
            df.loc[i, "resp_rate"] -= 0.8 * effect_scale

            # Increased oxygen saturation → improved oxygenation
            df.loc[i, "oxygen_sat"] += 0.5 * effect_scale

    return df