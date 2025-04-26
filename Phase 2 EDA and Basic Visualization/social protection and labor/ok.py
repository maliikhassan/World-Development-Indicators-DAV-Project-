import pandas as pd

# Load the CSV file
file_path = "/content/31297f3f-115b-4e5a-b80c-e4218ffbe53e_Data.csv"
data = pd.read_csv(file_path)

# Display the first few rows to understand the structure
data.head()

import matplotlib.pyplot as plt

# Filter data for a specific year
year = "2020 [YR2020]"

# Select a few interesting indicators manually (based on their names)
selected_indicators = [
    "Adequacy of social insurance programs (% of total welfare of beneficiary households)",
    "Adequacy of social protection and labor programs (% of total welfare of beneficiary households)",
    "Average working hours of children, study and work, ages 7-14 (hours per week)"
]

# Filter the DataFrame to only include selected indicators
filtered_data = data[data["Series Name"].isin(selected_indicators)]

# Plot
plt.figure(figsize=(10, 6))

for index, row in filtered_data.iterrows():
    plt.scatter(row["Series Name"], row[year], label=row["Series Name"], s=100)

plt.title(f"Selected Indicators for Pakistan in {year.split()[0]}", fontsize=14)
plt.xlabel("Indicator", fontsize=12)
plt.ylabel("Value", fontsize=12)
plt.xticks(rotation=15, ha="right")
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

import pandas as pd

# Load the CSV file
file_path = "/content/31297f3f-115b-4e5a-b80c-e4218ffbe53e_Data.csv"
data = pd.read_csv(file_path)

# Display the first few rows to understand the structure
data.head()

import matplotlib.pyplot as plt

# Filter data for a specific year
year = "2020 [YR2020]"

# Select a few interesting indicators manually (based on their names)
selected_indicators = [
    "Adequacy of social insurance programs (% of total welfare of beneficiary households)",
    "Adequacy of social protection and labor programs (% of total welfare of beneficiary households)",
    "Average working hours of children, study and work, ages 7-14 (hours per week)"
]

# Filter the DataFrame to only include selected indicators
filtered_data = data[data["Series Name"].isin(selected_indicators)]

# Plot
plt.figure(figsize=(10, 6))

for index, row in filtered_data.iterrows():
    plt.scatter(row["Series Name"], row[year], label=row["Series Name"], s=100)

plt.title(f"Selected Indicators for Pakistan in {year.split()[0]}", fontsize=14)
plt.xlabel("Indicator", fontsize=12)
plt.ylabel("Value", fontsize=12)
plt.xticks(rotation=15, ha="right")
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

