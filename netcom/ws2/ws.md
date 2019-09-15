## message
```
{'sender':'fei', 'event':'send', 'channel':'group1_schoolA', 'msg':'I will follow it'}

```

## server
``` 
/home/cf/project/pydb/T3/network/netcom/ws2
[root@cfBareos ws2]# python3 python-websocket-server/server.py 
jj test jj
jjjj
('127.0.0.1', 60456)
New client connected and was given id 1
{'id': 1, 'handler': <websocket_server.websocket_server.WebSocketHandler object at 0x7f6c0e7e5828>, 'address': ('127.0.0.1', 60456)} <socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 9001), raddr=('127.0.0.1', 60456)> <websocket_server.websocket_server.WebsocketServer object at 0x7f6c18512d68>
Client(1) said: Hello
Client(1) said: {"event": "ping", "subscription": {"name": "com"}}
```  

## client
```  
/home/cf/project/pydb/T3/network/netcom/ws2
[root@cfBareos ws2]# python3 websocket-client/examples/send_json.py 9001
{"event": "ping", "subscription": {"name": "com"}}
--- request header ---
GET / HTTP/1.1
Upgrade: websocket
Connection: Upgrade
Host: localhost:9001
Origin: http://localhost:9001
Sec-WebSocket-Key: 3piByNBYRs2nB0OE4Uxu0Q==
Sec-WebSocket-Version: 13


-----------------------
--- response header ---
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: 9HyTV237OO0jt+w0gsXRdEc9oGQ=
-----------------------
Hey all, a new client has joined us
send: b"\x81\x85?')(wBEDP"
send: b'\x81\xb2]"\x18\x94&\x00}\xe28Ll\xb6g\x02:\xe44L\x7f\xb6q\x02:\xe7(@k\xf7/Kh\xe04Mv\xb6g\x02c\xb63Cu\xf1\x7f\x188\xb6>Mu\xb6 _'
Connection is already closed.
### closed ###
```  
