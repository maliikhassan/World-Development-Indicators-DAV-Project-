import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
df = pd.read_csv('social_protection_labor.csv')

# Select year columns
year_columns = [col for col in df.columns if '[YR' in col]

# Select data and set index
data = df.iloc[:, 2:].set_index('Series Name')[year_columns].T

# Convert data to numeric, coercing non-numeric values to NaN
data = data.apply(pd.to_numeric, errors='coerce')

# Drop columns (indicators) with all NaN values or too few data points
data = data.dropna(axis=1, how='all')  # Drop columns that are entirely NaN
data = data.loc[:, data.notna().sum() >= 2]  # Keep columns with at least 2 non-NaN values

# Calculate the correlation matrix
corr_matrix = data.corr()

# Create a mask to hide NaN values in the heatmap
mask = np.isnan(corr_matrix)

# Create a larger heatmap
plt.figure(figsize=(50, 46))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', mask=mask)
plt.title('Correlation Matrix of Financial Indicators (1960-2023)')
plt.show()

# Identify and print significant correlations
significant_correlations = (corr_matrix.abs() > 0.7) & (corr_matrix != 1.0)
significant_pairs = significant_correlations.stack()[significant_correlations.stack()]
print("Significant Correlations (|corr| > 0.7):")
print(significant_pairs)