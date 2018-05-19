from transport import *

def main():
    try:
        get_transport_instance('SSH').cat_file('test')
    except TransportIOError:
        return 2
    except TransportConnectionError:
        return 4
    except TransportError:
        return 5
    return 1
