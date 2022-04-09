import dash 
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import pandas as pd 
import sqlite3


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(id='container', children=[
    html.Div(id="tweet_table", children=[
        dcc.Interval(
        id='table_update',
        interval=1*1000,
    ),
    ])
])



@app.callback(
    Output('tweet_table', 'children'),
    [Input("table_update", "n_intervals")]
)
def table(table_update):
    con = sqlite3.connect("twitter.db", check_same_thread=False)
    cur = con.cursor()

    df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE '%a%' ORDER BY create_at DESC LIMIT 10", con)
    return generate_table(df)


if __name__ == '__main__':
    app.run_server(debug=True)