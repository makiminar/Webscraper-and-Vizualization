# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

pd.options.mode.chained_assignment = None

app = dash.Dash(__name__)

df = pd.read_csv('cleaned_data/realities.csv')

df.reset_index(inplace=True)
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Vizualizace dat z realitek", style={'text-align': 'center', 'margin': '5vh 5vw'}),

    html.Div([
        html.Div([
            dcc.Dropdown(id="select_region1",
                         options=[
                             {"label": "Praha", "value": "praha"},
                             {"label": "Středočeský kraj", "value": "stredocesky-kraj"},
                             {"label": "Ústecký kraj", "value": "ustecky-kraj"},
                             {"label": "Liberecký kraj", "value": "liberecky-kraj"},
                             {"label": "Královéhradecký kraj", "value": "kralovehradecky-kraj"},
                             {"label": "Moravskoslezský kraj", "value": "moravskoslezsky-kraj"},
                             {"label": "Plzeňský kraj", "value": "plzensky-kraj"},
                             {"label": "Oloumoucký kraj", "value": "olomoucky-kraj"},
                             {"label": "Pardubický kraj", "value": "pardubicky-kraj"},
                             {"label": "Vysočina", "value": "kraj-vysocina"},
                             {"label": "Zlínský kraj", "value": "zlinsky-kraj"},
                             {"label": "Jihočeský kraj", "value": "jihocesky-kraj"},
                             {"label": "Jihomoravský kraj", "value": "jihomoravsky-kraj"},
                             {"label": "Karlovarský kraj", "value": "karlovarsky-kraj"},
                         ],
                         multi=False,
                         value="praha",
                         style={'width': "50%"}
                         ),
            html.Br(),

            dcc.RadioItems(id='select_type1',
                           options=[
                               {'label': 'Pronájem', 'value': 'monthly'},
                               {'label': 'Prodej', 'value': 'total'},
                           ],
                           value='monthly'
                           ),
            html.Br(),

            html.Div(id='output_container1', children=[]),
            dcc.Graph(id='scatter_graph1', figure={}),
            dcc.Graph(id='bar_graph1', figure={}),
            dcc.Graph(id='pie_property_graph1', figure={}),
            dcc.Graph(id='pie_building_graph1', figure={})
        ],
            style={'width': '60%', 'display': 'block'}),

        html.Div([
            dcc.Dropdown(id="select_region2",
                         options=[
                             {"label": "Praha", "value": "praha"},
                             {"label": "Středočeský kraj", "value": "stredocesky-kraj"},
                             {"label": "Ústecký kraj", "value": "ustecky-kraj"},
                             {"label": "Liberecký kraj", "value": "liberecky-kraj"},
                             {"label": "Královéhradecký kraj", "value": "kralovehradecky-kraj"},
                             {"label": "Moravskoslezský kraj", "value": "moravskoslezsky-kraj"},
                             {"label": "Plzeňský kraj", "value": "plzensky-kraj"},
                             {"label": "Oloumoucký kraj", "value": "olomoucky-kraj"},
                             {"label": "Pardubický kraj", "value": "pardubicky-kraj"},
                             {"label": "Vysočina", "value": "kraj-vysocina"},
                             {"label": "Zlínský kraj", "value": "zlinsky-kraj"},
                             {"label": "Jihočeský kraj", "value": "jihocesky-kraj"},
                             {"label": "Jihomoravský kraj", "value": "jihomoravsky-kraj"},
                             {"label": "Karlovarský kraj", "value": "karlovarsky-kraj"},
                         ],
                         multi=False,
                         value="praha",
                         style={'width': "50%"}),
            html.Br(),
            dcc.RadioItems(id='select_type2',
                           options=[
                               {'label': 'Pronájem', 'value': 'monthly'},
                               {'label': 'Prodej', 'value': 'total'},
                           ],
                           value='monthly'
                           ),
            html.Br(),

            html.Div(id='output_container2', children=[]),
            dcc.Graph(id='scatter_graph2', figure={}),
            dcc.Graph(id='bar_graph2', figure={}),
            dcc.Graph(id='pie_property_graph2', figure={}),
            dcc.Graph(id='pie_building_graph2', figure={})
        ],
            style={'width': '60%', 'display': 'block'}),
    ], style={'display': 'flex', 'flex-flow': 'row', 'justify-content': 'space-evenly'}),

    html.Br()

], style={'display': 'flex', 'flex-flow': 'column', 'justify-content': 'center'})


# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='output_container1', component_property='children'),
    Output(component_id='scatter_graph1', component_property='figure'),
    Output(component_id='bar_graph1', component_property='figure'),
    Output(component_id='pie_property_graph1', component_property='figure'),
    Output(component_id='pie_building_graph1', component_property='figure'),
    Input(component_id='select_region1', component_property='value'),
    Input(component_id='select_type1', component_property='value')
)
def update_output1(selected_region, selected_type):
    container1 = 'The first chosen region is: "{}"'.format(selected_region)
    chosen_df = df.loc[(df["region"] == selected_region) & (df["payment"] == selected_type)]
    chosen_df.reset_index(drop=True, inplace=True)

    square_meter = chosen_df[(chosen_df.price.notnull()) & chosen_df.util_area.notnull()]
    square_meter["sqr_metr"] = square_meter["price"] / square_meter["util_area"]
    res = square_meter.describe().loc[['mean', 'min', 'max'], "sqr_metr"]

    fig_scatter = px.scatter(x=chosen_df.index, y=chosen_df["price"], title="Jednotlivé ceny nemovitostí - Y: cena")

    fig_bar = px.bar(x=["mean", "min", "max"], y=res, barmode='group', title="Min, max a střední hodnota ceny za metr "
                                                                             "čtvereční", height=400)

    fig_property_pie = px.pie(chosen_df, values="index", names="property",
                              color_discrete_sequence=px.colors.sequential.RdBu,
                              title="Rozložení vlastnictví nemovitostí")
    fig_property_pie.update_traces(textposition='inside', textinfo='percent+label')

    fig_building_pie = px.pie(chosen_df, values="index", names="building_type",
                              color_discrete_sequence=px.colors.sequential.ice,
                              title="Rozložení typů nemovitostí")
    fig_building_pie.update_traces(textposition='inside', textinfo='percent+label')

    return container1, fig_scatter, fig_bar, fig_property_pie, fig_building_pie


@app.callback(
    Output(component_id='output_container2', component_property='children'),
    Output(component_id='scatter_graph2', component_property='figure'),
    Output(component_id='bar_graph2', component_property='figure'),
    Output(component_id='pie_property_graph2', component_property='figure'),
    Output(component_id='pie_building_graph2', component_property='figure'),
    Input(component_id='select_region2', component_property='value'),
    Input(component_id='select_type2', component_property='value')
)
def update_output2(selected_region, selected_type):
    container2 = 'The second chosen region is: "{}"'.format(selected_region)
    chosen_df = df.loc[(df["region"] == selected_region) & (df["payment"] == selected_type)]
    chosen_df.reset_index(drop=True, inplace=True)

    square_meter = chosen_df[(chosen_df.price.notnull()) & chosen_df.util_area.notnull()]

    square_meter["sqr_metr"] = square_meter["price"] / square_meter["util_area"]
    res = square_meter.describe().loc[['mean', 'min', 'max'], "sqr_metr"]

    fig_scatter = px.scatter(x=chosen_df.index, y=chosen_df["price"], title="Jednotlivé ceny nemovitostí - Y: cena")

    fig_bar = px.bar(x=["mean", "min", "max"], y=res, barmode='group', title="Min, max a střední hodnota ceny za metr "
                                                                             "čtvereční", height=400)

    fig_property_pie = px.pie(chosen_df, values="index", names="property",
                              color_discrete_sequence=px.colors.sequential.RdBu,
                              title="Rozložení vlastnictví nemovitostí")
    fig_property_pie.update_traces(textposition='inside', textinfo='percent+label')

    fig_building_pie = px.pie(chosen_df, values="index", names="building_type",
                              color_discrete_sequence=px.colors.sequential.ice,
                              title="Rozložení typů nemovitostí")
    fig_building_pie.update_traces(textposition='inside', textinfo='percent+label')

    return container2, fig_scatter, fig_bar, fig_property_pie, fig_building_pie


if __name__ == '__main__':
    app.run_server(debug=True)
