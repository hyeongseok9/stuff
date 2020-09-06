import time, os
import picamera
from datetime import datetime
from PIL import Image

def takepicture(prefix):
    with picamera.PiCamera() as cam:
        now = datetime.now()
        filename = str(int(time.time()*1000)) + '.png'
        filepath = os.path.join(prefix,str(now.year), str(now.month), str(now.day), filename)
        directory = os.path.split(filepath)[0]
        if not os.path.exists(directory):
            os.makedirs(directory)
        cam.capture(filepath)
        im = Image.open(filepath)
        im.rotate(90).save(filepath)
        

        return filepath


if __name__ == '__main__':
    takepicture('/home/pi')
