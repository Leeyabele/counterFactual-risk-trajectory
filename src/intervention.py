# Intervention Module
# This function simulates a clinical intervention applied to deteriorating patients
# after a specified intervention day.

import numpy as np


def apply_intervention(df, intervention_day=45):
    # Create a copy so the original dataset is not modified
    df = df.copy()

    # Select only deteriorating patients on or after the intervention day
    intervention_mask = (
        (df["group"] == "deteriorating") &
        (df["day"] >= intervention_day)
    )

    # Calculate days since intervention for selected rows
    days_since_intervention = df.loc[intervention_mask, "day"] - intervention_day

    # Treatment effect builds gradually over 10 days and is capped at 1
    effect_scale = np.minimum(1, days_since_intervention / 10)

    # Apply intervention effects to physiological variables
    df.loc[intervention_mask, "heart_rate"] -= 1.0 * effect_scale
    df.loc[intervention_mask, "resp_rate"] -= 0.8 * effect_scale
    df.loc[intervention_mask, "oxygen_sat"] += 0.5 * effect_scale

    return df