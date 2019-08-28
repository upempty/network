
class Transceiver:
    def __init__(self, connector):
        self._conn = connector
    
    def send_msg(self, message):
        if isinstance(message, Message) == TRUE:
            msg = message.pack_msg(endianness='>')
        else:
            print ('to support message')
        self._conn.send(msg)

    def receive_msg(self, timeout):
        raw = self.__conn.receive(timeout)
        msgs = []
        while len(raw) > 0:
            msg = Message()
            msg.parse_header(raw, ">")
            msg._payload = raw[16 : msg._payloadsize+16]
            msgs.append(msg)
        return msgs[0]
          
            
