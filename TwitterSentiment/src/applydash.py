import dash
import dash_core_components as dcc 
import dash_html_components as html 
import plotly.express as px
import pandas as pd 


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

color = {
	"background": '#111111',
	'text': '#7FDBFF',
}

df = pd.DataFrame({
	"Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
	})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# app.layout = html.Div(children=[
# 	html.H1(children="Hello Dash"), 
# 	html.Div(children='''
# 		Dash: A web application framework for python
# 		'''),
# 	dcc.Graph(
# 		id='example-graph',
# 		figure=fig
# 		)
# 	])

fig.update_layout(
	plot_bgcolor=color["background"],
	paper_bgcolor=color["background"],
	font_color=color["text"]
)

app.layout = html.Div(style={
	'background': color['background']},
	children=[
		html.H1(
			children="Hello World", 
			style={
				'text-align': 'center',
				'color': color["text"]
			}
		),

		html.Div(children="Dash : A web framework", style={
				'text-align': 'center',
				'color': color['text']
			}),
		dcc.Graph(
			id='example-graph-2',
			figure=fig
		)
	])


if __name__ == "__main__":
	app.run_server(debug=True)