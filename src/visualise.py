import matplotlib.pyplot as plt


# Plot stable vs deteriorating patient risk trajectories
def plot_stable_vs_deteriorating(df, experiment_size):
    plt.figure()

    stable_patients = df[df["group"] == "stable"]["patient_id"].unique()[:2]
    deteriorating_patients = df[df["group"] == "deteriorating"]["patient_id"].unique()[:2]

    for pid in stable_patients:
        patient = df[df["patient_id"] == pid]
        plt.plot(patient["day"], patient["risk"], color="blue", alpha=0.7)

    for pid in deteriorating_patients:
        patient = df[df["patient_id"] == pid]
        plt.plot(patient["day"], patient["risk"], color="orange", alpha=0.7)

    plt.plot([], [], color="blue", label="Stable")
    plt.plot([], [], color="orange", label="Deteriorating")

    plt.xlabel("Day")
    plt.ylabel("Risk Score")
    plt.title("Stable vs Deteriorating")
    plt.xticks(range(0, 91, 5))
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"outputs/stable_vs_deteriorating_{experiment_size}.png")
    plt.close()


# Plot no intervention versus standard intervention for one patient
def plot_no_intervention_vs_standard_intervention(baseline_patient, standard_patient, experiment_size):
    plt.figure()

    plt.plot(
        baseline_patient["day"],
        baseline_patient["risk"],
        label="No Intervention",
        color="red"
    )

    plt.plot(
        standard_patient["day"],
        standard_patient["risk"],
        label="Standard Intervention",
        color="green"
    )

    plt.xlabel("Day")
    plt.ylabel("Risk Score")
    plt.title("No Intervention vs Standard Intervention")
    plt.xticks(range(0, 91, 5))
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"outputs/no_intervention_vs_standard_intervention_{experiment_size}.png")
    plt.close()


# Plot intervention timing comparison for one patient
def plot_intervention_timing_comparison(
    baseline_patient,
    early_patient,
    standard_patient,
    late_patient,
    experiment_size,
):
    plt.figure()

    plt.plot(
        baseline_patient["day"],
        baseline_patient["risk"],
        label="No Intervention",
        color="red"
    )

    plt.plot(
        early_patient["day"],
        early_patient["risk"],
        label="Early (Day 30)",
        color="green"
    )

    plt.plot(
        standard_patient["day"],
        standard_patient["risk"],
        label="Standard (Day 45)",
        color="blue"
    )

    plt.plot(
        late_patient["day"],
        late_patient["risk"],
        label="Late (Day 60)",
        color="orange"
    )

    plt.xlabel("Day")
    plt.ylabel("Risk Score")
    plt.title("Intervention Timing Comparison")
    plt.xticks(range(0, 91, 5))
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"outputs/intervention_timing_comparison_{experiment_size}.png")
    plt.close()


# Plot cumulative risk comparison by scenario
def plot_outcome_by_scenario(results, experiment_size):
    scenarios = list(results.keys())
    values = [results[scenario]["mean"] for scenario in scenarios]
    errors = [results[scenario]["std"] for scenario in scenarios]

    plt.figure()
    plt.bar(
        scenarios,
        values,
        yerr=errors,
        capsize=5,
        color=["red", "green", "blue", "orange"]
    )

    for i, value in enumerate(values):
        plt.text(i, value + 1, f"{value:.1f}", ha="center")

    plt.ylabel("Mean Cumulative Risk")
    plt.title("Outcome by Scenario")
    plt.tight_layout()
    plt.savefig(f"outputs/outcome_by_scenario_{experiment_size}.png")
    plt.close()