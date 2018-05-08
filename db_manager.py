import sqlite3
import json
CONTROL =   '''
            CREATE TABLE IF NOT EXISTS control(
            id INTEGER PRIMARY KEY, 
            title TEXT,
            description TEXT,
            requirement TEXT,
            transport TEXT)
            '''
SCANDATA =  '''
            CREATE TABLE IF NOT EXISTS scandata(
            id INTEGER PRIMARY KEY,
            status INTEGER)
            '''
DB_NAME = 'control.db'


STATUSES = dict(enumerate(
        ["STATUS_COMPLIANT",
         "STATUS_NOT_COMPLIANT",
         "STATUS_NOT_APPLICABLE",
         "STATUS_ERROR",
         "STATUS_EXCEPTION"]
        ,1))

def get_db():
    return sqlite3.connect(DB_NAME)

def prepare_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(CONTROL)
    cursor.execute(SCANDATA)
    db.commit()
    with open('controls.json') as f: 
        for record in json.load(f):
            id_, descr, title, requirement, transport  = tuple(record)
            cursor.execute('''INSERT OR IGNORE INTO control
                (id, description, title, requirement, transport) 
         VALUES ({}, \"{}\", \"{}\", \"{}\", \"{}\")'''.format(id_, str(descr), str(title), str(requirement), str(transport)))
    db.commit()
    db.close()

def add_control(id_, status):
    db = get_db()
    cursor = db.cursor()
    complaint_data = cursor.execute("SELECT * FROM control WHERE id={}".format(id_)).fetchone()
    id_, descr, title, requirement, transport = complaint_data
    data = cursor.execute("SELECT EXISTS(SELECT * FROM scandata WHERE id = {})".format(id_))
    if (data.fetchone()[0] == True):
        cursor.execute("UPDATE scandata SET status = \"{}\"".format(str([STATUSES[status]])))
    else:
        cursor.execute("INSERT OR IGNORE INTO scandata(id, status) VALUES({},\"{}\")".format(id_, str([STATUSES[status]]) ))
    db.commit()
    db.close()
