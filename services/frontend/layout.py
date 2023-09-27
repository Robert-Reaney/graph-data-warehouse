import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import dash_cytoscape as cyto

def make_layout():
    return dbc.Container(
        [
            # Title row
            dbc.Row(
                dbc.Col(
                    html.H1("FOCI Risk", id='main-title'),
                    width={'size': 6, 'offset': 3},
                    className='text-center'
                ),
                className='mb-4 mt-4'
            ),
            
            # 2nd Row for widgets and graph
            dbc.Row(
                [
                    # 1st column for widgets
                    dbc.Col(
                        [
                            html.Button(
                                'Query', id='query-button'
                            ),
                            dcc.Input(
                                id='dacis-id',
                                type='text',
                                value='152516'
                            ),
                            html.P(id='node-click')
                        ],
                        width=3,
                        className='mb-4'
                    ),
                    # 2nd column for a graph
                    dbc.Col(
                        cyto.Cytoscape(
                            id='graph-viewer',
                            layout={
                                'name': 'breadthfirst'
                            },
                            style={'width': '100%', 'height': '600px'},
                            elements=[],
                            stylesheet=[
                                {'selector': 'node', 'style': {'content': 'data(label)'}},
                                {'selector': 'edge', 'style': {'content': 'data(label)'}},
                                {'selector': '.company', 'style': {'shape': 'triangle', 'color': 'red'}},
                                {'selector': '.entity', 'style': {'shape': 'circle'}}
                            ]
                        ),
                        width=9,
                        className='mb-4'
                    )
                ]
            )
        ],
        fluid=True
    )


# dcc.Graph(
#     id='scatter-plot',
#     figure=px.scatter(data.df, x='x', y='y', color='x')
# )