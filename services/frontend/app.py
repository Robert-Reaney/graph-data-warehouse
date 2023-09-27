# Import necessary libraries
import dash
import dash_bootstrap_components as dbc

# from callbacks import register_callbacks
from layout import make_layout
from data import NeoData
import networkx as nx
import logging

# initialize graph
G = nx.MultiDiGraph()

# initialize data connection
neodata = NeoData()

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout
app.layout = make_layout()

# register callbacks

# register_callbacks(app, neodata)
from dash.dependencies import Input, Output, State
@app.callback(
    Output('graph-viewer', 'elements', allow_duplicate=True),
    Output('graph-viewer', 'layout', allow_duplicate=True),
    Input('query-button', 'n_clicks'),
    State('dacis-id', 'value'),
    prevent_initial_call = True
)
def update_graph(n_clicks, dacis_id):
    graph_data = neodata.test_ubo(dacis_id)
    # graph_data = neodata.ubo_query(dacis_id)
    logging.info(f'graph update triggered for dacis_id={dacis_id} with graph_data={graph_data}')
    return [graph_data, {'name': 'breadthfirst', 'roots': f'#{dacis_id}'}]
    # return graph_data

@app.callback(
    Output('node-click', 'children'),
    Output('graph-viewer', 'elements', allow_duplicate=True),
    Input('graph-viewer', 'tapNodeData'),
    State('graph-viewer', 'elements'),
    prevent_initial_call = True
)
def click_node(data, elements):
    if data:
        text = "You clicked: " + data['label']
        logging.info(f'clicked {data}')

        if len(data['id']) < 10:
            budget_info = neodata.query(f"""
            MATCH (b:Budget)<-[f:FUNDED_BY]-(c:Company) where c.id='{data['id']}' return b,f,c
            """)
            dash_elements = neodata.netx_to_dash(neodata.cypher_to_netx(budget_info))
            logging.info(dash_elements)

            elements = elements + dash_elements
            # need to remove the clicked node so it isn't duplicated
            # extra_elements = [x for x in dash_elements if x['data']['id']]

            if len(dash_elements) == 0:
                text += f'\n and found no related budgets found for {data["label"]}'
            else:
                budget_ids = []
                for element in dash_elements:
                    _id = element['data'].get('id', None)
                    if _id and element['classes'] == 'budget':
                        budget_ids.append(_id)
                text += f"\n and found related budget_ids of {budget_ids}"

        return [text, elements]
        


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)

