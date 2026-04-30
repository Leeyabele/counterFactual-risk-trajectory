import os
import numpy as np

np.random.seed(42)

from generate_data import generate_dataset, save_dataset
from risk_model import calculate_risk
from experiments import run_timing_experiments, build_scenario_data
from outcomes import compare_all_patients, results_to_dataframe
from visualise import (
    plot_stable_vs_deteriorating,
    plot_no_intervention_vs_standard_intervention,
    plot_intervention_timing_comparison,
    plot_outcome_by_scenario,
)


def main():
    print("inside main")

    # Label this run so output files are saved separately
    experiment_size = "100k"

    os.makedirs("data", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    # Generate base dataset
    df = generate_dataset()
    print("dataset generated")

    # Compute baseline risk
    baseline_df = calculate_risk(df)

    # Save base data
    save_dataset(baseline_df, "data/base_patient_data.csv")

    # Run experiments
    early_df, standard_df, late_df = run_timing_experiments(df)

    # Save full scenario data
    scenario_df = build_scenario_data(baseline_df, early_df, standard_df, late_df)
    save_dataset(scenario_df, "data/scenario_data.csv")

    print("\nUnique group values:")
    print(baseline_df["group"].unique())

    print("\nGroup counts:")
    print(baseline_df["group"].value_counts())

    deteriorating_patients = baseline_df[
        baseline_df["group"].astype(str).str.strip().str.lower() == "deteriorating"
    ]["patient_id"].unique()

    print("\nDeteriorating patient IDs found:")
    print(deteriorating_patients)

    if len(deteriorating_patients) == 0:
        raise ValueError("No deteriorating patients found in baseline_df")

    # Select one deteriorating patient for illustrative plots
    patient_id = deteriorating_patients[0]

    baseline_patient = baseline_df[baseline_df["patient_id"] == patient_id]
    early_patient = early_df[early_df["patient_id"] == patient_id]
    standard_patient = standard_df[standard_df["patient_id"] == patient_id]
    late_patient = late_df[late_df["patient_id"] == patient_id]

    # Compare outcomes across all deteriorating patients
    results = compare_all_patients(
        baseline_df,
        early_df,
        standard_df,
        late_df,
    )

    # Save summary metrics
    results_df = results_to_dataframe(results)
    results_df.to_csv(f"outputs/summary_metrics_{experiment_size}.csv", index=False)

    # Save plots
    plot_stable_vs_deteriorating(baseline_df, experiment_size)
    plot_no_intervention_vs_standard_intervention(baseline_patient, standard_patient, experiment_size)
    plot_intervention_timing_comparison(
        baseline_patient,
        early_patient,
        standard_patient,
        late_patient,
        experiment_size,
    )
    plot_outcome_by_scenario(results, experiment_size)

    print("\n--- Cumulative Risk Comparison ---")
    for scenario, metrics in results.items():
        print(
            f"{scenario}: "
            f"mean={metrics['mean']:.2f}, "
            f"std={metrics['std']:.2f}, "
            f"reduction_vs_no_intervention={metrics['pct_reduction_vs_no_intervention']:.2f}%"
        )


if __name__ == "__main__":
    main()