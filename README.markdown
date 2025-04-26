# Pakistan WDI Data Analysis and Visualization

## Project Overview
This project conducts a comprehensive **data analysis and visualization** of **World Development Indicators (WDI)** for Pakistan, sourced from the World Bank. It covers categories including **health**, **education**, **poverty**, **finance**, **social protection**, and **labor**. The pipeline cleans raw WDI datasets, extracts statistical features (mean, median, mode, variance, covariance, correlation), detects outliers using box plots, and generates visualizations to uncover trends, relationships, and anomalies in Pakistan's development metrics.

The goal is to provide actionable insights for researchers, policymakers, and stakeholders by summarizing Pakistan's socio-economic trends and enabling cross-category comparisons.

---

## Features
- **Data Cleaning**: Handles missing values ("..") by imputing row-wise means and removes metadata rows.
- **Feature Extraction**: Computes statistical metrics (mean, median, mode, variance, covariance, correlation) for each indicator relative to a category-specific reference indicator.
- **Outlier Detection**: Uses box plots to identify anomalies in statistical features.
- **Visualizations**: Generates time-series plots, bar charts, and correlation heatmaps to visualize trends and relationships.
- **Scalability**: Modular scripts applicable to multiple WDI categories.

---

## Prerequisites
To run this project, ensure you have the following installed:
- **Python 3.8+**
- **Libraries** (install via `pip`):
  ```bash
  pip install pandas numpy matplotlib seaborn
  ```
- **WDI Datasets**: Download CSV files from the [World Bank WDI database](https://databank.worldbank.org/source/world-development-indicators) for Pakistan, covering desired categories.

---

## Project Structure
```
pakistan-wdi-analysis/
│
├── data/
│   ├── health/
│   │   └── 4f2f6b82-aa5d-429f-80d4-564ae648423d_Data.csv
│   ├── education/
│   ├── poverty/
│   ├── finance/
│   ├── social_protection/
│   └── labor/
│
├── scripts/
│   ├── clean_data.py               # Script for data cleaning
│   ├── compute_stats.py            # Script for statistical feature extraction
│   └── visualize.py                # Script for visualizations and outlier detection
│
├── outputs/
│   ├── health_stats.csv            # Statistical results for health
│   ├── health_Mean_boxplot.png     # Box plot for mean (health)
│   ├── uhc_trend.png               # Time-series plot for UHC index
│   └── ...                         # Other category outputs
│
├── README.md                       # Project documentation
└── requirements.txt                # Python dependencies
```

---

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/pakistan-wdi-analysis.git
   cd pakistan-wdi-analysis
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare Data**:
   - Place WDI CSV files in the respective category folders under `data/` (e.g., `data/health/`).
   - Update file paths in `scripts/clean_data.py` and `scripts/compute_stats.py` to match your local setup.

4. **Run Scripts**:
   - Clean data:
     ```bash
     python scripts/clean_data.py
     ```
   - Compute statistics:
     ```bash
     python scripts/compute_stats.py
     ```
   - Generate visualizations:
     ```bash
     python scripts/visualize.py
     ```

---

## Usage
### 1. Data Cleaning (`clean_data.py`)
- **Input**: Raw WDI CSV files (e.g., `data/health/4f2f6b82-aa5d-429f-80d4-564ae648423d_Data.csv`).
- **Process**:
  - Identifies non-numeric (`Country Name`, `Series Name`, etc.) and numeric (year) columns.
  - Replaces `".."` with `NaN` and imputes `NaN` with row-wise means.
  - Removes metadata rows and saves cleaned data.
- **Output**: Cleaned CSV (overwrites input or saves to `outputs/`).

### 2. Statistical Analysis (`compute_stats.py`)
- **Input**: Cleaned WDI CSV files.
- **Process**:
  - Computes mean, median, mode, variance, covariance, and correlation for each indicator.
  - Uses a reference indicator per category (e.g., `SH.UHC.SRVS.CV.XD` for health) for covariance/correlation.
- **Output**: CSV with statistical features (e.g., `outputs/health_stats.csv`).

### 3. Visualization and Outlier Detection (`visualize.py`)
- **Input**: Statistical results (e.g., `health_stats.csv`).
- **Process**:
  - Generates box plots for outlier detection (mean, variance, etc.).
  - Creates time-series plots for key indicators and correlation heatmaps.
- **Output**: PNG files (e.g., `outputs/health_Mean_boxplot.png`, `outputs/uhc_trend.png`).

### Example Command
To process the health category:
```bash
python scripts/clean_data.py --category health
python scripts/compute_stats.py --category health
python scripts/visualize.py --category health
```

---

## Scripts Details
Below are the key scripts and their functionality:

### `clean_data.py`
```python
import pandas as pd
import numpy as np

file_path = 'data/health/4f2f6b82-aa5d-429f-80d4-564ae648423d_Data.csv'
df = pd.read_csv(file_path)
non_numeric_cols = ['Country Name', 'Country Code', 'Series Name', 'Series Code']
year_cols = [col for col in df.columns if col not in non_numeric_cols]

def replace_missing_with_mean(row):
    numeric_values = pd.to_numeric(row[year_cols], errors='coerce')
    row_mean = numeric_values.mean()
    numeric_values.fillna(row_mean, inplace=True)
    return numeric_values

df[year_cols] = df.apply(replace_missing_with_mean, axis=1)
df.to_csv('outputs/health_cleaned.csv', index=False)
```

### `compute_stats.py`
```python
import pandas as pd
import numpy as np

df = pd.read_csv('outputs/health_cleaned.csv')
non_numeric_cols = ['Country Name', 'Country Code', 'Series Name', 'Series Code']
year_cols = [col for col in df.columns if col not in non_numeric_cols]
df[year_cols] = df[year_cols].apply(pd.to_numeric, errors='coerce')

reference_indicator = 'SH.UHC.SRVS.CV.XD'
reference_series = df[df['Series Code'] == reference_indicator][year_cols].iloc[0]

def compute_row_stats(row, reference_series):
    values = pd.to_numeric(row[year_cols], errors='coerce')
    values_clean = values[~np.isnan(values)]
    if len(values_clean) == 0:
        return {'Mean': np.nan, 'Median': np.nan, 'Mode': np.nan, 'Variance': np.nan, 'Covariance': np.nan, 'Correlation': np.nan}
    mean_val = np.mean(values_clean)
    median_val = np.median(values_clean)
    mode_val = pd.Series(values_clean).mode().iloc[0] if not pd.Series(values_clean).mode().empty else np.nan
    variance_val = np.var(values_clean, ddof=1) if len(values_clean) > 1 else 0
    paired_data = pd.DataFrame({'current': values, 'reference': reference_series}).dropna()
    covariance_val = np.cov(paired_data['current'], paired_data['reference'], ddof=1)[0, 1] if len(paired_data) >= 2 else np.nan
    correlation_val = np.corrcoef(paired_data['current'], paired_data['reference'])[0, 1] if len(paired_data) >= 2 else np.nan
    return {'Mean': mean_val, 'Median': median_val, 'Mode': mode_val, 'Variance': variance_val, 'Covariance': covariance_val, 'Correlation': correlation_val}

stats_list = [compute_row_stats(row, reference_series) | {'Factor Name': row['Series Name']} for _, row in df.iterrows()]
stats_df = pd.DataFrame(stats_list)
stats_df.to_csv('outputs/health_stats.csv', index=False)
```

### `visualize.py`
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

stats_df = pd.read_csv('outputs/health_stats.csv')
for col in ['Mean', 'Median', 'Variance', 'Covariance', 'Correlation']:
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=stats_df[col].dropna())
    plt.title(f'Box Plot for {col} (Health - Pakistan)')
    plt.savefig(f'outputs/health_{col}_boxplot.png')
    plt.close()

df = pd.read_csv('outputs/health_cleaned.csv')
indicator = df[df['Series Code'] == 'SH.UHC.SRVS.CV.XD']
year_cols = [col for col in df.columns if col not in ['Country Name', 'Country Code', 'Series Name', 'Series Code']]
plt.figure(figsize=(10, 6))
plt.plot(year_cols, indicator[year_cols].iloc[0], marker='o')
plt.title('UHC Service Coverage Index (Pakistan, 1960-2023)')
plt.xlabel('Year')
plt.ylabel('Index Value')
plt.savefig('outputs/uhc_trend.png')
plt.close()
```

---

## Outputs
- **Cleaned Data**: `outputs/<category>_cleaned.csv`
- **Statistical Results**: `outputs/<category>_stats.csv`
- **Visualizations**:
  - Box plots: `outputs/<category>_<stat>_boxplot.png`
  - Time-series plots: `outputs/<indicator>_trend.png`
  - Correlation heatmaps (if implemented): `outputs/<category>_correlation.png`

---

## Extending to Other Categories
To analyze additional categories (education, poverty, etc.):
1. Place WDI CSV files in `data/<category>/`.
2. Update `file_path` and `reference_indicator` in scripts.
3. Run scripts with the respective category flag:
   ```bash
   python scripts/clean_data.py --category education
   ```

---

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact
For questions or suggestions, contact [your-email@example.com] or open an issue on GitHub.