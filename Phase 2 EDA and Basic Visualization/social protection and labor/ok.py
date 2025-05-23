import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

# Read the CSV file
df = pd.read_csv('/content/31297f3f-115b-4e5a-b80c-e4218ffbe53e_Data.csv')

# Define the indicators to visualize
indicators = [
    'Adequacy of social safety net programs (% of total welfare of beneficiary households)',
    'Children in employment, total (% of children ages 7-14)',
    'Unemployment, total (% of total labor force) (national estimate)',
    'Vulnerable employment, total (% of total employment) (modeled ILO estimate)'
]

# Filter data for selected indicators
df_filtered = df[df['Series Name'].isin(indicators)]

# Select columns for years 2000–2023
year_columns = [f'{year} [YR{year}]' for year in range(2000, 2024)]
data_dict = {'year': list(range(2000, 2024))}

# Process data for each indicator
for indicator in indicators:
    indicator_data = df_filtered[df_filtered['Series Name'] == indicator][year_columns].iloc[0]
    # Convert to numeric, handling non-numeric values
    values = pd.to_numeric(indicator_data, errors='coerce').values
    data_dict[indicator] = values

# Create a DataFrame for plotting
plot_df = pd.DataFrame(data_dict)

# Create subplots: 2 rows, 2 columns
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        'Adequacy of Social Safety Nets',
        'Children in Employment (Ages 7-14)',
        'Total Unemployment (National Estimate)',
        'Vulnerable Employment'
    ),
    vertical_spacing=0.15,
    horizontal_spacing=0.1
)

# Plot 1: Line plot for adequacy of social safety net programs
fig.add_trace(
    go.Scatter(
        x=plot_df['year'],
        y=plot_df['Adequacy of social safety net programs (% of total welfare of beneficiary households)'],
        name='Social Safety Net Adequacy',
        line=dict(color='blue', width=2),
        mode='lines+markers'
    ),
    row=1, col=1
)

# Plot 2: Area plot for children in employment
fig.add_trace(
    go.Scatter(
        x=plot_df['year'],
        y=plot_df['Children in employment, total (% of children ages 7-14)'],
        name='Child Employment',
        fill='tozeroy',
        line=dict(color='green', width=2),
        mode='lines+markers'
    ),
    row=1, col=2
)

# Plot 3: Bar plot for total unemployment
fig.add_trace(
    go.Bar(
        x=plot_df['year'],
        y=plot_df['Unemployment, total (% of total labor force) (national estimate)'],
        name='Total Unemployment',
        marker_color='purple'
    ),
    row=2, col=1
)

# Plot 4: Line plot for vulnerable employment
fig.add_trace(
    go.Scatter(
        x=plot_df['year'],
        y=plot_df['Vulnerable employment, total (% of total employment) (modeled ILO estimate)'],
        name='Vulnerable Employment',
        line=dict(color='gold', width=2),
        mode='lines+markers'
    ),
    row=2, col=2
)

# Update layout for better styling
fig.update_layout(
    title=dict(
        text='Pakistan Social Protection and Labor Indicators (2000–2023)',
        x=0.5,
        xanchor='center',
        font=dict(size=24, color='black')
    ),
    showlegend=True,
    legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5),
    height=800,
    width=1000,
    template='plotly_white',
    margin=dict(l=50, r=50, t=100, b=100)
)

# Update axes labels
fig.update_xaxes(title_text='Year', row=1, col=1)
fig.update_yaxes(title_text='% of Welfare', row=1, col=1)
fig.update_xaxes(title_text='Year', row=1, col=2)
fig.update_yaxes(title_text='% of Children', row=1, col=2)
fig.update_xaxes(title_text='Year', row=2, col=1)
fig.update_yaxes(title_text='% of Labor Force', row=2, col=1)
fig.update_xaxes(title_text='Year', row=2, col=2)
fig.update_yaxes(title_text='% of Employment', row=2, col=2)

# Save the plot as an HTML file
pio.write_html(fig, file='pakistan_social_labor_visualization.html', auto_open=True)

print("Visualization saved as 'pakistan_social_labor_visualization.html'")