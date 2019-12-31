import dash_html_components as html
import dash_core_components as dcc


def Header(app):
    return html.Div([get_header(app), html.Br([])])


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.Img(
                        src=app.get_asset_url("agrodat.PNG"),
                        className="logo",
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("Agrodat: Una oportunidad para crecer tu finca")],
                        className="seven columns main-title",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table

def make_table_serie(df, year, code):
    serie = df.loc[year, code]
    length = serie.shape[0]
    table = []
    index = serie.index
    values = serie.values
    for i in range(length):
        html_row = []
        html_row.append(html.Td([index[i]]))
        html_row.append(html.Td([values[i]]))
        table.append(html.Tr(html_row))

    return table
