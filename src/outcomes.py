import numpy as np
import pandas as pd


# Calculate cumulative harmful risk over time
# Only positive risk contributes to burden
def calculate_cumulative_risk(patient_df):
    return patient_df["risk"].clip(lower=0).sum()


# Compare cumulative risk across scenarios for one patient
def compare_scenarios(baseline_patient, early_patient, standard_patient, late_patient):
    results = {
        "No Intervention": calculate_cumulative_risk(baseline_patient),
        "Early": calculate_cumulative_risk(early_patient),
        "Standard": calculate_cumulative_risk(standard_patient),
        "Late": calculate_cumulative_risk(late_patient),
    }

    return results


# Compare scenarios across all deteriorating patients
def compare_all_patients(baseline_df, early_df, standard_df, late_df):
    # Keep deteriorating patients only
    baseline_det = baseline_df[
        baseline_df["group"].astype(str).str.strip().str.lower() == "deteriorating"
    ].copy()

    early_det = early_df[
        early_df["group"].astype(str).str.strip().str.lower() == "deteriorating"
    ].copy()

    standard_det = standard_df[
        standard_df["group"].astype(str).str.strip().str.lower() == "deteriorating"
    ].copy()

    late_det = late_df[
        late_df["group"].astype(str).str.strip().str.lower() == "deteriorating"
    ].copy()

    # Only positive risk contributes to cumulative burden
    baseline_det["positive_risk"] = baseline_det["risk"].clip(lower=0)
    early_det["positive_risk"] = early_det["risk"].clip(lower=0)
    standard_det["positive_risk"] = standard_det["risk"].clip(lower=0)
    late_det["positive_risk"] = late_det["risk"].clip(lower=0)

    # Sum risk per patient using groupby instead of looping patient by patient
    baseline_totals = baseline_det.groupby("patient_id")["positive_risk"].sum()
    early_totals = early_det.groupby("patient_id")["positive_risk"].sum()
    standard_totals = standard_det.groupby("patient_id")["positive_risk"].sum()
    late_totals = late_det.groupby("patient_id")["positive_risk"].sum()

    # Calculate Preventability Adjusted Risk per patient
    # PAR shows the proportion of cumulative risk reduced by early intervention
    par_values = (baseline_totals - early_totals) / baseline_totals

    # Replace invalid values caused by division by zero
    par_values = par_values.replace([np.inf, -np.inf], np.nan).dropna()

    results = {
        "No Intervention": {
            "mean": baseline_totals.mean(),
            "std": baseline_totals.std(),
            "pct_reduction_vs_no_intervention": 0.0,
        },
        "Early": {
            "mean": early_totals.mean(),
            "std": early_totals.std(),
        },
        "Standard": {
            "mean": standard_totals.mean(),
            "std": standard_totals.std(),
        },
        "Late": {
            "mean": late_totals.mean(),
            "std": late_totals.std(),
        },
        "PAR": {
            "mean": par_values.mean(),
            "std": par_values.std(),
            "pct_reduction_vs_no_intervention": np.nan,
        },
    }

    baseline_mean = results["No Intervention"]["mean"]

    for scenario in ["Early", "Standard", "Late"]:
        scenario_mean = results[scenario]["mean"]
        pct_reduction = ((baseline_mean - scenario_mean) / baseline_mean) * 100
        results[scenario]["pct_reduction_vs_no_intervention"] = pct_reduction

    return results


# Convert scenario comparison into a dataframe for saving
def results_to_dataframe(results):
    rows = []

    for scenario, metrics in results.items():
        rows.append(
            {
                "scenario": scenario,
                "mean_cumulative_risk": metrics["mean"],
                "std_cumulative_risk": metrics["std"],
                "pct_reduction_vs_no_intervention": metrics["pct_reduction_vs_no_intervention"],
            }
        )

    return pd.DataFrame(rows)