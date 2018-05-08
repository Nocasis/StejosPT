#!/usr/bin/env python3
import os
import json
import importlib
import re

from time import time
from transport import *
from db_manager import *
from reporting import *

DB_NAME = 'control.db'


if __name__ == '__main__':
    start_time = time()
    prepare_db()
    for script in [name for name in os.listdir('./scripts') if re.match(".+\.py",name)]:
        result = importlib.import_module("scripts." + script.split('.')[0]).main()
        add_control(int(script[:3]), result)
    time_passed = int(time() - start_time)
    scan_time = "{}h {}m {}s".format(time_passed//3600, time_passed%3600//60, time_passed%60)
    make_report(scan_time)
    
