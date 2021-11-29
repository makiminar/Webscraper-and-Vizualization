# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

FILES = ['ustecky', 'pardubicky', 'stredocesky',
              'praha', 'moravskoslezsky', 'zlinsky',
              'liberecky', 'plzensky', 'kralovehradecky',
              'karlovarsky', 'jihocesky', 'olomoucky',
              'jihomoravsky', 'vysocina']

# -- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")

df = pd.DataFrame()

for x in FILES:
    tmp_df = pd.read_csv('../webscraper/outputs/reality-' + x + '.csv')
    tmp_df["kraj"] = x
    df = pd.concat([df, tmp_df], axis=0)

df.reset_index(inplace=True)
print(df.head())
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Vizualizace dat z realitek", style={'text-align': 'center'}),

    dcc.Dropdown(id="select_region",
                 options=[
                     {"label": "Praha", "value": "praha"},
                     {"label": "Středočeský kraj", "value": "stredocesky"},
                     {"label": "Ústecký kraj", "value": "ustecky"},
                     {"label": "Liberecký kraj", "value": "liberecky"},
                     {"label": "Královéhradecký kraj", "value": "kralovehradecky"},
                     {"label": "Moravskoslezský kraj", "value": "moravskoslezsky"},
                     {"label": "Plzeňský kraj", "value": "plzensky"},
                     {"label": "Oloumoucký kraj", "value": "olomoucky"},
                     {"label": "Pardubický kraj", "value": "pardubicky"},
                     {"label": "Vysočina", "value": "vysocina"},
                     {"label": "Zlínský kraj", "value": "zlinsky"},
                     {"label": "Jihočeský kraj", "value": "jihocesky"},
                     {"label": "Jihomoravský kraj", "value": "jihomoravsky"},
                     {"label": "Karlovarský kraj", "value": "karlovarsky"},
                 ],
                 multi=False,
                 value="praha",
                 style={'width': "40%"}
                 ),

    html.Br(),
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])


# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='select_region', component_property='value')]
)
def update_output(value):
    print(value)
    print(type(value))

    container = 'The regioin chosen by user was: "{}"'.format(value)

    dff = df.copy()
    # dodelat - spojit datasety
    dff = dff[dff["kraj"] == value]

    # Plotly Express
    fig = px.scatter(dff, x="index", y="price")

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig


if __name__ == '__main__':
    app.run_server(debug=True)
