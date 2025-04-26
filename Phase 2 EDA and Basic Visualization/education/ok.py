import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
csv_file = "/content/f8b9ad6d-dd87-42c9-8e67-25e3a6d19309_Data.csv"  # Update path if necessary
df = pd.read_csv(csv_file)

# Filter for the desired indicators
indicators = ['SE.PRM.TENR', 'SE.PRM.TENR.FE', 'SE.PRM.TENR.MA']
df_filtered = df[df['Series Code'].isin(indicators)]

# Select columns for years 2002–2023
year_columns = [f"{year} [YR{year}]" for year in range(2002, 2024)]
data_columns = ['Series Name'] + year_columns
df_filtered = df_filtered[data_columns]

# Clean and prepare data
# Convert year columns to numeric, handling any non-numeric values
for col in year_columns:
    df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce')

# Transpose data for plotting
df_transposed = df_filtered.set_index('Series Name')[year_columns].T
df_transposed.index = [int(col.split()[0]) for col in df_transposed.index]  # Extract year as integer

# Rename columns for clarity
df_transposed.columns = [
    'Total Enrollment',
    'Female Enrollment',
    'Male Enrollment'
]

# Create the time series line chart
plt.figure(figsize=(10, 6))
for column in df_transposed.columns:
    plt.plot(df_transposed.index, df_transposed[column], marker='o', label=column)

# Customize the plot
plt.title('Primary School Adjusted Net Enrollment Rate in Pakistan (2002–2023)', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Enrollment Rate (%)', fontsize=12)
plt.legend()
plt.grid(True)
plt.xticks(df_transposed.index, rotation=45)
plt.tight_layout()

# Show the plot
plt.show()