
import sqlite3,os

def getConn(dbname=os.getenv('DBFILE',"test_ex.db")):
    conn = sqlite3.connect(dbname)
    return conn

def save_insert_values(sqlquery, params=None, sqlfile=os.getenv('DUMPFILE', 'dump.sql')):
    with open(sqlfile, 'a+') as f:
        if params:
            sqlquery = sqlquery.split('values')[0] +' values '
            f.write(sqlquery)
        
            new_params = []
            isFirst = True
            for x in params:
                if not isFirst:
                    f.write(', ')
                f.write('(')
                isFirst2 = True
                for p in x:
                    if not isFirst2:
                        f.write(', ')    
                    if type(p) == str:
                        f.write("'"+p+"'")
                    else:
                        f.write(str(p))
                    isFirst2 = False
                f.write(')')
        
                isFirst = False
            
        f.write(';\n')


def save_query(sqlquery, params=None, sqlfile=os.getenv('DUMPFILE', 'dump.sql')):
    with open(sqlfile, 'a+') as f:
        if params:
            sqlquery = sqlquery.replace("?", "{}")
            new_params = []
            for x in params:
                if type(x) == str:
                    new_params.append("'"+x+"'")
                else:
                    new_params.append(x)
            #print('save_query:', sqlquery, new_params)
            sqlquery = sqlquery.format(*new_params)
        f.write(sqlquery)
        f.write(';\n')



def create_all_tables(): 
    conn = getConn()
    
    cur = conn.cursor()
    # 수집 데이터 종류
    create_table_item="""CREATE TABLE IF NOT EXISTS item (
        id integer PRIMARY KEY AUTOINCREMENT,
        item_name text NOT NULL,
        item_type text not null,
        pcode integer,
        oid integer 
    );""" 
    cur.execute(create_table_item)
    save_query(create_table_item)
    # 수집 데이터
    create_table_history="""CREATE TABLE IF NOT EXISTS history (
        item_id integer,
        clock integer ,
        value float 
    );"""
    cur.execute(create_table_history)
    save_query(create_table_history)
    # 연결닫기
    conn.close()


def upsert_item(item_name, item_type, pcode=0, oid=0):
    with getConn() as c:
        cur = c.cursor()
        upsert_query = """INSERT INTO item (item_name, item_type, pcode, oid) 
    SELECT '{}', '{}' , '{}', '{}'
    WHERE NOT EXISTS(SELECT 1 FROM item WHERE item_name = ? AND item_type = ? and pcode = ? and oid = ?)""".format(item_name, item_type, pcode, oid)

        cur.execute(upsert_query, (item_name, item_type, pcode, oid))
        save_query(upsert_query, params=(item_name, item_type, pcode, oid))
        select_query = """select id from item where item_name = ? AND item_type = ? and pcode=? and oid=?"""

        cur = cur.execute(select_query, (item_name, item_type, pcode, oid))
        
        return cur.fetchall()[0][0]


def store_process(pcode=0, oid=0, process=None):
    
    process_name= process['name']
    process_name_item_id = upsert_item(process_name, 'process_name', pcode=pcode, oid=oid)
    process_hash= process['hash']
    process_hash_item_id = upsert_item(str(process_hash), 'process_hash', pcode=pcode, oid=oid)
    process_cpu_item_id = upsert_item('process_cpu', 'process_cpu', pcode=pcode, oid=oid)
    process_rss_item_id = upsert_item('process_rss', 'process_rss', pcode=pcode, oid=oid)
    
    
    process_count_item_id = upsert_item('process_count', 'process_count', pcode=pcode, oid=oid)
    
    process_cpu= process['cpu']
    process_rss= process['rss']
    process_net= process['net']
    process_file= process['file']
    process_count= process['count']
    process_clock= process['clock']

    process_name_list = [(process_name_item_id, x, process_hash)  for x in process_clock]
    process_hash_list = [(process_hash_item_id, x, process_hash)  for x in process_clock]

    process_cpu_list = []
    process_rss_list = []
    process_net_list = []
    process_file_list = []
    process_count_list = []
    for i in range(len(process_clock)):
        process_cpu_list.append((process_cpu_item_id, process_clock[i], process_cpu[i]))
        process_rss_list.append((process_rss_item_id, process_clock[i], process_rss[i]))
        if process_net:
            k = sorted(process_net.keys())[0]
            process_net_item_id = upsert_item(k, 'process_net', pcode=pcode, oid=oid)
            process_net_list.append((process_net_item_id, process_clock[i], hash(k)))
        if process_file:
            k = sorted(process_file.keys())[0]
            process_file_item_id = upsert_item(k, 'process_file', pcode=pcode, oid=oid)
            process_file_list.append((process_file_item_id, process_clock[i], hash(k)))
        process_count_list.append((process_count_item_id, process_clock[i], process_count[i]))

        
    # from pprint import pprint
    # pprint(process_name_list)

    with getConn() as c:
        cur = c.cursor()
        cur.executemany('INSERT OR REPLACE INTO history (item_id, clock, value) values(?,?,?);', process_name_list)
        save_insert_values('INSERT OR REPLACE INTO history (item_id, clock, value) values(?,?,?);', params= process_name_list)
        cur.executemany('INSERT OR REPLACE INTO history (item_id, clock, value) values(?,?,?);', process_hash_list)
        save_insert_values('INSERT OR REPLACE INTO history (item_id, clock, value) values(?,?,?);', params= process_hash_list)
        cur.executemany('INSERT OR REPLACE INTO history (item_id, clock, value) values(?,?,?);', process_cpu_list)
        save_insert_values('INSERT OR REPLACE INTO history (item_id, clock, value) values(?,?,?);', params= process_cpu_list)
        cur.executemany('INSERT OR REPLACE INTO history (item_id, clock, value) values(?,?,?);', process_rss_list)
        save_insert_values('INSERT OR REPLACE INTO history (item_id, clock, value) values(?,?,?);', params= process_rss_list)
        cur.executemany('INSERT OR REPLACE INTO history (item_id, clock, value) values(?,?,?);', process_net_list)
        save_insert_values('INSERT OR REPLACE INTO history (item_id, clock, value) values(?,?,?);', params= process_net_list)
        cur.executemany('INSERT OR REPLACE INTO history (item_id, clock, value) values(?,?,?);', process_file_list)
        save_insert_values('INSERT OR REPLACE INTO history (item_id, clock, value) values(?,?,?);', params= process_file_list)
        cur.executemany('INSERT OR REPLACE INTO history (item_id, clock, value) values(?,?,?);', process_count_list)
        save_insert_values('INSERT OR REPLACE INTO history (item_id, clock, value) values(?,?,?);', params= process_count_list)
        
create_all_tables()

if __name__ == '__main__':
    import testdata

    store_process(pcode=111, oid=22, process=testdata.p1)
    