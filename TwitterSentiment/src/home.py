import sqlite3
import os, sys
import time
import pandas as pd
from threading import Timer, Lock
import plotly
import plotly.express as px
import plotly.graph_objs as go
import dash 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


con = sqlite3.connect("twitter.db", check_same_thread=False)
external_stylesheets = ['https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css']

sentiment_color = {
	'Positive': '#B6FFEA',
	'Negative': '#FFB3B3',
	'Neutral': '#FCE2AE'
}

scatter_color = {
	'scatter': '#393E46',
	'line': '#00ADB5'
}

def senti_color(senti):
	if senti == "Positive":
		return sentiment_color["Positive"]
	elif senti == "Negative":
		return sentiment_color["Negative"]
	else:
		return sentiment_color["Neutral"]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
	html.Div(className="container", children=[html.H2('Twitter Sentiment', style={'color': '#595959', 'text-align': 'center', 'font-weight': 'bold', 'font-family': 'Courier', 'font-weight': '700',}),
	html.H5('Save The World | Peace & Happy', style={'text-align': 'center', 'font-weight': 'bold', 'letter-spacing': '2px', 'font-family': 'Courier'}),
	html.Div(className="col-md-12", children=[html.H3('Search Here:', style={'text-align': 'center', 'font-weight': 'bold', 'letter-spacing': '2px', 'font-family': 'Courier'}),
		# dcc.Input(id="search_term", className="form-control", value="war", type="text"),
		
	html.Div(className="col-md-12 mt-5", children=[html.Div(className="row", 
		children=[
			dcc.Input(id="search_term", className="form-control", value="neymar", type="text"),
			dcc.Graph(id='indicator-graphic', animate=False),
			dcc.Interval(
				id="indicator_graphic_update",
				interval=1*1000,
			)
			]),
		]),
		html.Div(className="container", 
			children=[html.Div(id='tweet_table'),
			# dcc.Input(id="search_term_table", className="form-control", value="a", type="text"),
			dcc.Interval(
				id='table_update',
				interval=2*1000,
				n_intervals=2
			)
		]),
	]),
	]),
])

# table generate
def generate_table_data(df, max_rows=10):
	return html.Table(className="table table-striped", children=[
		html.Thead(
			html.Tr([html.Th(col) for col in df.columns])
		),
		html.Tbody([
			html.Tr(children=[
				html.Td(df.iloc[i][col]) for col in df.columns
			], style={'font-weight': '500', 'background-color': senti_color(df.iloc[i]["sentiment"])}) for i in range(min(len(df), max_rows))
		])
	])

@app.callback(
	Output(component_id="tweet_table", component_property="children"),
	[Input(component_id='search_term', component_property='value'), 
	Input(component_id="table_update", component_property="n_intervals")]
)
def update_tweet_live(search_term, table_update):
	# if search_term:
	df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY create_at DESC LIMIT 10", con, params=('%'+search_term +'%',))
	# df = pd.read_sql("SELECT * FROM sentiment_ft WHERE tweet MATCH ? ORDER BY create_at DESC LIMIT 10", con, params=(search_term_table+'*',))
	# df = pd.read_sql("SELECT score.* FROM sentiment_fts fts LEFT JOIN sentiment ON fts.rowid = score.id WHERE fts.sentiment_fts MATCH ? ORDER BY fts.rowid DESC LIMIT 10", con, params=(search_term_table+'*',))
	# df = pd.DataFrame(data, columns=["id", "timestamp", "tweet", "score", "sentiment"])
	# df["mov_avg"] = df['score'].rolling(int(len(df)/5)).mean()
	df["date"] = pd.to_datetime(df["create_at"], unit="ms")
	# df.set_index('date', inplace=True)
	df = df[["date", "tweet", "score", "sentiment"]]
	return generate_table_data(df, max_rows=10)


@app.callback(
			Output('indicator-graphic', 'figure'),
			[Input(component_id='search_term', component_property='value'), 
			Input('indicator_graphic_update', 'n_intervals')]
)
def update_tweet_live_scatter_plot(search_term, indicator_graphic_update):
	try:
		con = sqlite3.connect("twitter.db", check_same_thread=False)
		cur = con.cursor()
		df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY create_at DESC LIMIT 1000", con ,params=('%' + search_term + '%',))
		# df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE '%a%' ORDER BY create_at DESC LIMIT 1000", 
		# 		con)
		df.sort_values(by="create_at", inplace=True)
		df["mov_avg"] = df['score'].rolling(int(len(df)/5)).mean()
		df["date"] = pd.to_datetime(df["create_at"], unit="ms")
		df.set_index("date", inplace=True)
		df = df.resample('1s').mean()
		# df = df[["mov_avg"]]
		df.dropna(inplace=True)
		# df = df.mov_avg.resample('1s')
		X = df.index
		Y = df.mov_avg.values
		# df = pd.DataFrame(data, columns=["id", "timestamp", "tweet", "score", "sentiment"])
		# df["timestamp"] = pd.to_datetime(df["create_at"], unit="ms")
		# df = df[["timestamp", "tweet", "score", "sentiment"]]
		# df.set_index('timestamp', inplace=True)
		# X = df.index[-100:]
		# Y = df.score.values[-100:]
		data = go.Scatter(
			x=X,
			y=Y,
			name='Scatter',
			mode= 'lines+markers',
			marker_color=scatter_color['scatter'],
			line = dict(color=scatter_color['line'], width=4),
		)

		return {'data': [data], 'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                    yaxis=dict(range=[min(Y),max(Y)]),
                                                    showlegend=False,
                                                    height=500,
                                                    title=f"Searching For : {search_term}")}

	except Exception as e:
		print(e)


if __name__ == "__main__":
	app.run_server(debug=True)