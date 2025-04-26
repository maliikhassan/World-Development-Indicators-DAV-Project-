import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = '/content/4f2f6b82-aa5d-429f-80d4-564ae648423d_Data.csv'
data = pd.read_csv(file_path)

# Pick 4 different features by their "Series Name"
selected_features = data['Series Name'].iloc[[0, 3, 4, 5]].values
feature_data = data[data['Series Name'].isin(selected_features)]

# Extract the years from column names
years = [col.split(' ')[0] for col in data.columns if '[YR' in col]
years = list(map(int, years))

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
axs = axs.flatten()

# Plot each feature
for idx, (feature, ax) in enumerate(zip(selected_features, axs)):
    row = feature_data[feature_data['Series Name'] == feature]
    values = row.iloc[0, 4:].values.astype(float)  # Skip first 4 columns
    ax.plot(years, values, marker='o')
    ax.set_title(feature, fontsize=10)
    ax.set_xlabel('Year')
    ax.set_ylabel('Value')
    ax.grid(True)

plt.tight_layout()
plt.show()
