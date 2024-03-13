import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.offline as offline
from plotly.subplots import make_subplots
import plotly.subplots as sp
import base64


data= pd.read_csv("assets/bond_details.csv", sep=";")







bonds_tree= data.groupby("name_of_purchaser")['denomination'].apply(sum).to_dict()  # only use it for a combined analysis of all projects



         
fig=go.Figure(go.Treemap(labels= list(bonds_tree.keys()), parents= [""]*len(bonds_tree.keys()), values= list(bonds_tree.values()), text= list(bonds_tree.keys()), marker_colors=px.colors.qualitative.Plotly, textinfo="label+text+value"))    
fig.update_layout(width=750, height=750, margin=dict(l=0, r=0, t=0, b=0))
    


offline.plot(fig, filename="bonds_map.html", auto_open=True)
# We have to add a time slider to the map to show the evolution of the bonds over time.

# We can also add a slider to show the evolution of the bonds over time.
fig.update_layout(sliders=[
    dict(
        active=0,
        currentvalue={"prefix": "Year: "},
        pad={"t": 50},
        steps=[dict(
            label=str(year),
            method="update",
            args=[{"visible": [year == int(data['year']) for year in data['year']]}]
        ) for year in data['year'].unique()]
    )
])
