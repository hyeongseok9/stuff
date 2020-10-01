# grid search sarima hyperparameters
import grid_search_async

# create a set of sarima configs to try
def sarima_configs(seasonal=[0]):
    models = list()
    # define config lists
    p_params = [0, 1, 2]
    d_params = [0, 1]
    q_params = [0, 1, 2]
    t_params = ['n','c','t','ct']
    P_params = [0, 1, 2]
    D_params = [0, 1]
    Q_params = [0, 1, 2]
    m_params = seasonal
    # create config instances
    for p in p_params:
        for d in d_params:
            for q in q_params:
                for t in t_params:
                    for P in P_params:
                        for D in D_params:
                            for Q in Q_params:
                                for m in m_params:
                                    cfg = [(p,d,q), (P,D,Q,m), t]
                                    models.append(cfg)
    return models


if __name__ == '__main__':
    # data split
    n_test = int(1000)
    
    cfg_list = sarima_configs()
    # grid search
    result_list = []
    url="http://193.122.126.51:8081/cpmyard.cvs"
    for cfg in cfg_list:
        result = grid_search_async.grid_search.delay(url, cfg, n_test)
        result_list.append(result)

    for result in result_list:
        (cfg, error) = result.get()
        print(cfg, error)
    