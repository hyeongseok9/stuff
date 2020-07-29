import time
import zmq
import pb_pb2

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()
    mp = pb_pb2.MeasurePayload()
    mp.LoadFromString(message)
    
    for a in mp.Tag:
        print('Tag:', a.Key, a.Value)
    
    for a in mp.IntField:
        print('IntField:', a.Key, a.Value)

    for a in mp.FloatField:
        print('FloatField:', a.Key, a.Value)
