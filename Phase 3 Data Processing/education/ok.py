import pandas as pd
import numpy as np
import os

# Step 1: Load the data
file_path = 'D:\\DAV_LABs\\DAV Project\\PreProcessing_M_M_M_V_C_C\\education\\f8b9ad6d-dd87-42c9-8e67-25e3a6d19309_Data.csv'
try:
    df = pd.read_csv(file_path)
    print("Data loaded successfully.")
    print(f"Dataset shape (before cleaning): {df.shape}")
except FileNotFoundError:
    print(f"File not found: {file_path}")
    print("Files in directory:", os.listdir('D:\\DAV_LABs\\DAV Project\\PreProcessing_M_M_M_V_C_C\\education\\'))
    raise

# Step 2: Clean the dataset (remove empty rows and metadata)
# Remove rows where 'Series Name' is NaN or contains metadata
df = df[df['Series Name'].notna()]
df = df[~df['Series Name'].str.contains('Data from database|Last Updated', na=False)]
print(f"Dataset shape (after cleaning): {df.shape}")

# Step 3: Identify non-numeric and numeric columns
non_numeric_cols = ['Country Name', 'Country Code', 'Series Name', 'Series Code']
year_cols = [col for col in df.columns if col not in non_numeric_cols]
print(f"Year columns identified: {year_cols[:5]}... (total: {len(year_cols)})")

# Step 4: Convert year columns to numeric, handling missing values
df[year_cols] = df[year_cols].replace(['..', ''], np.nan)
df[year_cols] = df[year_cols].apply(pd.to_numeric, errors='coerce')

# Step 5: Select the reference indicator for covariance and correlation
reference_indicator = 'SE.PRM.TENR'  # Adjusted net enrollment rate, primary, which exists in this dataset
reference_series = df[df['Series Code'] == reference_indicator][year_cols].iloc[0]
if reference_series.empty:
    print("Reference indicator not found in the dataset!")
    raise ValueError(f"Reference indicator {reference_indicator} not found.")

# Step 6: Function to compute statistics for a row
def compute_row_stats(row, reference_series):
    # Extract the 64 numeric values for the row (1960–2023)
    values = row[year_cols].values
    # Ensure values are numeric
    values = pd.to_numeric(values, errors='coerce')
    # Drop NaN values for computation
    values_clean = values[~np.isnan(values)]
    
    # If all values are NaN, return empty results
    if len(values_clean) == 0:
        return {
            'Mean': np.nan,
            'Median': np.nan,
            'Mode': np.nan,
            'Variance': np.nan,
            'Covariance': np.nan,
            'Correlation': np.nan
        }
    
    # Compute mean, median, variance
    mean_val = np.mean(values_clean)
    median_val = np.median(values_clean)
    variance_val = np.var(values_clean, ddof=1) if len(values_clean) > 1 else 0  # Sample variance
    
    # Compute mode using pandas.Series.mode()
    values_series = pd.Series(values_clean)
    mode_val = values_series.mode().iloc[0] if not values_series.mode().empty else np.nan
    
    # Compute covariance and correlation with the reference series
    paired_data = pd.DataFrame({
        'current': values,
        'reference': reference_series
    }).dropna()
    
    if len(paired_data) < 2:  # Need at least 2 pairs for covariance/correlation
        covariance_val = np.nan
        correlation_val = np.nan
    else:
        covariance_val = np.cov(paired_data['current'], paired_data['reference'], ddof=1)[0, 1]
        correlation_val = np.corrcoef(paired_data['current'], paired_data['reference'])[0, 1]
    
    return {
        'Mean': mean_val,
        'Median': median_val,
        'Mode': mode_val,
        'Variance': variance_val,
        'Covariance': covariance_val,
        'Correlation': correlation_val
    }

# Step 7: Process each row and collect results
stats_list = []
for idx, row in df.iterrows():
    factor_name = row['Series Name']
    print(f"Processing row {idx + 1}/{len(df)}: {factor_name}")
    stats = compute_row_stats(row, reference_series)
    stats['Factor Name'] = factor_name
    stats_list.append(stats)

# Step 8: Create a DataFrame with the results
stats_df = pd.DataFrame(stats_list, columns=[
    'Factor Name', 'Mean', 'Median', 'Mode', 'Variance', 'Covariance', 'Correlation'
])

# Step 9: Save the results to a CSV file
output_file = 'education_stats.csv'
try:
    stats_df.to_csv(output_file, index=False, na_rep='')
    print(f"Statistics saved as {output_file}")
except PermissionError as e:
    print(f"Permission denied: {e}")
    fallback_path = os.path.join(os.path.expanduser('~'), 'Desktop', output_file)
    try:
        stats_df.to_csv(fallback_path, index=False, na_rep='')
        print(f"Data saved to fallback location: {fallback_path}")
    except Exception as e2:
        print(f"Failed to save to fallback location: {e2}")

# Step 10: Display the first few rows of the results
print("\nFirst few rows of the computed statistics:")
print(stats_df.head())