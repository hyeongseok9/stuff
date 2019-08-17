

def create_or_open_db(db_file):
    db_is_new = not os.path.exists(db_file)
    conn = sqlite3.connect(db_file)
    if db_is_new:
        print 'Creating schema'
        sql = '''create table if not exists THERMAL_PICTURES(
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Picture BLOB,
        Width INTEGER,
        Height INTEGER,
        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);'''
        conn.execute(sql) # shortcut for conn.cursor().execute(sql)
    else:
        print 'Schema exists\n'
    return conn


def add_photo(conn, photob, width, height):
    conn.execute('INSERT INTO t (Picture, Width, Height) VALUES (?)', (buffer(photob), width, height))
    conn.commit()
