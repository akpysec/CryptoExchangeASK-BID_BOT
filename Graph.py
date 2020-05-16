from datetime import datetime
import sqlite3
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_auth

database = "btc_usdt_db.sqlite"

USERNAME_PASSWORD_PAIRS = [['name', 'pass'], ['another_name', 'another_pass']]

app = dash.Dash()

auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

app.layout = html.Div([
    html.Div([
        dcc.Graph(id='live-update-graph', children='Ticker', style={'width': 1200}),

        dcc.Interval(
            id='interval-component',
            interval=4000,  # = 4 seconds
            n_intervals=0,
        )])
])


def db_values_pull(db: str):
    con = sqlite3.connect(db)
    start_end = con.execute("SELECT MIN(time) AS First, MAX(time) AS Last FROM cage")
    distinct = con.execute("SELECT DISTINCT name FROM cage")
    markets_in_db = list()
    for m in distinct:
        markets_in_db.append(m[0])
    result = start_end.fetchone()
    start_date = str(datetime.fromtimestamp(result[0]))[0:16]
    end_date = str(datetime.fromtimestamp(result[1]))[0:16]
    con.close()

    return start_date, end_date, markets_in_db


print(f"Snoopy DB-{database.upper()} has records between dates: "
      f"{db_values_pull(db=database)[0]} - {db_values_pull(db=database)[1]}")


def read_db():
    con = sqlite3.connect(database)
    df = pd.read_sql_query(f"SELECT * FROM cage ORDER BY id DESC LIMIT 10000", con)  # ORDER BY time DESC LIMIT 10
    normal = [datetime.fromtimestamp(d) for d in df['time']]
    df['time'] = normal
    con.close()
    return df


@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    df = read_db()
    col = [col for col in df.columns]
    coin = ''.join(col[-1:]).rstrip('Ask')

    bids = [go.Scatter(x=df[df['name'] == mark]['time'],
                       y=df[df['name'] == mark]['USDBid'],
                       mode='lines',
                       # marker=dict(
                       #      color='rgb(102, 102, 255)'),
                       name=mark + ':BID') for mark in sorted(df['name'].unique())]

    asks = [go.Scatter(x=df[df['name'] == mark]['time'],
                       y=df[df['name'] == mark]['USDAsk'],
                       mode='lines',
                       # marker=dict(
                       #     color='rgb(255, 102, 102)'),
                       name=mark + ':ASK') for mark in sorted(df['name'].unique())]

    data = [*bids, *asks]

    return {
        'data': data[0:],
        'layout': {
            'title': 'BID:ASK Tickers',
            'xaxis': dict(title='TIMELINE'),
            'yaxis': dict(title=coin),
            'hovermode': 'closest',
            'legend': {'x': 1, 'y': 0},
            'uirevision': True,
        }
    }


if __name__ == '__main__':
    app.run_server(port=5426)
