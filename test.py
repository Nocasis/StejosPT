#!/usr/bin/env python3
import json
from transport import *
import pymysql.cursors

DB_NAME = 'control.db'


if __name__ == '__main__':
    t_sql = get_transport_instance("SQL")
    a = t_sql.sqlexec("describe test;")
    print(a)
