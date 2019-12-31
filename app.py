# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from utils import Header

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
                                        "Sensibilidad del punto de equilibrio",
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
                                    dcc.Input(id="input-1", type="text", value="789")
                                )
                            ]),
                            html.Tr([
                                html.Td('Número de hectáreas'),
                                html.Td(
                                    dcc.Input(id="input-2", type="text", value="20")
                                )
                            ]),
                            html.Tr([
                                html.Td('Vacas en ordeño'),
                                html.Td(
                                    dcc.Input(id="input-3", type="text", value="45")
                                )
                            ]),
                            html.Tr([
                                html.Td('Vacas Horras'),
                                html.Td(
                                    dcc.Input(id="input-4", type="text", value="7")
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
                            value=1230,
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
                            value=2,
                            marks={
                                0: {'label': '0', 'style': {'color': '#77b0b1'}},
                                40: {'label': '40', 'style': {'color': '#f50'}}
                            },
                            step=1,
                            included = False
                        ), style={'width': '90%', 'padding': '0px 20px 20px 20px'}),
                        html.Div(id = 'sens-text-2')
                    ]),
                    html.H6("Arrendamiento por fanegada mensual"),
                    html.Br([]),
                    html.Div([
                        html.Div(dcc.Slider(
                            id='sens-slider-3',
                            min=100000,
                            max=1000000,
                            value=200000,
                            marks={
                                100000: {'label': '100.000', 'style': {'color': '#77b0b1'}},
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
                            value=1300,
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
                            value=250,
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
                        value=1300,
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
                        value=250,
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
                                html.Td('Leche / concentrado'),
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
                line={"color": "#15961a"},
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
                line={"color": "#153d96"},
                mode="lines",
                name="Volumen total",
            )
        ],
        "layout": go.Layout(
            autosize=True,
            title=title,
            font={"family": "Raleway", "size": 10},
            height=480,
            width=600,
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
    conc_leche = volumen / (masa_ene + masa_fib)
    lit_lib = (precio*volumen - prec_ene * masa_ene - prec_fib * masa_fib) / (precio * float(vacas_ord))
    lit_trab = volumen / trab
    lit_ha_a = volumen * 365 / float(HEC)
    lit_vac = volumen / float(vacas_ord)
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
