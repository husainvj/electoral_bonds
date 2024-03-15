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
df['Month_Year'] = df['Date_of_Purchase'].dt.strftime('%b-%Y')

#unique_dates=df.Month_Year.unique()
#unique_dates


# Convert 'date_of_purchase' to datetime and extract the year
#df['Date_of_Purchase'] = pd.to_datetime(df['date_of_purchase'])
#df['Year'] = df['Date_of_Purchase'].dt.year
#df['Month'] = df['Date_of_Purchase'].dt.month
# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.Graph(id='treemap'),
    dcc.RangeSlider(
        id='year-slider',
        min=0,
        max=len(df['Month_Year'].unique())-1,
        value=[0,10],
        marks={i: df['Month_Year'].unique()[i] for i in range(len(df['Month_Year'].unique()))},
        step=1,
        allowCross=False
    )
    
])

# Callback to update treemap based on slider input
@app.callback(
    Output('treemap', 'figure'),
    [Input('year-slider', 'value')]
)
def update_figure(selected_time):
    
    m_y_start = df['Month_Year'].unique()[selected_time[0]]
    m_y_end = df['Month_Year'].unique()[selected_time[1]]
    idx_start = df.index[df['Month_Year'] == m_y_start][0]
    idx_end = df.index[df['Month_Year'] == m_y_end][-1]

    #filtered_df = df[df['Month_Year'].between(m_y_start, m_y_end)]

    filtered_df = df.loc[idx_start : idx_end]
    
    dict_b= filtered_df.groupby("Purchaser_Name")["Denomination"].apply(sum).to_dict()
    fig = go.Figure(go.Treemap(
        labels = list(dict_b.keys()),
        parents = [""]*len(dict_b.keys()),   #[""]*len(bonds_tree.keys()
        values = list(dict_b.values()),
        textinfo = "label+value"
    ))
    fig.update_layout( width=700 , height= 700 , margin = dict(t=25, l=25, r=25, b=25))
    return fig



# Run app
if __name__ == '__main__':
    app.run_server(debug=True)