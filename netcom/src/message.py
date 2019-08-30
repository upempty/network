
HeadType = {
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
    def __init__(self, id, receiver, sender, payload, len):
        self._header = []
        self._id = id
        self._receiver = receiver
        self._sender = sender
        self._len = len
        self._payload = payload

    def pack_header(self, endianness=">"):
        fmt = endianness
        for i in HeaderType:
            fmt += HeaderType[i]
        self._header = struct.pack(fmt, self._id, self._receiver, self._sender, self._len)

    def unpack_header(self, header, endianness=">"):
        fmt = endianness
        for i in HeaderType:
            fmt += HeaderType[i]
        self._id, self._receiver, self._sender, self._len = struct.unpack(fmt, header)


    def pack_body(self, endianness=">"):
        pass
    '''
    def pack_header(self, endianness=">"):
        fmt = '> I'
        self._header.append(struct.pack(fmt, self._id))
        self._header.append(struct.pack(fmt, self._receiver))
        self._header.append(struct.pack(fmt, self._sender))
        self._header.append(struct.pack(fmt, self._len))
        return self._header
    '''


    def pack_msg(self, endianness=">"):
        m = self.pack_header() + self.pack_boday()
        return m
        pass
 
    def unpack_msg(self, endianness=">"):
        pass
   
    def get_header(self):
        pass 

    def get_payload(self):
        pass 

