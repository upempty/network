import struct
HeaderType = {
             'id': 'I ',
             'receiver': 'I ',
             'sender': 'I ',
             'len': 'I ' 
            }


BodyType = {
             'type': 'I ',
             'id': 'I ',
             'desc': '6s '
            }



class Message:
    def __init__(self, id, receiver, sender, len):
        self._header = b''
        self._id = id
        self._receiver = receiver
        self._sender = sender
        self._len = len
        self._payload = b''

    def pack_header(self, endianness=">"):
        fmt = endianness
        for i in HeaderType:
            fmt += HeaderType[i]
        print ('pack fmt={}'.format(fmt))
        self._header = struct.pack(fmt, self._id, self._receiver, self._sender, self._len)
        print ('pack header {}'.format(self._header))
        return self._header

    def unpack_header(self, header, endianness=">"):
        fmt = endianness
        for i in HeaderType:
            fmt += HeaderType[i]
        print ('unpack fmt={}'.format(fmt))
        self._id, self._receiver, self._sender, self._len = struct.unpack(fmt, header)
        print ('unpack header {} {} {} {}'.format(self._id, self._receiver, self._sender, self._len))


    def pack_payload(self, endianness=">"):
        self._payload = b''
        return self._payload


    def pack_msg(self, endianness=">"):
        m = self.pack_header() + self.pack_payload()
        return m
 
    def unpack_msg(self, endianness=">"):
        pass
   
    def get_header(self):
        pass 

    def get_payload(self):
        pass 

