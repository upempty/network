import socket
import struct
import types

class Connector:
    def __init__(self):
        self._handle = "xxxcreate socket open connect"
        self.connected = False
     
    def open(self, serverip='127.0.0.1', port=18000, timeout=50.0):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(timeout)
        try:
            self.sock.connect((serverip, port))
        except socket.error:
            print ("faild to connect {}:{}".format(serverip, port))
            raise socket.error
     
        self.connected = True 

    def reconn(self):
        pass
    
    def close(self):
        if self.connected == True:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            self.connected = False
    #aligned with 4bytes like I unsigned int format data
    def send(self, msg):
        bys = b'' 
        for i in msg: 
            if isinstance(i, types.StringTypes) == False:
                bys += struct.pack("I", socket.htonl(i))
            else:
                bys += i
        self.sock.send(bys)
        return 0

    def receive(self, timeout):
        self.sock.settimeout(timeout)
        msg = self.sock.recv(2048)
        return msg
