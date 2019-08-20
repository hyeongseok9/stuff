import time

import zmq
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import cm
import numpy as np
from pprint import pprint
import persistence
import time
remoteaddr = "localhost:5555"
context = zmq.Context()
print ("Connecting server")
socket = context.socket(zmq.REQ)

socket.connect("tcp://{}".format(remoteaddr))

import LocalConf

imgwidth = 32
imgheight = 24

while True:
    for i in range(5):
        socket.send(b'take photo')
        message = socket.recv()
    socket.send(b'take photo')
    message = socket.recv()
    conn = persistence.create_or_open_db(LocalConf.DB_PATH)
    persistence.add_photo(conn, message, imgwidth, imgheight)
    time.sleep(LocalConf.SLEEP_TIME)



