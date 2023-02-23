from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

#read required dataset
df = pd.read_csv("NationalAndStatePregnancy_PublicUse.csv")

#create filter var
state_data=df['state'].unique()
year_data=df['year'].unique()

app = Dash(__name__)

app.css.config.serve_locally = True

#front-end development
app.layout =html.Div([
    
    html.Div([        
        html.Div('Abortion Data Statistics Dashboard', id='header')
    ]),
    
    html.Div([
        dcc.Dropdown(
            id='states', 
            options=[{'label': i,'value': i} for i in state_data],
            value=["State"],
            multi=True,
            searchable=True,
            clearable=True,
            placeholder="Filter by State"
        ),

    dcc.Graph(id="abortion_plot", animate=True),
    ]),
   
])

@app.callback(
    Output("abortion_plot", "figure"), 
    Input("states", "value"))


def display_graph(states):
    filtered_data=df[['year','state','abortionstotal', 'birthstotal', 'pregnancyratetotal', 'birthratetotal',
       'abortionratetotal', 'abortionratiototal', 'miscarriagestotal',
       'pregnanciestotal']]
    #filtered_data=pd.pivot(filtered_data)
    #print(filtered_data)


    #create filter for drop-down interactions
    if states == ['State'] or states==None or states==[]:
        new_data = filtered_data[['year','state','abortionstotal', 'birthstotal', 'pregnancyratetotal', 'birthratetotal',
       'abortionratetotal', 'abortionratiototal', 'miscarriagestotal',
       'pregnanciestotal']]
        
    else:
        new_data=filtered_data.copy()
        new_data = filtered_data.loc[filtered_data['state'].isin(states)]
        #print(new_data)
    
    #plot the graphs
    fig = px.bar(
        data_frame=new_data, x='state', y='abortionratiototal',
        #hover_name='Product Name',
        #text='Product Name',
        #barmode='group',
        template="simple_white",
        hover_data=['pregnanciestotal','abortionratetotal', 'abortionratiototal', 'miscarriagestotal', 'birthratetotal'],
        range_y=(0,15000)
    )

    #set color
    fig.update_traces(marker_color='darkseagreen')

    fig.update_layout(
        hoverlabel=dict(
            bgcolor="antiquewhite",
            font_size=16,
            font_family="Rockwell"
    )
    )
    
    #creating buttons to update graph to different visualization
    fig.update_layout(
    updatemenus=[
        dict(
            type = "buttons",
            direction = "left",
            buttons=list([
                dict(
                    args=["type", "bar"],
                    label="Bar",
                    method="restyle"
                ),
                dict(
                    args=["type", "pie"],
                    label="Pie",
                    method="restyle"
                ),
                dict(
                    args=["type", "box"],
                    label="Box",
                    method="restyle"
                ),
                dict(
                    args=["type", "line"],
                    label="Line",
                    method="restyle"
                ),
                dict(
                    args=["type", "funnel"],
                    label="Funnel",
                    method="restyle"
                ),
                dict(
                    args=["type", "violin"],
                    label="Violin",
                    method="restyle"
                )
            ]),
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.11,
            xanchor="left",
            y=1.1,
            yanchor="top"
        ),
    ]
)

    fig.update_layout(
        font_family="Open Sans",
        legend_title_font_color="green",
        autosize=False,
        width=1400,
        height=500,        
    )

    #create X axis and the grids for X-axis
    fig.update_xaxes(title_text='States')
    fig.update_xaxes(showline=True, linewidth=2, linecolor='Light Grey', mirror=True)
    fig.update_xaxes(title_font=dict(size=18, color='Dark Blue'))

    #create Y axis and the grids for Y-Axis
    fig.update_yaxes(title_text='Abortion Ratio since 1973')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='Light Grey', mirror=True)
    fig.update_yaxes(title_font=dict(size=18, color='Dark Blue'))

    return fig

#turn on debug, where debug=True if graph not working
app.run_server(debug=False, port=8082)