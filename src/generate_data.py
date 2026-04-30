import numpy as np
import pandas as pd

# Fixed seed for reproducibility
np.random.seed(42)


# Generate a synthetic patient trajectory over time
# Stable patients fluctuate around baseline
# Deteriorating patients show progressive physiological decline
def generate_patient_trajectory(patient_id, days, group):
    data = []

    heart_rate = np.random.normal(75, 5)
    resp_rate = np.random.normal(15, 2)
    oxygen_sat = np.random.normal(98, 1)

    deterioration_factor = np.random.uniform(0.02, 0.06)

    for day in range(days):
        hr_noise = np.random.normal(0, 0.8)
        rr_noise = np.random.normal(0, 0.4)
        ox_noise = np.random.normal(0, 0.2)

        if group == "stable":
            heart_rate += hr_noise
            resp_rate += rr_noise
            oxygen_sat += ox_noise

        elif group == "deteriorating":
            # Simulate gradual deterioration (non-linear progression)
            progression = deterioration_factor * (day / days) ** 2
            heart_rate += progression * 2 + hr_noise
            resp_rate += progression * 2 + rr_noise
            oxygen_sat -= progression * 1.2 + ox_noise

        heart_rate = np.clip(heart_rate, 40, 180)
        resp_rate = np.clip(resp_rate, 8, 40)
        oxygen_sat = np.clip(oxygen_sat, 75, 100)

        data.append({
            "patient_id": patient_id,
            "day": day,
            "heart_rate": heart_rate,
            "resp_rate": resp_rate,
            "oxygen_sat": oxygen_sat,
            "group": group
        })

    return pd.DataFrame(data)


# Generate full dataset with equal split:
# 50% stable, 50% deteriorating patients
def generate_dataset(n_patients=100000, days=90):
    all_data = []

    for i in range(n_patients):
        if i < n_patients / 2:
            group = "stable"
        else:
            group = "deteriorating"

        patient_df = generate_patient_trajectory(
            patient_id=i,
            days=days,
            group=group
        )

        all_data.append(patient_df)

    return pd.concat(all_data, ignore_index=True)


# Save dataset to CSV
def save_dataset(df, filepath):
    df.to_csv(filepath, index=False)