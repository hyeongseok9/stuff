import os, sqlite3

def create_or_open_db(db_file):
    db_is_new = not os.path.exists(db_file)
    conn = sqlite3.connect(db_file)
    if db_is_new:
        print('Creating schema')
        sql = '''create table if not exists THERMAL_PICTURES(
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Picture BLOB,
        Width INTEGER,
        Height INTEGER,
        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        RealPhotoPath TEXT );'''
        conn.execute(sql) # shortcut for conn.cursor().execute(sql)
    else:
        print('Schema exists\n')
    return conn


def add_photo(conn, photob, width, height):
    conn.execute('INSERT INTO THERMAL_PICTURES (Picture, Width, Height) VALUES (?,?,?)', (photob, width, height))
    conn.commit()

def allPhotos(conn):
    cur = conn.cursor()
    cur.execute("SELECT Id, Width, Height, Timestamp, RealPhotoPath FROM THERMAL_PICTURES")
 
    rows = cur.fetchall()
 
    
    return rows

def getphoto(conn, photoid):
    cur = conn.cursor()
    cur.execute("SELECT Picture, Width, Height, Timestamp, RealPhotoPath  FROM THERMAL_PICTURES where Id=?", (photoid,))
 
    (picture, width, height, timestamp, real_photo_path) = cur.fetchone()
    
    class _photo:
        def __init__(self, picture, width, height, timestamp, real_photo_path):
            self.Picture = picture
            self.Width = width
            self.Height = height
            self.Timestamp = timestamp
            self.RealPhotoPath = real_photo_path

    return _photo(picture, width, height, timestamp, real_photo_path)

