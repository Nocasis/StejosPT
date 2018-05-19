import paramiko
import socket
import json
import pymysql
from paramiko.ssh_exception import AuthenticationException, NoValidConnectionsError, SSHException
from pymysql.err import InternalError, OperationalError, ProgrammingError

_config = None

def set_config(config):
    with open('env.json', 'w') as f: json.dump(config, f, indent=4, sort_keys=True)

def get_config():
    global _config
    if not _config:
        with open('env.json','r') as f: _config = json.load(f)
    return _config

def get_default(transport_name):
    _config_json = get_config()
    return{
        "host"    :  _config_json['host'],
        "port"    :  _config_json['transports'][transport_name]['port'],
        "login"   :  _config_json['transports'][transport_name]['login'],
        "password":  _config_json['transports'][transport_name]['password']}
        
class TransportError(Exception):#MAYBE TODO
    def __init___(self,dErrorArguments):
        Exception.__init__(self,"TransportError {0}".format(dErrArguments))
        self.dErrorArguments = dErrorArguements

class UnknownTransport(TransportError):
    def __init___(self,dErrorArguments):
        Exception.__init__(self,"UnknownTransport {0}".format(dErrArguments))
        self.dErrorArguments = dErrorArguements


class TransportConnectionError(TransportError):
    def __init___(self,dErrorArguments):
        Exception.__init__(self,"TransportConnectionError {0}".format(dErrArguments))
        self.dErrorArguments = dErrorArguements

class TransportIOError(TransportError):
    def __init___(self,dErrorArguments):
        Exception.__init__(self,"TransportIOError {0}".format(dErrArguments))
        self.dErrorArguments = dErrorArguements
        
class MySQLError(TransportError):
    def __init___(self,dErrorArguments):
        Exception.__init__(self,"MySQLError {0}".format(dErrArguments))
        self.dErrorArguments = dErrorArguements

def get_transport_instance(transport_name, host = None, port = None, login = None, password = None):
    if not host or not port or not login or not password:
        config   = get_default(transport_name)
        host     = config['host']
        port     = config['port']
        login    = config['login']
        password = config['password']
        
    available = {'SSH':SSHTransport,
                 'SQL':SQLTransport
                 }
    transport = available.get(transport_name.upper(), None)
    if transport:
        return transport(host, port, login, password)
    raise UnknownTransport("UnknownTransport: {}".format(transport_name))

def check_db(dbname):
    t_sql = get_transport_instance("SQL")
    return t_sql.sqlexec("SHOW databases LIKE '{}';".format(dbname))
    
def check_table(tablename):
    t_sql = get_transport_instance("SQL")
    if t_sql.sqlexec("SHOW tables LIKE '{}';".format(tablename)):
        return t_sql.sqlexec("SELECT COUNT(*) FROM {}".format(tablename))['COUNT(*)']

class SSHTransport():
    def __init__(self ,host, port, login, password):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())   #knows_hosts
            self.client.connect(hostname=host, username=login, password = password, port=port)
        except socket.error:
            raise TransportConnectionError("Unable connect to port {} on {}".format(port, host))
        except NoValidConnectionsError:
            raise TransportConnectionError("Unable connect to port {} on {}".format(port, host))
        except BadHostKeyException:
            raise TransportConnectionError("Host key could not be verified")
        except AuthenticationException:
            raise TransportConnectionError("Unable to authenticate with login:{}".format(login))
        except SSHException:
            raise TransportConnectionError("Unable to connect to port {} on {}".format(port, host))

    
    def __del__(self):
        self.client.close()

    def close(self):
        self.client.close()
    
    def exec(self, command, debug = False):
        try:
            if debug:
                return self.client.exec_command(command) #Так удобнее будет работать с stdin, stdout, stderr
            else:
                stdin, stdout, stderr = self.client.exec_command(command) 
                data = stdout.readlines() + stderr.readlines()      #data = stdout.read() + stderr.read()
                data = [line[:-1] for line in data]
                for line in data:
                    print (line)
                return data
        
        except SSHException:
            raise TransportConnectionError("SSHException with command")
        
    def get_file(self, file_name, get_as = 'get_file'):
        try:
            ftp = self.client.open_sftp()
            ftp.get(file_name, get_as)
            ftp.close()
        except FileNotFoundError:
            print ("Error: file not found")
        except TypeError:
            print ("Error: not enough arguments")
    
    def put_file(self, file_name, put_as = 'put_file'):
        try:
            ftp = self.client.open_sftp()
            ftp.put(file_name,put_as)
            ftp.close()
        except FileNotFoundError:
            print ("Error: file not found")
        except TypeError:
            print ("Error: not enough arguments")
    
    def cat_file(self, path):
        try:
            return self.client.open_sftp().open(path).read()
        except SSHException:
            raise TransportError("Failed connection")
        except IOError:
            raise TransportError("Cant open file by path {}".format(path))
        
        
class SQLTransport():
    def __init__(self, hostname, port, login, password):
        db = 'transport'
        try:
            self.connection = pymysql.connect(host=hostname, user=login, 
                                            port = port, password = password, 
                                            db = db, charset = 'utf8', 
                                            cursorclass=pymysql.cursors.DictCursor, 
                                            unix_socket=False)
        except InternalError: #Temp TODO
            raise TransportConnectionError("Unknown database {}".format(db))
        except OperationalError:
            raise TransportConnectionError("Can't connect to MySQL server on '{}'@'{}' with given password".format(login,hostname))
        except ProgrammingError:
            raise TransportConnectionError("Unable to connect to port {} on {}".format(port, host))
    
    def sqlexec(self, quary):
        with self.connection.cursor() as cursor:
            cursor.execute(quary)
            self.connection.commit()
            return cursor.fetchall()
        return None
    
    def __del__(self):
        self.connection.close()
        
    def close(self):
        self.connection.close()
    
