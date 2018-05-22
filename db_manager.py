import sqlite3
import json
from sys import exit
from consts import *

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
            data = cursor.execute("SELECT EXISTS(SELECT * FROM scandata WHERE id = ?)",(str(id_),))
            if (data.fetchone()[0] == True):
                cursor.execute('''UPDATE control SET id = ?, description = ?, title = ?, requirement = ?, transport = ?''',((int(id_), str(descr), str(title), str(requirement), str(transport))))
            else:
                cursor.execute('''INSERT INTO control
                (id, description, title, requirement, transport) 
         VALUES (?, \"?\", \"?\", \"?\", \"?\")''',(int(id_), str(descr), str(title), str(requirement), str(transport)))
    db.commit()
    db.close()

def add_control(id_, status):
    try:
        db = get_db()
        cursor = db.cursor()
    except:
        exit()
    complaint_data = cursor.execute("SELECT * FROM control WHERE id=?",(str(id_),)).fetchone()
    id_, descr, title, requirement, transport = complaint_data
    data = cursor.execute("SELECT EXISTS(SELECT * FROM scandata WHERE id = ?)",(str(id_),))
    if (data.fetchone()[0] == True):
        cursor.execute("UPDATE scandata SET status = ?",(str([STATUSES[status]]),))
    else:
        cursor.execute("INSERT OR IGNORE INTO scandata(id, status) VALUES(?,\"?\")",(int(id_), str([STATUSES[status]])))
    db.commit()
    db.close()
