import pandas as pd

from intervention import apply_intervention
from risk_model import calculate_risk


# Run intervention timing scenarios
def run_timing_experiments(df):

    # Early intervention
    early_df = apply_intervention(df, intervention_day=30)
    early_df = calculate_risk(early_df)

    # Standard intervention
    standard_df = apply_intervention(df, intervention_day=45)
    standard_df = calculate_risk(standard_df)

    # Late intervention
    late_df = apply_intervention(df, intervention_day=60)
    late_df = calculate_risk(late_df)

    return early_df, standard_df, late_df


# Build full scenario dataset for saving
def build_scenario_data(baseline_df, early_df, standard_df, late_df):

    baseline_copy = baseline_df.copy()
    baseline_copy["scenario"] = "No Intervention"

    early_copy = early_df.copy()
    early_copy["scenario"] = "Early"

    standard_copy = standard_df.copy()
    standard_copy["scenario"] = "Standard"

    late_copy = late_df.copy()
    late_copy["scenario"] = "Late"

    scenario_df = pd.concat(
        [baseline_copy, early_copy, standard_copy, late_copy],
        ignore_index=True
    )

    return scenario_df