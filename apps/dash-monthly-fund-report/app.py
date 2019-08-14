import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from plotly import graph_objs as go
from datetime import datetime as dt
import json
import pandas as pd
import os

app = dash.Dash(__name__)
server = app.server


df_fund_data = pd.read_csv("https://plot.ly/~jackp/17534.csv")
df_fund_data.head()

df_perf_summary = pd.read_csv("https://plot.ly/~jackp/17530.csv")
df_perf_summary.head()

df_cal_year = pd.read_csv("https://plot.ly/~jackp/17528.csv")
df_cal_year.head()

df_perf_pc = pd.read_csv("https://plot.ly/~jackp/17532.csv")


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table


modifed_perf_table = make_dash_table(df_perf_summary)


modifed_perf_table.insert(
    0,
    html.Tr(
        [
            html.Td([]),
            html.Td(["Cumulative"], colSpan=4, style={"text-align": "center"}),
            html.Td(["Annualised"], colSpan=4, style={"text-align": "center"}),
        ],
        style={"background": "white", "font-weight": "600"},
    ),
)

df_fund_info = pd.read_csv("https://plot.ly/~jackp/17544.csv")
df_fund_characteristics = pd.read_csv("https://plot.ly/~jackp/17542.csv")
df_fund_facts = pd.read_csv("https://plot.ly/~jackp/17540.csv")
df_bond_allocation = pd.read_csv("https://plot.ly/~jackp/17538.csv")

df_sector_allocation = pd.read_csv("data/sector-allocation.csv")


def header():
    return html.Div(
        [
            html.Div(
                className="row",
                children=html.Img(className="logo", src=app.get_asset_url("logo.png")),
            ),
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="header-left",
                        children=[
                            html.H1(
                                "Goldman Sachs Strategic Absolute Return Bond II Portfolio"
                            ),
                            html.H2("A sub-fund of Goldman Sachs Funds, SICAV"),
                        ],
                    ),
                    html.Div(
                        className="header-right",
                        children=[
                            html.H1(
                                children=[
                                    html.Span("03", className="light-blue"),
                                    html.Span("17", className="blue"),
                                ]
                            ),
                            html.H6("Monthly Fund Update"),
                        ],
                    ),
                ],
            ),
        ]
    )


# Describe the layout, or the UI, of the app
app.layout = html.Div(
    [
        # Page 1
        html.Div(
            [
                html.A(["Print PDF"], className="button no-print"),
                # Subpage 1
                html.Div(
                    [
                        # Row 1
                        header(),
                        html.Br([]),
                        # Row 2
                        html.Div(
                            className="spec-row",
                            children=[
                                html.Div(
                                    className="six columns div-investor-profile",
                                    children=[
                                        html.H5("Investor Profile"),
                                        html.H6("Investor objective"),
                                        html.P("Capital appreciation and income."),
                                        html.H6(
                                            "Position in your overall investment portfolio"
                                        ),
                                        html.P(
                                            "The fund can complement your portfolio."
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="six columns div-fund-designed-for",
                                    children=[
                                        html.H4("The fund is designed for:"),
                                        html.P(
                                            "The fund is designed for investors who are looking for a flexible \
                                global investment and sub-investment grade fixed income portfolio \
                                that has the ability to alter its exposure with an emphasis on interest \
                                rates, currencies and credit markets and that seeks to generate returns \
                                through different market conditions with a riskier investment strategy \
                                than GS Strategic Absolute Return Bond I Portfolio."
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        # Row 3
                        html.Div(
                            className="row",
                            children=[
                                # Left Side
                                html.Div(
                                    className="six columns",
                                    children=[
                                        # Performace %
                                        html.Div(
                                            children=[
                                                html.H6("Performance (%)"),
                                                html.Table(make_dash_table(df_perf_pc)),
                                            ]
                                        ),
                                        # Fund Data
                                        html.Div(
                                            children=[
                                                html.H6("Fund Data"),
                                                html.Table(
                                                    make_dash_table(df_fund_data)
                                                ),
                                            ]
                                        ),
                                    ],
                                ),
                                # Right Side
                                html.Div(
                                    className="six columns div-graphs",
                                    children=[
                                        html.Div(
                                            [
                                                html.H6("Performance (Indexed)"),
                                                html.Iframe(
                                                    src="https://plot.ly/~jackp/17553.embed?modebar=false&link=false&autosize=true",
                                                    style={
                                                        "border": "0",
                                                        "width": "100%",
                                                        "height": "250",
                                                    },
                                                ),
                                                html.P(
                                                    "This is an actively managed fund that is not designed to track its reference benchmark. \
                                                    Therefore the performance of the fund and the performance of its reference benchmark \
                                                    may diverge. In addition stated reference benchmark returns do not reflect any management \
                                                    or other charges to the fund, whereas stated returns of the fund do."
                                                ),
                                                html.P(
                                                    "Past performance does not guarantee future results, which may vary. \
                                                    The value of investments and the income derived from investments will fluctuate and \
                                                    can go down as well as up. A loss of capital may occur."
                                                ),
                                            ]
                                        )
                                    ],
                                ),
                            ],
                        ),
                        # Row 3
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    children=[
                                        html.H6("Performance Summary (%)"),
                                        html.Table(
                                            modifed_perf_table, className="reversed"
                                        ),
                                        html.H6("Calendar Year Performance (%)"),
                                        html.Table(make_dash_table(df_cal_year)),
                                    ]
                                )
                            ],
                        ),
                    ],
                    className="subpage",
                ),
            ],
            className="page",
        ),
        # Page 2
        html.Div(
            [
                html.A(["Print PDF"], className="button no-print"),
                # Subpage 2
                html.Div(
                    children=[
                        # Row 1
                        header(),
                        html.Br([]),
                        # Row 2
                        html.Div(
                            className="row",
                            children=[
                                # Left Column
                                html.Div(
                                    className="five columns",
                                    children=[
                                        html.H6("Financial Information"),
                                        html.Table(make_dash_table(df_fund_info)),
                                        html.H6("Fund Characteristics"),
                                        html.Table(
                                            make_dash_table(df_fund_characteristics)
                                        ),
                                        html.H6("Fund Facts"),
                                        html.Table(make_dash_table(df_fund_facts)),
                                        html.H6("Country Bond Allocation (%)"),
                                        html.Table(make_dash_table(df_bond_allocation)),
                                    ],
                                ),
                                # Right Column
                                html.Div(
                                    className="seven columns div-graphs",
                                    children=[
                                        html.H6("Sector Allocation (%)"),
                                        dcc.Graph(
                                            figure={
                                                "data": [
                                                    {
                                                        "uid": "353874",
                                                        "mode": "markers",
                                                        "name": "B",
                                                        "type": "bar",
                                                        "x": df_sector_allocation["x"],
                                                        "y": df_sector_allocation["y"],
                                                        "marker": {"color": "#119dff"},
                                                    }
                                                ],
                                                "layout": {
                                                    "width": 300,
                                                    "font": "8px",
                                                    "xaxis": {
                                                        "type": "category",
                                                        "range": [-0.5, 11.5],
                                                        "autorange": True,
                                                    },
                                                    "yaxis": {
                                                        "type": "linear",
                                                        "range": [0, 48.94736842105263],
                                                        "autorange": True,
                                                    },
                                                    "height": 300,
                                                    "margin": dict(
                                                        t=0, r=0, b=160, l=0
                                                    ),
                                                    "hovermode": "closest",
                                                    "bargroupgap": 0.2,
                                                },
                                            }
                                        ),
                                        html.H6("Top 10 Currency Weights (%)"),
                                        dcc.Graph(
                                            figure={
                                                "data": [
                                                    {
                                                        "uid": "80eb70",
                                                        "name": "Col1",
                                                        "type": "bar",
                                                        "x": [
                                                            -50.8,
                                                            1.8,
                                                            1.8,
                                                            2.2,
                                                            2.3,
                                                            3.2,
                                                            4.2,
                                                            5.7,
                                                            6.6,
                                                            8,
                                                            8.9,
                                                            106.1,
                                                        ],
                                                        "y": [
                                                            "Other",
                                                            "Russian Ruble",
                                                            "Chinese Yuan",
                                                            "Canadian Dollar",
                                                            "Hungarian Forint",
                                                            "Brazilian Real",
                                                            "Mexican Peso",
                                                            "Polish Zloty",
                                                            "Czech Koruna",
                                                            "Norwegian Krone",
                                                            "Swedish Krona",
                                                            "US Dollar",
                                                        ],
                                                        "marker": {"color": "#119dff"},
                                                        "orientation": "h",
                                                    }
                                                ],
                                                "layout": {
                                                    "title": "",
                                                    "width": 300,
                                                    "xaxis": {
                                                        "type": "linear",
                                                        "range": [
                                                            -62.13380540229584,
                                                            164.54230264362104,
                                                        ],
                                                        "ticks": "outside",
                                                        "title": "",
                                                        "mirror": False,
                                                        "nticks": 6,
                                                        "showgrid": False,
                                                        "showline": True,
                                                        "zeroline": False,
                                                        "autorange": True,
                                                        "ticksuffix": "%",
                                                    },
                                                    "yaxis": {
                                                        "type": "category",
                                                        "range": [-0.5, 11.5],
                                                        "title": "",
                                                        "showgrid": True,
                                                        "showline": False,
                                                        "zeroline": False,
                                                        "autorange": True,
                                                    },
                                                    "height": 300,
                                                    "margin": {
                                                        "b": 40,
                                                        "l": 100,
                                                        "r": 5,
                                                        "t": 40,
                                                        "pad": 0,
                                                    },
                                                },
                                            }
                                        ),
                                        html.H6("Credit Allocation (%)"),
                                        dcc.Graph(
                                            figure={
                                                "data": [
                                                    {
                                                        "uid": "a8c61b",
                                                        "name": "GS Strategic<br>Absolute<br>Return<br>Bond II<br>Portfolio",
                                                        "type": "bar",
                                                        "xsrc": "jackp:17802:62c223",
                                                        "x": [
                                                            "0",
                                                            "100",
                                                            "0",
                                                            "0",
                                                            "0",
                                                            "0",
                                                            "0",
                                                            "0",
                                                            "0",
                                                            "0",
                                                            "0",
                                                            "0",
                                                            "0",
                                                        ],
                                                        "ysrc": "jackp:17802:d66b98",
                                                        "y": [
                                                            "Derivatives",
                                                            "Cash",
                                                            "NR",
                                                            "D",
                                                            "C",
                                                            "CC",
                                                            "CCC",
                                                            "B",
                                                            "BB",
                                                            "BBB",
                                                            "A",
                                                            "AA",
                                                            "AAA",
                                                        ],
                                                        "marker": {"color": "#c2ebff"},
                                                        "visible": True,
                                                        "orientation": "h",
                                                    },
                                                    {
                                                        "uid": "f84602",
                                                        "name": "3 Month<br>USD Libor",
                                                        "type": "bar",
                                                        "xsrc": "jackp:17802:4a6d89",
                                                        "x": [
                                                            "0",
                                                            "12.6",
                                                            "0.6",
                                                            "0.1",
                                                            "0.2",
                                                            "1.1",
                                                            "2.3",
                                                            "1.6",
                                                            "2.1",
                                                            "1.9",
                                                            "31.8",
                                                            "3.7",
                                                            "42.1",
                                                        ],
                                                        "ysrc": "jackp:17802:d66b98",
                                                        "y": [
                                                            "Derivatives",
                                                            "Cash",
                                                            "NR",
                                                            "D",
                                                            "C",
                                                            "CC",
                                                            "CCC",
                                                            "B",
                                                            "BB",
                                                            "BBB",
                                                            "A",
                                                            "AA",
                                                            "AAA",
                                                        ],
                                                        "marker": {"color": "#119dff"},
                                                        "orientation": "h",
                                                    },
                                                ],
                                                "layout": {
                                                    "title": "",
                                                    "width": 301,
                                                    "xaxis": {
                                                        "type": "linear",
                                                        "range": [0, 100],
                                                        "ticks": "outside",
                                                        "title": "",
                                                        "nticks": 11,
                                                        "showgrid": False,
                                                        "showline": True,
                                                        "autorange": False,
                                                        "ticksuffix": "%",
                                                    },
                                                    "yaxis": {
                                                        "type": "category",
                                                        "range": [
                                                            -0.5,
                                                            12.592783505154639,
                                                        ],
                                                        "title": "",
                                                        "showgrid": True,
                                                        "autorange": True,
                                                        "ticksuffix": "",
                                                    },
                                                    "height": 300,
                                                    "legend": {
                                                        "x": 0.14793708706277642,
                                                        "y": 0.6998496240601503,
                                                        "bgcolor": "rgba(255, 255, 255, 0)",
                                                        "bordercolor": "rgba(68, 68, 68, 0)",
                                                    },
                                                    "margin": {
                                                        "b": 40,
                                                        "l": 60,
                                                        "r": 0,
                                                        "t": 10,
                                                        "pad": 0,
                                                    },
                                                },
                                            }
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                    className="subpage",
                ),
            ],
            className="page",
        ),
    ]
)

if __name__ == "__main__":
    app.server.run()
