import os
import numpy as np

# Set project paths so files are saved to the top level folders
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

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


def run_experiment(experiment_size, n_patients):
    print(f"\nRunning experiment: {experiment_size}")

    # Generate base dataset
    df = generate_dataset(n_patients=n_patients)
    print("dataset generated")

    # Compute baseline risk
    baseline_df = calculate_risk(df)

    # Save base data with experiment label
    save_dataset(
        baseline_df,
        os.path.join(DATA_DIR, f"base_patient_data_{experiment_size}.csv")
    )

    # Run intervention experiments
    early_df, standard_df, late_df = run_timing_experiments(df)

    # Save full scenario data with experiment label
    scenario_df = build_scenario_data(baseline_df, early_df, standard_df, late_df)
    save_dataset(
        scenario_df,
        os.path.join(DATA_DIR, f"scenario_data_{experiment_size}.csv")
    )

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

    # Save summary metrics with experiment label
    results_df = results_to_dataframe(results)
    results_df.to_csv(
        os.path.join(OUTPUT_DIR, f"summary_metrics_{experiment_size}.csv"),
        index=False
    )

    # Save plots with experiment label
    plot_stable_vs_deteriorating(baseline_df, experiment_size)
    plot_no_intervention_vs_standard_intervention(
        baseline_patient,
        standard_patient,
        experiment_size
    )
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
        if scenario == "PAR":
            print(
                f"{scenario}: "
                f"mean={metrics['mean']:.2f}, "
                f"std={metrics['std']:.2f}"
            )
        else:
            print(
                f"{scenario}: "
                f"mean={metrics['mean']:.2f}, "
                f"std={metrics['std']:.2f}, "
                f"reduction_vs_no_intervention={metrics['pct_reduction_vs_no_intervention']:.2f}%"
            )


def main():
    print("inside main")

    # Create output folders at the top level of the project
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Define all experiment sizes
    experiment_sizes = {
        "50": 50,
        "50k": 50000,
        "100k": 100000,
    }

    # Run all experiments
    for experiment_size, n_patients in experiment_sizes.items():
        run_experiment(experiment_size, n_patients)


if __name__ == "__main__":
    main()