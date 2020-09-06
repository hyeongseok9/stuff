from flask import Flask, render_template, send_file, request
from datetime import datetime
import persistence
import io
import imgutil

app = Flask(__name__)

import LocalConf

@app.route('/')
def list_photos():
    conn = persistence.create_or_open_db(LocalConf.DB_PATH)
    allphotos = persistence.allPhotos(conn)
    photos = []
    for p in allphotos:
        photos.append({"Id": p[0], "Taken": p[3], "Width": p[1], "Height": p[2]})
    conn.close()
    return render_template('index.html',photos= photos)

@app.route('/photo/<photoid>/view')
def photo_view(photoid):
    width = int(request.args.get('width'))*40
    height = int(request.args.get('height'))*40

    return render_template('photo_view.html',photoid= photoid, width= width, height= height )

@app.route('/photo/<photoid>/stream')
def photo_stream(photoid):
    conn = persistence.create_or_open_db(LocalConf.DB_PATH)
    photo = persistence.getphoto(conn, photoid)
    timestamp = photo.Timestamp
    
    image_binary = imgutil.resize(photo.Picture, photo.Width, photo.Height, 40)
    
    conn.close()
    return send_file(
        image_binary,
        mimetype='image/png',
        as_attachment=True,
        attachment_filename='%s.jpg' % timestamp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
