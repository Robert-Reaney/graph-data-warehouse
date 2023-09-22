from dash.dependencies import Input, Output, State
import logging

# Define the callback to update the graph and title
def register_callbacks(app, neodata):

    @app.callback(
        Output('graph-viewer', 'elements'),
        Input('query-button', 'n_clicks'),
        State('dacis-id', 'value')
    )
    def update_graph(n_clicks, dacis_id):
        logging.info(f'graph update triggered for dacis_id={dacis_id}')
        return neodata.ubo_query(dacis_id)