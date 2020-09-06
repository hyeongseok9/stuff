from influxdb import InfluxDBClient
import os


def getClient(host=os.environ.get('INFLUXDB_HOST', 'localhost'), port=8086):
    user = 'root'
    password = 'root'
    dbname = 'cpu_perf'
    dbuser = 'hsnam'
    dbuser_password = 'hsnam123'

    client = InfluxDBClient(host, port, user, password, dbname)

    try:
        print("Create database: " + dbname)
        client.create_database(dbname)

        print("Create a retention policy")
        client.create_retention_policy('awesome_policy', '3d', 3, default=True)

        print("Switch user: " + dbuser)
        client.switch_user(dbuser, dbuser_password)
    except Exception as e:
        print(e)

    return client

def put(measurement = None, time = '', tags = {}, fields = {}):
    client = getClient()
    jsonbody = [
        { 
            'measurement': measurement,
            'time' : time,
            'tags' : tags,
            'fields' : fields,
        }
    ]
    client.write_points(jsonbody)

def query(query)    :
    client = getClient()
    result = client.query(query)

    return result