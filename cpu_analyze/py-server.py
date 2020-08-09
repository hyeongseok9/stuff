
import time
import zmq
import pb_pb2
import tsdbhelper
from datetime import datetime
import threading
import json

def listenZeroMQ():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        #  Wait for next request from client
        print('waiting for message')
        message = socket.recv()
        print(' message received ', len(message), message.__class__, message)
        mp = pb_pb2.MeasurePayload()
        mp.ParseFromString(message)
        print("load Complete")
        tags = {}
        for a in mp.tags:
            #print('Tag:', a.key, a.value)
            tags[a.key] = a.value
        
        fields = {}
        for a in mp.intFields:
            print('IntField:', a.key, a.value)
            fields[a.key] = a.value

        for a in mp.floatFields:
            print('FloatField:', a.key, a.value)
            fields[a.key] = a.value
        tsdbhelper.put(measurement = 'cpu_frequency', \
            time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z'), \
                tags = tags, fields = fields)
        print("Process Complete")
        socket.send(b"ok")

def listenAPI():
    import http.server as SimpleHTTPServer
    import socketserver as SocketServer
    import dateutil.parser
    PORT = 5000

    class GetHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type','text/json')
            self.end_headers()
            
            categories= []
            series = {}
            for rr in tsdbhelper.query('select * from cpu_frequency;'):
                for r in rr:
                    categories.append(int( dateutil.parser.parse(r['time']).timestamp()*1000))
                    for k, v in r.items():
                        if k not in  ('ip', 'hostname', 'time'):
                            if k not in series:
                                series[k] = []
                            if v == None:
                                series[k].append(0)
                            else:
                                series[k].append(v)
            self.wfile.write(json.dumps(dict(categories = categories, series = series)).encode())
            return

    while True:
        try:
            httpd = SocketServer.TCPServer(("", PORT), GetHandler)

            print("serving at port", PORT)
            httpd.serve_forever()
        except Exception as e:
            print(e)
            time.sleep(1)

if __name__ == '__main__':
    threads = []
    t = threading.Thread(target=listenZeroMQ)
    t.setDaemon(True)
    t.start()
    threads.append(t)

    t = threading.Thread(target=listenAPI)
    t.setDaemon(True)
    t.start()
    threads.append(t)

    for t in threads:
        t.join()
