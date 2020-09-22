
import .sqlite3_helper
import .rabbitmq_helper

def getHelper():
    return sqlite3_helper.getHelper()

def getQueueHelper():
    return rabbitmq_helper.getHelper()    