
config = None

def setConfig(_config):
    global config
    config = _config

class KombuHelper(object):
    def __init__(self):
        self.__connect()

    def __connect(self):
        rabbit_url = config.rabbitmq_url
        conn = Connection(rabbit_url)
def getHelper():
    return KombuHelper()