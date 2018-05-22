#!/usr/bin/env python3
import os
import importlib
import re

from time import time
from db_manager import *
from reporting import *
from sys import exit

if __name__ == '__main__':
    start_time = time()
    try:
        prepare_db()
    except:
        exit("ERROR: prepare_db")
    for script in [name for name in os.listdir('./scripts') if re.match(".+\.py",name)]:
        try:
            result = importlib.import_module("scripts." + script.split('.')[0]).main()
            add_control(int(script[:3]), result)
        except:
            print("Script {} is down.".format(script.split('.')[0]))
            pass
    time_passed = int(time() - start_time)
    scan_time = "{}h {}m {}s".format(time_passed//3600, time_passed%3600//60, time_passed%60)
    make_report(scan_time)
    
