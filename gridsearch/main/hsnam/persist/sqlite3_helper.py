
class PersistHelper(object):
    def __init__(self):
        self.__conn = self.__connect()

    def __connect(self):
        import sqlite3
        conn = sqlite3.connect('test.db')

        return conn

    

def getHelper():
    return PersistHelper()