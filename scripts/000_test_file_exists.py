from transport import *
from consts import RETURN_VALUE

def main():
    try:
        get_transport_instance('SSH').cat_file('test')
    except TransportIOError:
        return RETURN_VALUE['STATUS_NOT_COMPLIANT']
    except TransportConnectionError:
        return RETURN_VALUE['STATUS_ERROR']
    except TransportError:
        return RETURN_VALUE['STATUS_EXCEPTION']
    return RETURN_VALUE['STATUS_COMPLIANT']
