import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go

# Load the dataset
df=pd.read_csv('assets/bond_details.csv', sep=',', parse_dates=['Date_of_Purchase'])
#party=pd.read_csv('assets/party_details.csv', sep=',')
df["Denomination"] = df["Denomination"].astype(float)




# Convert 'date_of_purchase' to datetime and extract the year
#df['Date_of_Purchase'] = pd.to_datetime(df['date_of_purchase'])
df['Year'] = df['Date_of_Purchase'].dt.year
df['Month'] = df['Date_of_Purchase'].dt.month
# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.Slider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    ),
    dcc.Graph(id='treemap')
])

# Callback to update treemap based on slider input
@app.callback(
    Output('treemap', 'figure'),
    [Input('year-slider', 'value')]
)
def update_figure(selected_time):
    filtered_df = df[df['Date_of_Purchase'] == selected_time]
    #bonds_tree= df.groupby("Purchaser_Name")["Denomination"].apply(sum).to_dict()
    fig = go.Figure(go.Treemap(
        labels=filtered_df['Purchaser_Name'],
        values=filtered_df['Denomination'],
        textinfo="label+value+percent root"
    ))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    return fig

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)