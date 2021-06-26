import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd 
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# app.layout = html.Div([
# 	html.H6("Change the value in the text box to see callback in action"),
# 	html.Div(["Input: ", dcc.Input(id="my-input", value='initital value', type='text')]),
# 	html.Br(),
# 	html.Div(id='my-output'),
# ])

# @app.callback(
# 	Output(component_id='my-output', component_property='children'),
# 	Input(component_id='my-input', component_property='value')
# )

# def update_output_div(input_value): 
# 	return 'Output: {}'.format(input_value)

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv")

app.layout = html.Div([
	dcc.Graph(id='graph-with-slider'),
	dcc.Slider(
		id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
	)
])

@app.callback(
	Output('graph-with-slider', 'figure'),
	Input('year-slider', 'value')
)

def update_figure(selected_year):
	filtered_df = df[df.year == selected_year]
	fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)
	fig.update_layout(transition_duration=500)
	return fig
if __name__ == "__main__":
	app.run_server(debug=True)