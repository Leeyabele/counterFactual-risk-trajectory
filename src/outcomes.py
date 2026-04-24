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

    deteriorating_ids = baseline_df[
        baseline_df["group"].astype(str).str.strip().str.lower() == "deteriorating"
    ]["patient_id"].unique()

    baseline_totals = []
    early_totals = []
    standard_totals = []
    late_totals = []

    for pid in deteriorating_ids:
        baseline_patient = baseline_df[baseline_df["patient_id"] == pid]
        early_patient = early_df[early_df["patient_id"] == pid]
        standard_patient = standard_df[standard_df["patient_id"] == pid]
        late_patient = late_df[late_df["patient_id"] == pid]

        baseline_totals.append(calculate_cumulative_risk(baseline_patient))
        early_totals.append(calculate_cumulative_risk(early_patient))
        standard_totals.append(calculate_cumulative_risk(standard_patient))
        late_totals.append(calculate_cumulative_risk(late_patient))

    results = {
        "No Intervention": {
            "mean": np.mean(baseline_totals),
            "std": np.std(baseline_totals),
            "pct_reduction_vs_no_intervention": 0.0,
        },
        "Early": {
            "mean": np.mean(early_totals),
            "std": np.std(early_totals),
        },
        "Standard": {
            "mean": np.mean(standard_totals),
            "std": np.std(standard_totals),
        },
        "Late": {
            "mean": np.mean(late_totals),
            "std": np.std(late_totals),
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