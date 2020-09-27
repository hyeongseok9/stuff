# grid search sarima hyperparameters
from math import sqrt
from multiprocessing import cpu_count
from warnings import catch_warnings
from warnings import filterwarnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from pandas import read_csv
import time


# one-step sarima forecast
def sarima_forecast(history, config):
    order, sorder, trend = config
    # define model
    model = SARIMAX(history, order=order, seasonal_order=sorder, trend=trend, enforce_stationarity=False, enforce_invertibility=False)
    # fit model
    model_fit = model.fit(disp=False)
    # make one step forecast
    yhat = model_fit.predict(len(history), len(history))
    return yhat[0]

# root mean squared error or rmse
def measure_rmse(actual, predicted):
    return sqrt(mean_squared_error(actual, predicted))

# split a univariate dataset into train/test sets
def train_test_split(data, n_test):
    return data[:-n_test], data[-n_test:]

# walk-forward validation for univariate data
def walk_forward_validation(data, n_test, cfg):
    predictions = list()
    # split dataset
    train, test = train_test_split(data, n_test)
    # seed history with training dataset
    history = [x for x in train]
    # step over each time-step in the test set
    total = len(test)
    total_process_started = time.time()
    for i in range(total):
        # fit model and make forecast for history
        yhat = sarima_forecast(history, cfg)
        # store forecast in list of predictions
        predictions.append(yhat)
        # add actual observation to history for the next loop
        history.append(test[i])
    # estimate prediction error
    error = measure_rmse(test, predictions)
    return error

# score a model, return None on failure
def score_model(data, n_test, cfg, debug=False):
    result = None
    # convert config to a key
    key = str(cfg)
    # show all warnings and fail on exception if debugging
    if debug:
        result = walk_forward_validation(data, n_test, cfg)
    else:
        # one failure during model validation suggests an unstable config
        try:
            # never show warnings when grid searching, too noisy
            with catch_warnings():
                filterwarnings("ignore")
                result = walk_forward_validation(data, n_test, cfg)
        except Exception as e:
            print('score_model', e)
            error = None
    # check for an interesting result
    if result is not None:
        print(' > Model[%s] %.3f' % (key, result))
    return (key, result)


from celery import Celery
from celery.utils.log import get_task_logger

# Create the celery app and get the logger
celery_app = Celery('tasks', broker='pyamqp://api:kP4zZ6vD@193.122.126.51/hsnam_0927',
    backend='rpc://',
)
logger = get_task_logger(__name__)


@celery_app.task
def grid_search(url, cfg, n_test):
    import requests
    from datetime import datetime
    parser=lambda x: datetime.fromtimestamp(int(x)/1000)
    from io import StringIO
    buf = StringIO(requests.get(url).text)
    series = read_csv(buf, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)

    data = series.values
    
    score = score_model(data, n_test, cfg) 
    
    return score


if __name__ == '__main__':
    # define dataset
    from datetime import datetime
    parser=lambda x: datetime.fromtimestamp(int(x)/1000)
    series = read_csv('cpmyard.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)

    data = series.values
    
    print(data[:10])
    # data split
    n_test = int(len(data) * 0.34)
    print(n_test)
    # model configs
    cfg_list = sarima_configs()
    # grid search
    scores = grid_search(data, cfg_list, n_test, parallel=False)
    print('done')
    # list top 3 configs
    for cfg, error in scores[:3]:
        print(cfg, error)