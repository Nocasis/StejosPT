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
