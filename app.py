import pandas as pd
import dash
import numpy as np
from dash import html, dcc, Input, Output
import plotly.graph_objects as go

#-------------------------------------------------------------------------Load the datasets------------------------------------------------------------------------#
df=pd.read_csv('assets/bond_details.csv', sep=',', parse_dates=['Date_of_Purchase'])
#party=pd.read_csv('assets/party_details.csv', sep=',')
df["Denomination"] = df["Denomination"].astype(float)
df['Month_Year'] = df['Date_of_Purchase'].dt.strftime('%b-%Y')

df_party=pd.read_csv('assets/party_details.csv', sep=',', parse_dates=['Date_of_Encashment'])
df_party["Denomination"] = df_party["Denomination"].astype(float)
df_party['Month_Year'] = df_party['Date_of_Encashment'].dt.strftime('%b-%Y')

ele_data=pd.read_csv('assets/Election_dates.csv', sep=',', parse_dates=['Year'])
#ele_data['shifted_date'] = ele_data.Year + pd.Timedelta(days=-35)
specific_dates = ele_data.Year.tolist()

# Convert 'date_of_purchase' to datetime and extract the year
#df['Date_of_Purchase'] = pd.to_datetime(df['date_of_purchase'])
#df['Year'] = df['Date_of_Purchase'].dt.year
#df['Month'] = df['Date_of_Purchase'].dt.month

#---------------------------new detailed dataset-----------------------------#
parties = pd.read_csv('assets/parties.csv', parse_dates=['Date_of_Encashment'])
purchasers = pd.read_csv('assets/purchasers.csv', parse_dates=['Date_of_Purchase'])

df_details = pd.merge(purchasers,parties,how='left',left_on='Bond_number',right_on='Bond_number').dropna(axis=0)
df_details['Month_Year'] = df_details['Date_of_Purchase'].dt.strftime('%b-%Y')

#-----------------------------------------------------------------Define diagrams and Visualizations-------------------------------------------------#
def sankey(table):
    unique = table.iloc[:,0].unique().tolist()+table.iloc[:,1].unique().tolist()
    #unique labels from both the source and target give us the lables for all the nodes
    
    #next we need to map the numbers/index from the unique list to the actual table becuase plotly sankey only takes indexes
    #for SOURCE we map its index from the UNIQUE list
    #for TARGET we map its index from the UNIQUE list
    
    source = []
    for i in range(table.shape[0]-1):
        x = unique.index(table.iloc[:,0].loc[i])
        source.append(x)
        
    target = []
    for j in range(table.shape[0]-1):
        y = unique.index(table.iloc[:,1].loc[j])
        target.append(y)
    
    #Value will be the weights that we give to the links this will be the third column
    value = table.iloc[:,2].values.tolist()
    
    #sankey construction
    node = dict(label = unique, pad=15, thickness=15)
    link = dict(source = source, target = target, value = value)
    sankey = go.Sankey(link = link, node = node, textfont=dict(size=8))
    
    #plot
    fig = go.Figure(sankey)
    fig.update_layout( title_text="Top 100 Bond Buyers and Parties Donated to", font_size=12, width=500, height=800, margin=dict(l=0, r=0, t=50, b=0))
    
    return fig


# Initialize Dash app
app = dash.Dash(__name__)

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

#------------------------------------------------------ App layout ------------------------------------------------------#
app.layout = html.Div([
    html.H1('Electoral Bonds Tracker', style={'text-align': 'center', 'color': 'black', 'font-size': '25px', 'font-weight': 'bold', 'top': '3%'}),
    html.Div([
        html.Div([
            dcc.Graph(id='treemap', style={'width': '50%', 'height': '95%'}),
            dcc.Graph(id='treemap_party', style={'width': '50%', 'height': '95%'})
        ], style={'display': 'flex', 'justify-content': 'space-around', 'width': '70%', 'height': '65%', 'position': 'absolute', 'top': '0', 'left': '0'}),
        html.Div([
            dcc.RangeSlider(
                id='year-slider',
                min=0,
                max=len(df['Month_Year'].unique())-1,
                value=[0,10],
                marks={i: df['Month_Year'].unique()[i] for i in range(len(df['Month_Year'].unique()))},
                step=1,
                allowCross=False),
            dcc.Graph(id='time-series'),       
        ], style={'width': '70%', 'height': '30%', 'position': 'absolute', 'top': '67%', 'left': '0'}),
        html.Div([
            dcc.Graph(id='sankey')    
        ], style={'width': '25%', 'height': '80%', 'position': 'absolute', 'top': '0%', 'left': '72%'})
    ], style={'width': '95%', 'height': '83%', 'position': 'absolute', 'top': '7%', 'left': '2.5%'})
])

#---------------------------Callback to update treemap based on slider input---------------------------#
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
    
    dict_b= filtered_df.groupby("Purchaser_Name")["Denomination"].apply(np.sum).to_dict()
    fig = go.Figure(go.Treemap(
        labels = list(dict_b.keys()),
        parents = [""]*len(dict_b.keys()),   #[""]*len(bonds_tree.keys()
        values = list(dict_b.values()),
        textinfo = "label+value"
    ))
    fig.update_layout( title = 'Purchasers of Bonds by Value', margin = dict(t=30, l=10, r=10, b=0))
    
    return fig

#---------------------------Callback to update treemap_party based on slider input---------------------------#
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
    
    dict_p= filtered_df.groupby("Name_of_Party")["Denomination"].apply(np.sum).to_dict()
    fig = go.Figure(go.Treemap(
        labels = list(dict_p.keys()),
        parents = [""]*len(dict_p.keys()),   #[""]*len(bonds_tree.keys()
        values = list(dict_p.values()),
        textinfo = "label+value" 
    ))
    fig.update_layout( title = "Parties that recieved Bonds by Value", margin = dict(t=30, l=10, r=10, b=0))
    return fig

#--------------------------------Callback to update sankey based on slider input--------------------------------#
@app.callback(
    Output('sankey', 'figure'),
    [Input('year-slider', 'value')]
)
def update_figure(selected_time):
    m_y_start = df_details['Month_Year'].unique()[selected_time[0]]
    m_y_end = df_details['Month_Year'].unique()[selected_time[1]]
    idx_start = df_details.index[df_details['Month_Year'] == m_y_start][0]
    idx_end = df_details.index[df_details['Month_Year'] == m_y_end][-1]

    filtered_df_details= df_details.loc[idx_start : idx_end]
    
    #filtered_df_details = df_details.loc[m_y_start <= df_details['Date_of_Purchase'] <= m_y_end]

    filtered_df_details_groups= filtered_df_details.groupby(["Name_of_Purchaser", "Name_of_Political_Party"])["Denominations_x"].apply(sum).reset_index()

    filtered_df_groups_top100= filtered_df_details_groups.nlargest(100, "Denominations_x").reset_index().drop(columns=["index"])   
    
    return sankey(filtered_df_groups_top100)




#--------------------------------Callback to update timeseries based on slider input--------------------------------#
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

    fil_ele_data = ele_data.loc[(ele_data['Year'] >= m_y_start) & (ele_data['Year'] <= m_y_end)]

    

    df_grouped = filtered_df.groupby(['Date_of_Purchase', 'Denomination']).size().unstack(fill_value=0)

    # Create stacked bar chart
    trace1 = go.Bar(x=df_grouped.index, y=df_grouped[1000], name='1 Thousand')
    trace2 = go.Bar(x=df_grouped.index, y=df_grouped[10000], name='10 Thousand')
    trace3 = go.Bar(x=df_grouped.index, y=df_grouped[100000], name='1 Lakh')
    trace4 = go.Bar(x=df_grouped.index, y=df_grouped[1000000], name='10 Lakh')
    trace5 = go.Bar(x=df_grouped.index, y=df_grouped[10000000], name='1 Crore')

    marker_traces = []
    for date in fil_ele_data['Year']:
        marker_trace = go.Scatter(x=[date], y=[550], mode='lines+markers', marker=dict(color='red', size=10), 
                                  showlegend=False, name=str(fil_ele_data['State'][fil_ele_data['Year'] == date].values), 
                                  hoverinfo='name', hovertemplate='%{name}')
        marker_traces.append(marker_trace)

    data = [trace1, trace2, trace3, trace4, trace5] + marker_traces

    layout = go.Layout(
        #title='Type of Denominations',
        barmode='stack',
        #xaxis=dict(title='Number of Bonds Purchased by their Denominations and Election Results dates'),       
        #yaxis=dict(title='Count'),
        legend=dict(
            x=0.85,
            y=1,
            traceorder='normal',
            bgcolor='rgb(229, 236, 246)'),
        margin=dict(l=0, r=0, t=40, b=10),
        height=300,
        title='Number of Bonds Purchased by their Denominations and Election Results dates', font=dict(size=12),
    )
    
    fig = go.Figure(data=data, layout=layout)
    return fig



# Run app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)