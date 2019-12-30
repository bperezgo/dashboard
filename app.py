# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from utils import Header, make_dash_table, make_table_serie

import pandas as pd
import numpy as np
import pathlib
from datetime import datetime

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("./data").resolve()

df_general_data = pd.read_csv(DATA_PATH.joinpath("general_data.csv"))
df_indicators = pd.read_csv(DATA_PATH.joinpath("indicators.csv"))
df_point_of_eq = pd.read_csv(DATA_PATH.joinpath("point_of_eq.csv"))

#print(df_point_of_eq.set_index(['CODIGO', 'FECHA']).loc[512].index)

codes = df_indicators['CODIGO'].unique()


indicators = df_indicators.columns[5:]

general_cow_information = df_point_of_eq.groupby(['AÑO', 'CODIGO']).mean()
general_cow_information.drop(['MES', 'QUINCENA'], inplace = True, axis = 1)
general_information = df_indicators.groupby(['AÑO', 'CODIGO']).mean()
general_information.drop(['MES', 'QUINCENA'], inplace = True, axis = 1)

#df_point_of_eq = df_point_of_eq.set_index(['AÑO', 'MES', 'QUINCENA'])
df_point_of_eq_DATE = df_point_of_eq.set_index(['CODIGO', 'FECHA']).loc[512].index

dates_converted = [datetime.strptime(date, '%Y-%m-%d').date() for date in df_point_of_eq_DATE]

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Product Summary"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                    As the industry’s first index fund for individual investors, \
                                    the Calibre Index Fund is a low-cost way to gain diversified exposure \
                                    to the U.S. equity market. The fund offers exposure to 500 of the \
                                    largest U.S. companies, which span many different industries and \
                                    account for about three-fourths of the U.S. stock market’s value. \
                                    The key risk for the fund is the volatility that comes with its full \
                                    exposure to the stock market. Because the Calibre Index Fund is broadly \
                                    diversified within the large-capitalization market, it may be \
                                    considered a core equity holding in a portfolio.",
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    html.Div([
                            html.H6("Código de la finca"),
                            html.Br([]),
                            dcc.Dropdown(
                                id='codes',
                                options=[{'label': i, 'value': i} for i in codes],
                                value='512'
                            ),
                            html.Br([]),
                            html.H6("Indicador a analizar"),
                            html.Br([]),
                            dcc.Dropdown(
                                id='indicators',
                                options=[{'label': i, 'value': i} for i in indicators],
                                value='LITROS POR VACA'
                            ),
                            html.Br([]),
                        ], style={'width': '90%', 'float': 'right', 'display': 'inline-block'}),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Fund Facts"], className="subtitle padded"
                                    ),
                                    html.Table(make_table_serie(general_information, 2018, 512)),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Average annual performance",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id='time-serie',
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Hypothetical growth of $10,000",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="eq-point",
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Price & Performance (%)",
                                        className="subtitle padded",
                                    ),
                                    html.Table(make_table_serie(general_cow_information, 2018, 512))
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row ",
                    ),
                    html.Div(dcc.Slider(
                        id='dates-slider',
                        min=general_cow_information.index.levels[0][0],
                        max=general_cow_information.index.levels[0][-1],
                        value=general_cow_information.index.levels[0][-1],
                        marks={str(fecha): str(fecha) for fecha in general_cow_information.index.levels[0]},
                        step=None
                    ), style={'width': '90%', 'padding': '0px 20px 20px 20px'}),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Planea tu producción"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                    Juega con las siguientes barras para que veas cómo \
                                    cambia tu punto de equilibrio y para que planees cómo \
                                    hacer tus inversiones",
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Hypothetical growth of $10,000",
                                        className="subtitle padded",
                                    ),
                                    html.Div(dcc.Graph(
                                        id="eq-sens-point",
                                        config={"displayModeBar": False},
                                    ), style={'width': '90%', 'padding': '0px 20px 20px 20px'}),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row ",
                    ),
                    html.Div([
                        html.Table([
                            html.Tr([
                                html.Td('Volumen de producción total'),
                                html.Td(
                                    dcc.Input(id="input-1", type="text", value="2000")
                                )
                            ]),
                            html.Tr([
                                html.Td('Número de hectáreas'),
                                html.Td(
                                    dcc.Input(id="input-2", type="text", value="40")
                                )
                            ]),
                            html.Tr([
                                html.Td('Vacas en ordeño'),
                                html.Td(
                                    dcc.Input(id="input-3", type="text", value="30")
                                )
                            ]),
                            html.Tr([
                                html.Td('Vacas Horras'),
                                html.Td(
                                    dcc.Input(id="input-4", type="text", value="5")
                                )
                            ])
                        ])
                    ]),
                    html.H6("Precio"),
                    html.Br([]),
                    html.Div([
                        html.Div(dcc.Slider(
                            id='sens-slider-1',
                            min=800,
                            max=1500,
                            value=1000,
                            marks={
                                800: {'label': '800 COP', 'style': {'color': '#77b0b1'}},
                                1500: {'label': '1.500 COP', 'style': {'color': '#f50'}}
                            },
                            step=10,
                            included = False
                        ), style={'width': '45%', 'padding': '0px 20px 20px 20px'}),
                        html.Div(id = 'sens-text-1')
                    ]),
                    html.H6("Número de trabajadores"),
                    html.Br([]),
                    html.Div([
                        html.Div(dcc.Slider(
                            id='sens-slider-2',
                            min=0,
                            max=40,
                            value=10,
                            marks={
                                0: {'label': '0', 'style': {'color': '#77b0b1'}},
                                40: {'label': '40', 'style': {'color': '#f50'}}
                            },
                            step=1,
                            included = False
                        ), style={'width': '90%', 'padding': '0px 20px 20px 20px'}),
                        html.Div(id = 'sens-text-2')
                    ]),
                    html.H6("Arrendamiento por fanegada"),
                    html.Br([]),
                    html.Div([
                        html.Div(dcc.Slider(
                            id='sens-slider-3',
                            min=400000,
                            max=1000000,
                            value=400000,
                            marks={
                                400000: {'label': '400.000', 'style': {'color': '#77b0b1'}},
                                1000000: {'label': '1.000.000', 'style': {'color': '#f50'}}
                            },
                            step=10000,
                            included = False
                        ), style={'width': '90%', 'padding': '0px 20px 20px 20px'}),
                    html.Div(id = 'sens-text-3')
                    ]),
                    html.H6("Salario promedio del trabajador"),
                    html.Br([]),
                    html.Div([
                        html.Div(dcc.Slider(
                            id='sens-slider-4',
                            min=800000,
                            max=2000000,
                            value=1000000,
                            marks={
                                800000: {'label': '800.000', 'style': {'color': '#77b0b1'}},
                                2000000: {'label': '2.000.000', 'style': {'color': '#f50'}}
                            },
                            step=10000,
                            included = False
                        ), style={'width': '90%', 'padding': '0px 20px 20px 20px'}),
                        html.Div(id = 'sens-text-4')
                    ]),
                    html.H6("Precio concentrado energético"),
                    html.Br([]),
                    html.Div([
                        html.Div(dcc.Slider(
                            id='sens-slider-5',
                            min=0,
                            max=1500,
                            value=1000,
                            marks={
                                0: {'label': '0', 'style': {'color': '#77b0b1'}},
                                1500: {'label': '1.500 COP', 'style': {'color': '#f50'}}
                            },
                            step=10,
                            included = False
                        ), style={'width': '90%', 'padding': '0px 20px 20px 20px'}),
                        html.Div(id = 'sens-text-5')
                    ]),
                    html.H6("Masa concentrado energético"),
                    html.Br([]),
                    html.Div([
                        html.Div(dcc.Slider(
                            id='sens-slider-6',
                            min=0,
                            max=2000,
                            value=400,
                            marks={
                                0: {'label': '0', 'style': {'color': '#77b0b1'}},
                                2000: {'label': '2.000 COP', 'style': {'color': '#f50'}}
                            },
                            step=10,
                            included = False
                        ), style={'width': '90%', 'padding': '0px 20px 20px 20px'}),
                        html.Div(id = 'sens-text-6')
                    ]),
                    html.H6("Precio concentrado fibroso"),
                    html.Br([]),
                    html.Div([
                    html.Div(dcc.Slider(
                        id='sens-slider-7',
                        min=0,
                        max=1500,
                        value=1000,
                        marks={
                            0: {'label': '0', 'style': {'color': '#77b0b1'}},
                            1500: {'label': '1.500 COP', 'style': {'color': '#f50'}}
                        },
                        step=10,
                        included = False
                    ), style={'width': '90%', 'padding': '0px 20px 20px 20px'}),
                    html.Div(id = 'sens-text-7')]),
                    html.H6("Masa concentrado fibroso"),
                    html.Br([]),
                    html.Div([
                    html.Div(dcc.Slider(
                        id='sens-slider-8',
                        min=0,
                        max=2000,
                        value=400,
                        marks={
                            0: {'label': '0', 'style': {'color': '#77b0b1'}},
                            2000: {'label': '2.000 COP', 'style': {'color': '#f50'}}
                        },
                        step=10,
                        included = False
                    ), style={'width': '90%', 'padding': '0px 20px 20px 20px'}),
                    html.Div(id = 'sens-text-8')]),
                    html.Div([
                        html.H6("Indicadores del pronóstico"),
                        html.Table([
                            html.Tr([
                                html.Td('Utilidad'),
                                html.Td(html.Div(id = 'output-utilidad'))
                            ]),
                            html.Tr([
                                html.Td('% Utilidad'),
                                html.Td(html.Div(id = 'output-porc-utilidad'))
                            ]),
                            html.Tr([
                                html.Td('Ingresos Netos'),
                                html.Td(html.Div(id = 'output-ing'))
                            ]),
                            html.Tr([
                                html.Td('Costos totales'),
                                html.Td(html.Div(id = 'output-ct'))
                            ]),
                            html.Tr([
                                html.Td('Punto de equilibrio'),
                                html.Td(html.Div(id = 'output-pe'))
                            ]),
                            html.Tr([
                                html.Td('Litros / Vaca'),
                                html.Td(html.Div(id = 'output-lit-vac'))
                            ]),
                            html.Tr([
                                html.Td('Litros / Hectáreas / año'),
                                html.Td(html.Div(id = 'output-lit-ha-a'))
                            ]),
                            html.Tr([
                                html.Td('Litros / trabajador'),
                                html.Td(html.Div(id = 'output-lit-trab'))
                            ]),
                            html.Tr([
                                html.Td('Litros libres'),
                                html.Td(html.Div(id = 'output-lit-lib'))
                            ]),
                            html.Tr([
                                html.Td('Concentrado / leche'),
                                html.Td(html.Div(id = 'output-conc-leche'))
                            ]),
                        ])
                    ]),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )]
)

def create_time_series(dff, title):
    #print(dff)
    #print(dff.index)
    #print(dff.values)
    #print(title)
    return {
        "data": [
            go.Scatter(
                x=dff.index,
                y=dff.values,
                line={"color": "#97151c"},
                mode="lines",
                name="Calibre Index Fund Inv",
            )
        ],
        "layout": go.Layout(
            autosize=True,
            title=title,
            font={"family": "Raleway", "size": 10},
            height=200,
            width=340,
            hovermode="closest",
            legend={
                "x": -0.0277108433735,
                "y": -0.142606516291,
                "orientation": "h",
            },
            margin={
                "r": 20,
                "t": 20,
                "b": 20,
                "l": 50,
            },
            showlegend=True,
            xaxis={
                "autorange": True,
                "linecolor": "rgb(0, 0, 0)",
                "linewidth": 1,
                "range": [2008, 2018],
                "showgrid": False,
                "showline": True,
                "title": "",
                "type": "linear",
            },
            yaxis={
                "autorange": True,
                "gridcolor": "rgba(127, 127, 127, 0.2)",
                "mirror": False,
                "nticks": 4,
                "showgrid": True,
                "showline": True,
                "ticklen": 10,
                "ticks": "outside",
                "title": "$",
                "type": "linear",
                "zeroline": False,
                "zerolinewidth": 4,
            },
        ),
    }

def eq_point_serie(x, y, z,v, w, title):
    #print(dff)
    #print(dff.index)
    #print(dff.values)
    #print(title)
    return {
        "data": [
            go.Scatter(
                x=x,
                y=y,
                line={"color": "#97151c"},
                mode="lines",
                name="Ingresos",
            ),
            go.Scatter(
                x=x,
                y=z,
                line={"color": "#97151c"},
                mode="lines",
                name="Costos",
            ),
            go.Scatter(
                x=v,
                y=w,
                line={"color": "#97151c"},
                mode="lines",
                name="Volumen total",
            )
        ],
        "layout": go.Layout(
            autosize=True,
            title=title,
            font={"family": "Raleway", "size": 10},
            height=240,
            width=300,
            hovermode="closest",
            legend={
                "x": -0.0277108433735,
                "y": -0.242606516291,
                "orientation": "h",
            },
            margin={
                "r": 20,
                "t": 20,
                "b": 20,
                "l": 50,
            },
            showlegend=True,
            xaxis={
                "autorange": True,
                "linecolor": "rgb(0, 0, 0)",
                "linewidth": 1,
                "range": [2008, 2018],
                "showgrid": False,
                "showline": True,
                "title": "",
                "type": "linear",
            },
            yaxis={
                "autorange": True,
                "gridcolor": "rgba(127, 127, 127, 0.2)",
                "mirror": False,
                "nticks": 4,
                "showgrid": True,
                "showline": True,
                "ticklen": 10,
                "ticks": "outside",
                "title": "$",
                "type": "linear",
                "zeroline": False,
                "zerolinewidth": 4,
            },
        ),
    }
@app.callback(
    dash.dependencies.Output('time-serie', 'figure'),
    [dash.dependencies.Input('codes', 'value'),
     dash.dependencies.Input('indicators', 'value')])
def update_timeseries(code, indicator):
    mask = (df_indicators['CODIGO'] == int(code))
    dff = df_indicators[mask].groupby(['AÑO', 'MES']).mean().loc[2018][indicator]
    title = '<b>{}</b><br>{}'.format(indicator, indicator)
    try:
        return create_time_series(dff, title)
    except:
        return None

@app.callback(
    dash.dependencies.Output('eq-point', 'figure'),
    [dash.dependencies.Input('codes', 'value'),
     dash.dependencies.Input('dates-slider', 'value')])
def update_timeseries(code, date):
    # date is in years
    mask = (df_point_of_eq['CODIGO'] == int(code))
    dff = df_point_of_eq[mask].groupby(['AÑO']).mean()[['PRECIO LECHE','COSTOS FIJOS','COSTOS VARIABLES','PUNTO DE EQUILIBRIO','VOLUMEN DIA']]
    x = np.array(list(range(0, int(dff['VOLUMEN DIA'].loc[date]), 100)))
    x = x*1.0
    y = x * dff['PRECIO LECHE'].loc[date]
    z = x * dff['COSTOS VARIABLES'].loc[date] + dff['COSTOS FIJOS'].loc[date]
    v = np.array([dff['VOLUMEN DIA'].loc[date]]*2)
    w = np.array([0.0, y[-1]])
    title = '<b>{}</b><br>{}'.format(date, date)
    try:
        return eq_point_serie(x, y, z, v, w, title)
    except:
        return None

@app.callback(
    [Output('eq-sens-point', 'figure'),
    Output('output-utilidad', 'children'),
    Output('output-conc-leche', 'children'),
    Output('output-lit-lib', 'children'),
    Output('output-lit-trab', 'children'),
    Output('output-lit-ha-a', 'children'),
    Output('output-lit-vac', 'children'),
    Output('output-pe', 'children'),
    Output('output-ct', 'children'),
    Output('output-ing', 'children'),
    Output('output-porc-utilidad', 'children')],
    [Input('sens-slider-1', 'value'),
    Input('sens-slider-2', 'value'),
    Input('sens-slider-3', 'value'),
    Input('sens-slider-4', 'value'),
    Input('sens-slider-5', 'value'),
    Input('sens-slider-6', 'value'),
    Input('sens-slider-7', 'value'),
    Input('sens-slider-8', 'value'),
    Input("input-1", "value"),
    Input("input-2", "value"),
    Input("input-3", "value"),
    Input("input-4", "value")])
def update_timeseries(precio, trab, arrend, salario, prec_ene, masa_ene, prec_fib, masa_fib, vol, HEC, vacas_ord, vacas_horr):
    if (vol is None) or (HEC is None):
        print('Amiguis no funciona')
        raise dash.excepcions.PreventUpdate
    volumen = float(vol)
    CV = (prec_ene*masa_ene + prec_fib*masa_fib) / volumen
    CF = arrend * float(HEC) * 10000 / 6400 / 30 + salario*trab/30
    x = np.array(list(range(0, int(volumen), 100)))
    x = x*1.1
    y = x * precio
    z = x * CV + CF
    v = np.array([volumen]*2)
    w = np.array([0.0, y[-1]])

    title = '<b>{}</b><br>{}'.format('sensibilidad', 'sensibilidad')

    vacas = float(vacas_ord) + float(vacas_horr)

    utilidad = (precio - CV) * volumen - CF
    conc_leche = (masa_ene + masa_fib) / volumen
    lit_lib = (precio*volumen - prec_ene * masa_ene - prec_fib * masa_fib) / (precio * vacas)
    lit_trab = volumen / trab
    lit_ha_a = volumen * 365 / float(HEC)
    lit_vac = volumen / vacas
    punto_eq = CF / (precio - CV)
    costos_tot = CV * volumen + CF
    ingresos = precio * volumen
    porc_utilidad = utilidad / ingresos * 100

    try:
        return eq_point_serie(x, y, z, v, w, title), u'{:0.2f}'.format(utilidad), u'{:0.2f}'.format(conc_leche), u'{:0.2f}'.format(lit_lib), u'{:0.2f}'.format(lit_trab), u'{:0.2f}'.format(lit_ha_a), u'{:0.2f}'.format(lit_vac), u'{:0.2f}'.format(punto_eq), u'{:0.2f}'.format(costos_tot), u'{:0.2f}'.format(ingresos), u'{:0.4f}'.format(porc_utilidad)
    except:
        return None

@app.callback(
    Output("sens-text-1", "children"),
    [Input("sens-slider-1", "value")],
)
def update_output(value_slider):
    return u'{}'.format(str(value_slider))

@app.callback(
    Output("sens-text-2", "children"),
    [Input("sens-slider-2", "value")],
)
def update_output(value_slider):
    return u'{}'.format(str(value_slider))

@app.callback(
    Output("sens-text-3", "children"),
    [Input("sens-slider-3", "value")],
)
def update_output(value_slider):
    return u'{}'.format(str(value_slider))

@app.callback(
    Output("sens-text-4", "children"),
    [Input("sens-slider-4", "value")],
)
def update_output(value_slider):
    return u'{}'.format(str(value_slider))

@app.callback(
    Output("sens-text-5", "children"),
    [Input("sens-slider-5", "value")],
)
def update_output(value_slider):
    return u'{}'.format(str(value_slider))

@app.callback(
    Output("sens-text-6", "children"),
    [Input("sens-slider-6", "value")],
)
def update_output(value_slider):
    return u'{}'.format(str(value_slider))

@app.callback(
    Output("sens-text-7", "children"),
    [Input("sens-slider-7", "value")],
)
def update_output(value_slider):
    return u'{}'.format(str(value_slider))

@app.callback(
    Output("sens-text-8", "children"),
    [Input("sens-slider-8", "value")],
)
def update_output(value_slider):
    return u'{}'.format(str(value_slider))


if __name__ == "__main__":
    app.run_server(debug=True)
