#!/usr/bin/python3
from transport import *
import pytest

def test_init():
    SSHTransport("localhost", 3222, "root", "ssh_test")
    with pytest.raises(TransportConnectionError):
        SSHTransport("localhost", 32222, "root", "lol")
        SSHTransport("localhost", 3222,"root", "kek")

def test_cat_file():
    SSHTransport("localhost", 3222, "root", "ssh_test").cat_file("test")
    with pytest.raises(TransportError):
        SSHTransport("localhost", 3222, "root", "ssh_test").cat_file("test_1234")  

def test_exec():
    SSHTransport("localhost", 3222, "root", "ssh_test").exec("ls -la")
    
def test_get_transport_instance():
    get_transport_instance("ssh", "localhost", 3222, "root", "ssh_test")
    with pytest.raises(UnknownTransport):
        get_transport_instance('sssh', "localhost", 3222, "root", "ssh_test")
