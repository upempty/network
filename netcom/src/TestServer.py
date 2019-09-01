#coding: utf-8
import socket
import struct
import types
import sys
import message

tcpServerSocket=socket.socket()#创建socket对象
host = "127.0.0.1"#获取本地主机名
port=18000#设置端口
tcpServerSocket.bind((host,port))#将地址与套接字绑定，且套接字要求是从未被绑定过的
tcpServerSocket.listen(5)#代办事件中排队等待connect的最大数目

c, addr = tcpServerSocket.accept()       
print (addr)
while True:
    #建立客户端连接,接受connection，返回两个参数，c是该connection上可以发送和接收数据的新套接字对象
    #addr是与connection另一端的套接字绑定的地址
    print ('jj')
    st=c.recv(16)
    print (st)
    print ('addd:', st)
    m = message.Message(8,8,8,8)
    m.unpack_header(st)
    #c.send(str)
    #套接字在垃圾收集garbage-collected时会自动close
    #close关闭该connection上的资源但不一定马上断开connection
    #想要立即断开connection，要先调用shutdown再close
    c.close() # 关闭连接
    sys.exit()
