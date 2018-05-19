import json

from db_manager import *

from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape
from weasyprint import HTML, CSS
from time import asctime
from collections import Counter
from consts import *

def take_compliance(compliance): #not used
    return{
        "id"          :  compliance[0],
        "status"      :  compliance[1],
        "description" :  compliance[3],
        "title"       :  compliance[4],
        "requirements":  compliance[5],
        "transport"   :  compliance[6]}
    

def make_report(scan_time):
    db = get_db()
    cursor = db.cursor()
    
    #Count statuses occurances
    comp_status = cursor.execute("SELECT status FROM scandata").fetchall()
    checks_counts = Counter([status[0][2:-2] for status in comp_status])
    checks_counts.update([i for i in STATUSES.values()])
    for check in checks_counts: checks_counts[check] -=1

    compliances = cursor.execute('''
        SELECT * FROM scandata AS t1
        INNER JOIN control AS t2
        ON t1.id=t2.id''')#.fetchall()
    columns_names = map(lambda x: x[0], cursor.description)
    compliances = [dict(zip(columns_names, compliance)) for compliance in cursor.fetchall()]
    transports_used = set()
    comps_data = list()

    for compliance in compliances:
        transports_used.add(compliance['transport'])
        '''comps_data.append({"id"          :compliance['id'],
                           "title"       :compliance['title'],
                           "description" :compliance['description'],
                           "requirements":compliance['requirements'],
                           "status"      :compliance['status']})'''
    
    #Transport data
    with open("./env.json") as f: env_conf = json.load(f)
    transports_data = {transport: env_conf['transports'][transport.upper()] for transport in transports_used}
    for transport in transports_data.values(): transport.pop('password')
    
    render_data = {
        'scan_date'   : asctime(),
        'scan_time'   : scan_time,
        'system_host' : env_conf['host'],
        'total_checks': len(compliances),
        'transports'  : transports_data,
        'comp_data'   : compliances
        }
    render_data.update(checks_counts)
    #print(render_data)
    #report
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    rendered_template = env.get_template('index.html').render(data = render_data)
    styles = [CSS(filename='./templates/style.css')]
    HTML(string = rendered_template).write_pdf('report.pdf', stylesheets=styles)
    db.close()

