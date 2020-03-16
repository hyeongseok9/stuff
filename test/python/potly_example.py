import plotly.express as px

df = px.data.gapminder().query("continent=='Oceania'")
from pprint import pprint

pprint(df.shape)
pprint(df)
fig = px.line(df, x="year", y="lifeExp", color='country')
fig.show()