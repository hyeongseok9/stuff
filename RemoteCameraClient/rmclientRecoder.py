import time

import zmq
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import cm
import numpy as np
from pprint import pprint
import persistence, photo
import time
from io import BytesIO

remoteaddr = "localhost:5555"
context = zmq.Context()
print ("Connecting server")
socket = context.socket(zmq.REQ)

socket.connect("tcp://{}".format(remoteaddr))

import LocalConf

imgwidth = 32
imgheight = 24

def upsideDown(samples):
    rows = []
    while samples:
        row = samples[:imgwidth*4]
        rows.append(row)
        samples = samples[imgwidth*4:]
    reversed_samples = BytesIO()
    for row in reversed(rows):
        reversed_samples.write(row)

    return reversed_samples.getvalue()

while True:
    for i in range(5):
        socket.send(b'take photo')
        message = socket.recv()
    socket.send(b'take photo')
    message = socket.recv()
    message = upsideDown(message)
    photo_path = photo.takepicture(LocalConf.PHOTO_PREFIX)
    conn = persistence.create_or_open_db(LocalConf.DB_PATH)
    persistence.add_photo(conn, message, imgwidth, imgheight, photo_path)
    time.sleep(LocalConf.SLEEP_TIME)



