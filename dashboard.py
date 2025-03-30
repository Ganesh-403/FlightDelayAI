# dashboard.py
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset
df = pd.read_csv("data/flight_data.csv")

# Create a 'route' column (combining origin and destination) if not already present
if 'route' not in df.columns:
    df['route'] = df['origin'].astype(str) + "-" + df['destination'].astype(str)

# Ensure 'congestion' and 'delay' are numeric
df["congestion"] = pd.to_numeric(df["congestion"], errors="coerce")
df["delay"] = pd.to_numeric(df["delay"], errors="coerce")

# Set default values for missing columns
if 'weather' not in df.columns:
    df['weather'] = "Clear"
if 'scheduled_time' not in df.columns:
    df['scheduled_time'] = pd.NaT

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Flight Delay Analytics Dashboard"

# Define the layout with four chart containers
app.layout = html.Div([
    html.H1("Flight Delay Analytics Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.H2("Average Delay by Route"),
        dcc.Graph(id='route-delay-chart')
    ], style={"width": "100%", "padding": "20px"}),

    html.Div([
        html.H2("Weather Impact on Delays"),
        dcc.Graph(id='weather-chart')
    ], style={"width": "100%", "padding": "20px"}),

    html.Div([
        html.H2("Airport Congestion vs Delays"),
        dcc.Graph(id='congestion-chart', style={'height': '500px', 'width': '800px'})
    ], style={"width": "100%", "padding": "20px"}),

    html.Div([
        html.H2("Historical Delay Trends"),
        dcc.Graph(id='time-series-chart')
    ], style={"width": "100%", "padding": "20px"}),
])

# Callback to update all charts on page load
@app.callback(
    Output('route-delay-chart', 'figure'),
    Output('weather-chart', 'figure'),
    Output('congestion-chart', 'figure'),
    Output('time-series-chart', 'figure'),
    Input('route-delay-chart', 'id')  # Dummy input to trigger callback on load
)
def update_charts(dummy_input):
    # Chart 1: Average Delay by Route
    try:
        route_df = df.groupby('route', as_index=False)['delay'].mean()
        route_fig = px.bar(
            route_df, x='route', y='delay', 
            title="Average Delay by Route",
            labels={"route": "Route", "delay": "Average Delay (min)"}
        )
    except Exception as e:
        route_fig = px.bar(title=f"Error generating chart: {e}")

    # Chart 2: Weather Impact on Delays
    try:
        weather_fig = px.box(
            df, x='weather', y='delay', 
            title="Delay Distribution by Weather",
            labels={"weather": "Weather Condition", "delay": "Delay (min)"}
        )
    except Exception as e:
        weather_fig = px.box(title=f"Error generating chart: {e}")

    # Chart 3: Airport Congestion vs Delays
    try:
        temp_df = df.dropna(subset=["congestion", "delay"]).copy()
        temp_df["congestion"] = pd.to_numeric(temp_df["congestion"], errors="coerce")
        temp_df["delay"] = pd.to_numeric(temp_df["delay"], errors="coerce")
        print("Filtered Data for Congestion Chart:")
        print(temp_df[["congestion", "delay"]].head())
        
        congestion_fig = px.scatter(
            temp_df, x='congestion', y='delay',
            title="Airport Congestion vs Delays",
            labels={"congestion": "Congestion Level", "delay": "Delay (min)"}
        )
        # Explicitly set marker size and axis ranges for clarity
        congestion_fig.update_traces(marker=dict(size=12, color='rgba(255, 0, 0, 0.7)'))
        congestion_fig.update_layout(height=500, width=800)
        congestion_fig.update_xaxes(range=[0, 10])
        congestion_fig.update_yaxes(range=[0, 50])
    except Exception as e:
        congestion_fig = px.scatter(title=f"Error generating chart: {e}")

    # Chart 4: Historical Delay Trends
    if 'scheduled_time' in df.columns and not df['scheduled_time'].isnull().all():
        try:
            df['scheduled_time'] = pd.to_datetime(df['scheduled_time'], format="%Y-%m-%d %H:%M:%S", errors='coerce', exact=False)
            time_series_df = df.dropna(subset=["scheduled_time"]).sort_values('scheduled_time')
            time_series_fig = px.line(
                time_series_df, x='scheduled_time', y='delay', 
                title="Historical Delay Trends",
                labels={"scheduled_time": "Scheduled Time", "delay": "Delay (min)"}
            )
        except Exception as e:
            time_series_fig = px.line(title=f"Error generating chart: {e}")
    else:
        time_series_fig = px.line(title="No scheduled_time data available.")

    return route_fig, weather_fig, congestion_fig, time_series_fig

# Run the dashboard
if __name__ == '__main__':
    app.run(debug=True)
