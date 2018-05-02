#!/usr/bin/env python3
import os
import json
import importlib
import re
from sshPT import *
from test_db import *


DB_NAME = 'control.db'


if __name__ == '__main__':
    prepare_db()
    for script in [name for name in os.listdir('./scripts') if re.match(".+\.py",name)]:
        result = importlib.import_module("scripts." + script.split('.')[0]).main()
        add_control(int(script[:3]), result)
