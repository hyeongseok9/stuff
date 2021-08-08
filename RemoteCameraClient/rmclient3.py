import time

import zmq
import matplotlib.pyplot as plt
from PIL import Image
import interpolate3
from matplotlib import cm
import numpy as np
from pprint import pprint
remoteaddr = "localhost:5555"

context = zmq.Context()
print ("Connecting server")
socket = context.socket(zmq.REQ)
socket.connect("tcp://{}".format(remoteaddr))
fig = plt.figure()
for i in range(1,13):
    socket.send(b'take photo')

    message = socket.recv()

    temps = []
    import struct
    samples = message
    #print('samples:', len(samples), samples.__class__)
    imgwidth = 32
    imgheight= 24
    rows = []
    while samples:
        row = samples[:imgwidth*4]
        rows.append(row)
        samples = samples[imgwidth*4:]
    for row in reversed(rows):
        #print('row length', len(row))
        #print('f'*imgwidth)
        frow = struct.unpack_from('<'+'f'*imgwidth, row)
        temps+=frow

    from scipy import interpolate

    x = np.linspace(0, 32 * 40, imgwidth)
    y = np.linspace(0, 24 * 40, imgheight)
    z = np.reshape(temps,(imgheight, imgwidth ))
    f = interpolate.interp2d(x, y, z, kind='cubic')

    xnew = np.linspace(0, 32 * 40, imgwidth * 40)
    ynew = np.linspace(0, 24 * 40, imgheight * 40)
    znew = f(xnew, ynew)

    fig.add_subplot(3,4,i)
    plt.imshow(znew, cmap=cm.gist_heat)
plt.show()



