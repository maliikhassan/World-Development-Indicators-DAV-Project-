import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

# Read the CSV file
# Assuming health.csv is in the same directory; adjust the path if needed
df = pd.read_csv('/content/4f2f6b82-aa5d-429f-80d4-564ae648423d_Data.csv')

# Define the indicators to visualize
indicators = [
    'Adolescent fertility rate (births per 1,000 women ages 15-19)',
    'Birth rate, crude (per 1,000 people)',
    'Births attended by skilled health staff (% of total)',
    'Current health expenditure (% of GDP)',
    'Tuberculosis treatment success rate (% of new cases)'
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
        'Fertility and Birth Rates',
        'Births Attended by Skilled Health Staff',
        'Current Health Expenditure (% of GDP)',
        'Tuberculosis Treatment Success Rate'
    ),
    vertical_spacing=0.15,
    horizontal_spacing=0.1
)

# Plot 1: Line plot for fertility and birth rates
fig.add_trace(
    go.Scatter(
        x=plot_df['year'],
        y=plot_df['Adolescent fertility rate (births per 1,000 women ages 15-19)'],
        name='Adolescent Fertility Rate',
        line=dict(color='blue', width=2),
        mode='lines+markers'
    ),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(
        x=plot_df['year'],
        y=plot_df['Birth rate, crude (per 1,000 people)'],
        name='Crude Birth Rate',
        line=dict(color='orange', width=2),
        mode='lines+markers'
    ),
    row=1, col=1
)

# Plot 2: Area plot for births attended by skilled health staff
fig.add_trace(
    go.Scatter(
        x=plot_df['year'],
        y=plot_df['Births attended by skilled health staff (% of total)'],
        name='Skilled Birth Attendance',
        fill='tozeroy',
        line=dict(color='green', width=2),
        mode='lines+markers'
    ),
    row=1, col=2
)

# Plot 3: Bar plot for health expenditure
fig.add_trace(
    go.Bar(
        x=plot_df['year'],
        y=plot_df['Current health expenditure (% of GDP)'],
        name='Health Expenditure',
        marker_color='purple'
    ),
    row=2, col=1
)

# Plot 4: Line plot for TB treatment success rate
fig.add_trace(
    go.Scatter(
        x=plot_df['year'],
        y=plot_df['Tuberculosis treatment success rate (% of new cases)'],
        name='TB Treatment Success',
        line=dict(color='gold', width=2),
        mode='lines+markers'
    ),
    row=2, col=2
)

# Update layout for better styling
fig.update_layout(
    title=dict(
        text='Pakistan Health Indicators (2000–2023)',
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
fig.update_yaxes(title_text='Rate (per 1,000)', row=1, col=1)
fig.update_xaxes(title_text='Year', row=1, col=2)
fig.update_yaxes(title_text='Percentage (%)', row=1, col=2)
fig.update_xaxes(title_text='Year', row=2, col=1)
fig.update_yaxes(title_text='% of GDP', row=2, col=1)
fig.update_xaxes(title_text='Year', row=2, col=2)
fig.update_yaxes(title_text='Success Rate (%)', row=2, col=2)

# Save the plot as an HTML file
pio.write_html(fig, file='pakistan_health_visualization.html', auto_open=True)

print("Visualization saved as 'pakistan_health_visualization.html'")