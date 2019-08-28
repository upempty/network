
class Message:
    def __init__(self, id, receiver, sender, payload):
        self._header = []
        self._id = id
        self._receiver = receiver
        self._sender = sender
        self._payload = payload

    #def parse_header(self, msg, ">"):
    def parse_header(self, msg, endian):
        pass

    def pack_msg(self, endianness=">"):
        pass
 
    def unpack_msg(self, endianness=">"):
        pass
   
    def get_header(self):
        pass 

    def get_payload(self):
        pass 
