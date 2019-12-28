#coding: utf-8
import socket
import struct
import types
import sys
import message

tcpServerSocket=socket.socket()
host = "127.0.0.1"
port=18000
tcpServerSocket.bind((host,port))
tcpServerSocket.listen(5)

c, addr = tcpServerSocket.accept()       
print (addr)
while True:
    print ('ready to recv:')
    st=c.recv(16)
    print (st)
    print ('received:', st)
    m = message.Message(8,8,8,8)
    m.unpack_header(st)
    c.close()
    sys.exit()
