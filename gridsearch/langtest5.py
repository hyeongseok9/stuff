
from pandas import read_csv
from statsmodels.tsa.statespace.sarimax import SARIMAX

def sarima_forecast(history, config, predict_points):
    order, sorder, trend = config
    # define model
    model = SARIMAX(history, order=order, seasonal_order=sorder, trend=trend, enforce_stationarity=False, enforce_invertibility=False)
    # fit model
    model_fit = model.fit(disp=False)
    # make one step forecast
    yhat = model_fit.forecast(steps= predict_points)
    #yhat = model_fit.predict(len(history), predict_points)
    return yhat
    
from datetime import datetime
from pandas import read_csv
parser=lambda x: datetime.fromtimestamp(int(x)/1000)
series = read_csv('cpmyard.min.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
datalength = len(series)
series2 = series[:int(datalength/2)]

data = series2.values
config = [(1, 1, 1), (1, 1, 1,60*24), 'ct']
predictions = sarima_forecast(data, config, 60*5).tolist()
#print('forecast:', len(predictions), predictions)
realdata = series[int(datalength/2):]
from datetime import datetime
clocks = [datetime.utcfromtimestamp(dt64.astype(int)/1000000000)  for dt64 in realdata.index.values]
#print(clocks[:10] )
import plotly.graph_objects as go
fig = go.Figure(data=go.Scatter(x = clocks, y=predictions))
fig.show()