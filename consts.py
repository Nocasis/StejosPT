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

STATUSES = {1: 'STATUS_COMPLIANT', 
            2: 'STATUS_NOT_COMPLIANT', 
            3: 'STATUS_NOT_APPLICABLE', 
            4: 'STATUS_ERROR', 
            5: 'STATUS_EXCEPTION'}

RETURN_VALUE = {value:key for key, value in STATUSES.items()}
