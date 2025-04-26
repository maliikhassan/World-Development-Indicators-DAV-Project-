import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = '/content/70e8aabb-b542-4bcc-b874-fccfdff1114b_Data.csv'
data = pd.read_csv(file_path)

# Drop the unnecessary 'Unnamed: 0' column if it exists
if 'Unnamed: 0' in data.columns:
    data = data.drop(columns=['Unnamed: 0'])

# Clean year columns
years = [col.split(' ')[0] for col in data.columns if '[YR' in col]
years = list(map(int, years))

# Select a few features to plot (first 5)
selected_features = data['Series Name'].iloc[0:5]
feature_data = data.iloc[0:5, data.columns.get_loc('1960 [YR1960]'):]

# Plot
plt.figure(figsize=(14, 8))
for idx, feature in enumerate(selected_features):
    values = feature_data.iloc[idx].astype(float)
    plt.plot(years, values, label=feature)

plt.title('Multiple Features Over Years')
plt.xlabel('Year')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()
