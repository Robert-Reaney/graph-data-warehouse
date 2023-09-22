# Import necessary libraries
import dash
import dash_bootstrap_components as dbc

from callbacks import register_callbacks
from layout import make_layout
from data import NeoData

# initialize data connection
neodata = NeoData()


# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout
app.layout = make_layout()

# register callbacks
register_callbacks(app, neodata)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
