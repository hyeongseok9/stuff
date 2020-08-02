from influxdb import InfluxDBClient

def getClient():
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
    except Exception, e:
        print(e)

    return client

def put(measurement = None, time = 0, tags = {}, fields = {}):
    client = getClient()
    jsonbody = [
        { 
            'measurement': measurement,
            'time' : time,
            'tags' : tags,
            'fields' : fields,
        }
    ]
    client.write_points(json_body)