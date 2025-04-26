import pandas as pd
import numpy as np

# Step 1: Load the dataset
# Assuming the data is saved as 'pakistan_data.csv'
file_path = 'd:\\DAV_LABs\\DAV Project\\education\\f8b9ad6d-dd87-42c9-8e67-25e3a6d19309_Data.csv'  # Replace with your actual file path
df = pd.read_csv(file_path)

# Step 2: Identify non-numeric and numeric columns
# First 4 columns are non-numeric
non_numeric_cols = ['Country Name', 'Country Code', 'Series Name', 'Series Code']
# Numeric columns are the year columns (e.g., "1960 [YR1960]", etc.)
year_cols = [col for col in df.columns if col not in non_numeric_cols]

# Step 3: Function to calculate mean and replace ".." with mean for a row
def replace_missing_with_mean(row):
    # Extract numeric values from year columns, converting ".." to NaN
    numeric_values = pd.to_numeric(row[year_cols], errors='coerce')
    
    # Calculate the mean of non-NaN values
    row_mean = numeric_values.mean()
    
    # Replace NaN (originally "..") with the row mean
    numeric_values.fillna(row_mean, inplace=True)
    
    return numeric_values

# Step 4: Apply the function to each row and update the DataFrame
df[year_cols] = df.apply(replace_missing_with_mean, axis=1)

# Step 5: Save or display the updated DataFrame
# Optionally save to a new CSV file
df.to_csv('d:\\DAV_LABs\\DAV Project\\education\\f8b9ad6d-dd87-42c9-8e67-25e3a6d19309_Data.csv', index=False)

# Display the first few rows to verify
print(df.head())

# Optional: Display summary info
print("\nDataFrame Info:")
print(df.info())