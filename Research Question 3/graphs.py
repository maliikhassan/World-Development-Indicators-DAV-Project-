import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set Pandas future behavior to avoid warnings
pd.set_option('future.no_silent_downcasting', True)

# Set Seaborn style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12
plt.rcParams['figure.dpi'] = 300

# Load datasets
datasets = {
    'Pakistan': pd.read_csv('/content/Pakistan.csv', skiprows=4),
    'UAE': pd.read_csv('/content/UAE.csv', skiprows=4),
    'UK': pd.read_csv('/content/UK.csv', skiprows=4)
}

# Debug: Print column names and first few rows
for country, df in datasets.items():
    print(f"\nColumns in {country} dataset: {df.columns.tolist()}")
    print(f"First 3 rows of {country} dataset:\n{df.head(3)}")

# Define indicators based on debug output
indicators = {
    'Education': [
        ('School enrollment, primary (% net)', 'SE.PRM.NENR', 'line'),
        ('Government expenditure on education, total (% of GDP)', 'SE.XPD.TOTL.GD.ZS', 'bar')
    ],
    'Finance': [
        ('Account ownership at a financial institution or with a mobile-money-service provider, older adults (% of population ages 25+)', 'FX.OWN.TOTL.OL.ZS', 'area'),
        ('GDP per capita (current US$)', 'NY.GDP.PCAP.CD', 'line')  # Verify if present
    ],
    'Poverty': [
        ('Gini index', 'SI.POV.GINI', 'bar')
    ],
    'Health': [
        ('Current health expenditure (% of GDP)', 'SH.XPD.CHEX.GD.ZS', 'stacked_bar'),
        ('Life expectancy at birth, total (years)', 'SP.DYN.LE00.IN', 'line')
    ],
    'Social Protection and Labour': [
        ('Unemployment, total (% of total labor force) (modeled ILO estimate)', 'SL.UEM.TOTL.ZS', 'line'),
        ('Labor force participation rate, total (% of total population ages 15-64) (modeled ILO estimate)', 'SL.TLF.ACTI.ZS', 'bar')
    ]
}

# Map year columns
year_mapping = {
    '...50': '2011',
    '...53': '2014',
    '...54': '2017',
    '...57': '2021'
}
data_cols = ['...50', '...53', '...54', '...57']
plot_years = ['2011', '2014', '2017', '2021']

# Function to process data
def process_data(df, indicators, data_cols):
    cols = df.columns.tolist()
    try:
        indicator_name_col = cols[2]  # 3rd column
        series_code_col = cols[3]    # 4th column
        selected_cols = [indicator_name_col, series_code_col] + data_cols
        df = df[selected_cols]
        
        indicator_codes = [code for _, code, _ in sum(indicators.values(), [])]
        df = df[df[series_code_col].isin(indicator_codes)]
        
        df[data_cols] = df[data_cols].replace('..', np.nan).astype(float)
        
        for idx, row in df.iterrows():
            mean_val = row[data_cols].mean()
            df.loc[idx, data_cols] = row[data_cols].fillna(mean_val)
        
        return df
    except IndexError:
        print(f"Error: Dataset has fewer than 4 columns: {cols}")
        return pd.DataFrame()

# Process data
processed_data = {}
for country, df in datasets.items():
    processed_data[country] = process_data(df, indicators, data_cols)
    if processed_data[country].empty:
        print(f"Warning: No matching indicators in {country} dataset.")
    else:
        print(f"Processed indicators for {country}: {processed_data[country][processed_data[country].columns[0]].tolist()}")

# Function to plot indicator
def plot_indicator(indicator_name, indicator_code, chart_type, ylabel, filename):
    plotted = False
    plt.figure()
    
    if chart_type == 'line':
        for country, df in processed_data.items():
            if indicator_code in df[df.columns[1]].values:
                data = df[df[df.columns[1]] == indicator_code][data_cols].T
                if not data.empty:
                    data.columns = [country]
                    plt.plot(plot_years, data[country], label=country, marker='o', linewidth=2)
                    plotted = True
    
    elif chart_type == 'bar':
        bar_width = 0.25
        x = np.arange(3)
        for i, country in enumerate(['Pakistan', 'UAE', 'UK']):
            if indicator_code in processed_data[country][processed_data[country].columns[1]].values:
                data = processed_data[country][processed_data[country][processed_data[country].columns[1]] == indicator_code]['...57']
                if not data.empty:
                    plt.bar(x[i], data.iloc[0], bar_width, label=country)
                    plotted = True
        plt.xticks(x, ['Pakistan', 'UAE', 'UK'])
    
    elif chart_type == 'area':
        for country, df in processed_data.items():
            if indicator_code in df[df.columns[1]].values:
                data = df[df[df.columns[1]] == indicator_code][data_cols].T
                if not data.empty:
                    data.columns = [country]
                    plt.fill_between(plot_years, data[country], label=country, alpha=0.4)
                    plotted = True
    
    elif chart_type == 'stacked_bar':
        bar_width = 0.25
        x = np.arange(3, dtype=float)  # Use float to avoid type mismatch
        bottom = np.zeros(3)
        x_offset = 0
        for country in ['Pakistan', 'UAE', 'UK']:
            if indicator_code in processed_data[country][processed_data[country].columns[1]].values:
                data = processed_data[country][processed_data[country][processed_data[country].columns[1]] == indicator_code]['...57']
                if not data.empty:
                    plt.bar(x + x_offset, data.iloc[0], bar_width, bottom=bottom, label=country)
                    bottom += data.iloc[0]
                    x_offset += bar_width
                    plotted = True
        plt.xticks(x + bar_width, ['Pakistan', 'UAE', 'UK'])
    
    if plotted:
        plt.title(f'{indicator_name} (2011–2021)', fontsize=14, pad=15)
        plt.xlabel('Year' if chart_type in ['line', 'area'] else 'Country', fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        if 'GDP per capita' in indicator_name:
            plt.yscale('log')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
        plt.xticks(rotation=45 if chart_type in ['line', 'area'] else 0)
        plt.tight_layout()
        plt.show()
        plt.savefig(f'{filename}.png', bbox_inches='tight')
    else:
        print(f"Skipping plot for {indicator_name}: No data available.")
    plt.close()

# Generate plots
for category, ind_list in indicators.items():
    for indicator_name, indicator_code, chart_type in ind_list:
        ylabel = 'Value (%)'
        if 'GDP per capita' in indicator_name:
            ylabel = 'US$'
        elif 'Gini index' in indicator_name:
            ylabel = 'Gini Coefficient'
        elif 'Life expectancy' in indicator_name:
            ylabel = 'Years'
        plot_indicator(
            indicator_name,
            indicator_code,
            chart_type,
            ylabel,
            f"{category.lower().replace(' ', '_')}_{indicator_name.lower().replace(' ', '_').replace('(', '').replace(')', '').replace(',', '')}"
        )