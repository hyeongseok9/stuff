from scipy import interpolate
import matplotlib.pyplot as plt
import struct, io
import numpy as np
from matplotlib import cm

def resize(samples, imgwidth, imgheight, ratio):
    temps = []
    while samples:
        row = samples[:imgwidth*4]
        frow = struct.unpack_from('<'+'f'*imgwidth, row)
        temps+=frow
        samples = samples[imgwidth*4:]


    x = np.linspace(0, imgwidth * ratio, imgwidth)
    y = np.linspace(0, imgheight * ratio, imgheight)
    z = np.reshape(temps,(imgheight, imgwidth ))
    f = interpolate.interp2d(x, y, z, kind='cubic')

    xnew = np.linspace(0, imgwidth * ratio, imgwidth * ratio)
    ynew = np.linspace(0, imgheight * ratio, imgheight * ratio)
    znew = f(xnew, ynew)
    
    plt.imshow(znew, cmap=cm.gist_heat)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    return buf
