
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
          

def set_xxx(netcom, field2):
    request = InfoReq()
    request.transactionId = 1
    request.type = 0
    request.id = domain
 
    req = Message(1011, address, 0, request)    


class InfoReq(Payload):
    def __init__(self, param = None):
        self.msgId = 1011
        self.transactionId = 0
        self.type = 0
        self.id = 0
        Message.Payload.__init__(self, param)

    def pack(self):
        self.appendU32(self.transactionId)
        self.appendU32(self.type)
        self.appendU32(self.id)
        return self._payload

    def unpack(self, data):
        self.transactionId = self.getU32(data, 0)
        self.type = self.getU32(data, 4)
        self.id = self.getU32(data, 8)



