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

df_party=pd.read_csv('assets/party_details.csv', sep=',', parse_dates=['Date_of_Encashment'])
df_party["Denomination"] = df_party["Denomination"].astype(float)
df_party['Month_Year'] = df_party['Date_of_Encashment'].dt.strftime('%b-%Y')


# Convert 'date_of_purchase' to datetime and extract the year
#df['Date_of_Purchase'] = pd.to_datetime(df['date_of_purchase'])
#df['Year'] = df['Date_of_Purchase'].dt.year
#df['Month'] = df['Date_of_Purchase'].dt.month
# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.Graph(id='treemap', style={'title': 'Electoral Bonds Bought', 'width': '30 vw', 'height':'45 vh','display': 'inline-block', 'right': '5 vw'}),
    dcc.Graph(id='treemap_party', style={'title': 'Electoral Bonds Encashed by Parties', 'width': '30 vw', 'height':'45 vh', 'display': 'inline-block', 'right': '45 vw'}),
    dcc.RangeSlider(
        id='year-slider',
        min=0,
        max=len(df['Month_Year'].unique())-1,
        value=[0,10],
        marks={i: df['Month_Year'].unique()[i] for i in range(len(df['Month_Year'].unique()))},
        step=1,
        allowCross=False
    ),
    dcc.Graph(id='time-series', style={'title': 'Electoral Bonds Bought Over Time', 'width': '70 vw', 'height':'20 vh', 'right': '0 vw'})    
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

# Callback to update treemap_party based on slider input
@app.callback(
    Output('treemap_party', 'figure'),
    [Input('year-slider', 'value')]
)
def update_figure(selected_time):
    m_y_start = df_party['Month_Year'].unique()[selected_time[0]]
    m_y_end = df_party['Month_Year'].unique()[selected_time[1]]
    idx_start = df_party.index[df_party['Month_Year'] == m_y_start][0]
    idx_end = df_party.index[df_party['Month_Year'] == m_y_end][-1]

    filtered_df = df_party.loc[idx_start : idx_end]
    
    dict_p= filtered_df.groupby("Name_of_Party")["Denomination"].apply(sum).to_dict()
    fig = go.Figure(go.Treemap(
        labels = list(dict_p.keys()),
        parents = [""]*len(dict_p.keys()),   #[""]*len(bonds_tree.keys()
        values = list(dict_p.values()),
        textinfo = "label+value"
    ))
    fig.update_layout( width=700 , height= 700 , margin = dict(t=25, l=25, r=25, b=25))
    return fig

# Callback to update timeseries based on slider input
@app.callback(
    Output('time-series', 'figure'),
    [Input('year-slider', 'value')]
)
def update_figure(selected_time):

    m_y_start = df['Month_Year'].unique()[selected_time[0]]
    m_y_end = df['Month_Year'].unique()[selected_time[1]]
    idx_start = df.index[df['Month_Year'] == m_y_start][0]
    idx_end = df.index[df['Month_Year'] == m_y_end][-1]

    filtered_df = df.loc[idx_start : idx_end]

    df_grouped = filtered_df.groupby(['Date_of_Purchase', 'Denomination']).size().unstack(fill_value=0)

    # Create stacked bar chart
    trace1 = go.Bar(x=df_grouped.index, y=df_grouped[1000], name='1 Thousand')
    trace2 = go.Bar(x=df_grouped.index, y=df_grouped[10000], name='10 Thousand')
    trace3 = go.Bar(x=df_grouped.index, y=df_grouped[100000], name='1 Lakh')
    trace4 = go.Bar(x=df_grouped.index, y=df_grouped[1000000], name='10 Lakh')
    trace5 = go.Bar(x=df_grouped.index, y=df_grouped[10000000], name='1 Crore')

    data = [trace1, trace2, trace3, trace4, trace5]

    layout = go.Layout(
        title='Type of Denominations',
        barmode='stack',
        xaxis=dict(title='Time'),       
        yaxis=dict(title='Count'),
        legend=dict(
            x=0.9,
            y=1,
            traceorder='normal',
            bgcolor='rgb(229, 236, 246)'
    )
    )

    fig = go.Figure(data=data, layout=layout)
    return fig



# Run app
if __name__ == '__main__':
    app.run_server(debug=True)