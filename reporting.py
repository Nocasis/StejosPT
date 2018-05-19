import json

from db_manager import *

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML, CSS
from time import asctime
from collections import Counter
from consts import *
    
def get_status_count(cursor):
    comp_status = cursor.execute("SELECT status FROM scandata").fetchall()
    checks_counts = Counter([status[0][2:-2] for status in comp_status])
    checks_counts.update([i for i in STATUSES.values()])
    for check in checks_counts: checks_counts[check] -=1
    return checks_counts

def get_compliances(cursor):
    cursor.execute('''
        SELECT * FROM scandata AS t1
        INNER JOIN control AS t2
        ON t1.id=t2.id''')
    columns_names = map(lambda x: x[0], cursor.description)
    compliances = [dict(zip(columns_names, compliance)) for compliance in cursor.fetchall()]
    return compliances

def get_transport_data(compliances, env_conf):
    transports_used = set()
    for compliance in compliances: transports_used.add(compliance['transport'])
    transports_data = {transport: env_conf['transports'][transport.upper()] for transport in transports_used}
    for transport in transports_data.values(): transport.pop('password')
    return transports_data

def render_data(scan_time, env_conf, compliances, transports_data):
    return {
        'scan_date'   : asctime(),
        'scan_time'   : scan_time,
        'system_host' : env_conf['host'],
        'total_checks': len(compliances),
        'transports'  : transports_data,
        'comp_data'   : compliances
        }

def render_report(rendered_data):
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    rendered_template = env.get_template('index.html').render(data = rendered_data)
    styles = [CSS(filename='./templates/style.css')]
    HTML(string = rendered_template).write_pdf('report.pdf', stylesheets=styles)
    
def make_report(scan_time):
    db = get_db()
    cursor = db.cursor()
    checks_counts = get_status_count(cursor)
    compliances = get_compliances(cursor)
    
    with open("./env.json") as f: env_conf = json.load(f)
    
    transports_data = get_transport_data(compliances, env_conf)
    rendered_data = render_data(scan_time, env_conf, compliances, transports_data)
    rendered_data.update(checks_counts)
    render_report(rendered_data)
    
    db.close()

