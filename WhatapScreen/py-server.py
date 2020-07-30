import time
import zmq
import pb_pb2

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
    for a in mp.tags:
        print('Tag:', a.key, a.value)
    
    for a in mp.intFields:
        print('IntField:', a.key, a.value)

    for a in mp.floatFields:
        print('FloatField:', a.key, a.value)
    print("Process Complete")
    socket.send(b"ok")