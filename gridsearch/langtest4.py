from pandas import read_csv

import plotly.graph_objects as go
series = read_csv('cpmyard.min.csv')
print('read ', len(series))
data = [go.Scatter(x = series['DATE'], y = series['YardCpu'],
                  name='Yard CPU Two Weeks')]


import chart_studio.plotly as py
py.iplot(data, filename='jupyter-basic_line')