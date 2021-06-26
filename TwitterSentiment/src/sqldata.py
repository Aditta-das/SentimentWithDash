import pandas as pd 
import sqlite3
import numpy as np 

con = sqlite3.connect("twitter.db", check_same_thread=False)
cur = con.cursor()

# # query_selection = cursor.execute('SELECT * FROM sentiment').fetchall()

# df = pd.DataFrame(query_selection, columns=["id", "timestamp", "tweet", "score", "sentiment"])
# # df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
# # df = df.sort_values(by="timestamp", ascending=False)
# # print(df)
# # df = pd.read_sql("SELECT * FROM sentiment", con)
# # print(df)
df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE '%a%' ORDER BY create_at DESC LIMIT 100", con)
# df.sort_values(by="create_at", inplace=True)
df["mov_avg"] = df['score'].rolling(int(len(df)/5)).mean()
df["date"] = pd.to_datetime(df["create_at"], unit="ms")
df.set_index("date", inplace=True)
df = df.resample('1s').mean()
df.dropna(inplace=True)
# df["mov_avg"] = df['score'].rolling(5).mean()
# df.set_index("date", inplace=True)
# # df = df[["mov_avg"]]
# # df = df.resample('1s').mean()
# # df.dropna(inplace=True)
# # # df = df["mov_avg"]
# df = df.to_dict()
print(df)
sentiment_color = {
	'Positive': '#228C7B',
	'Negative': '#F30E5C',
	'Neutral': '#F6C523'
}

def senti_color(senti):
	if senti == "Positive":
		return sentiment_color["Positive"]
	elif senti == "Negative":
		return sentiment_color["Negative"]
	else:
		return sentiment_color["Neutral"]

# a = senti_color([(d[4], i) for d in df.values.tolist() for i in d])
# print(a)
# print(df.values.tolist())
# for e in df.values.tolist():
# 	print(e)
# c = [senti_color((d[4])) for d in df.values.tolist()[:10]]
# print(c)
# print(senti_color(i for i in b))

# for j in b:
	# print(j)
# print(df.iloc[0]["sentiment"])
# print(df['sentiment'])
# for d in df.values.tolist():
# 	print(d[4])
# df = pd.DataFrame()
# for idx in range(10):
# ndf = pd.DataFrame()
# data  = {f'{df.columns[0]}': df.create_at, f'{df.columns[3]}': df.score}
# ndf = ndf.append(data, ignore_index=True)
# print(ndf)


# search_term = 'a'
# df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY create_at DESC LIMIT 10", con, params=(search_term + '*',))

# print(df)

# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import dash_table
# import pandas as pd
# import numpy as np

# app = dash.Dash(__name__)

# def getData():
#     df = pd.DataFrame()
#     for idx in range(10):
#         data  = {'x': np.random.random(1)[0], 'y': np.random.random(1)[0]}
#         df = df.append(data, ignore_index=True)
#     return df.to_dict('records')

# tblcols=[{'name': 'x', 'id': 'x'},
#          {'name': 'y', 'id': 'y'}, ]

# app.layout = html.Div([
#       html.H4('Dashboard'),
#       dcc.Interval('graph-update', interval = 1000, n_intervals = 0),
#       dash_table.DataTable(
#           id = 'table',
#           data = getData(),
#           columns=tblcols)])

# @app.callback(
#         dash.dependencies.Output('table','data'),
#         [dash.dependencies.Input('graph-update', 'n_intervals')])
# def updateTable(n):
#      return getData()

# if __name__ == '__main__':
#      app.run_server(debug=False)