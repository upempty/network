import websocket
import _thread as thread
import time
import sys
import json
from websocket._abnf import ABNF
#export PYTHONPATH=$PYTHONPATH:/home/cf/project/pydb/ws2/websocket-client:/home/cf/project/pydb/ws2/python-websocket-server

port = sys.argv[1]

AA = json.dumps({
	#"event": "subscribe",
	"sender": "fei",
	"event": "send",
	"channel": "ping",
	"msg": "i will follow it",
	#"subscription": {"name": "com"}
     })
print (AA)

def on_message(ws, message):
    print ('on msg')    
    print ('msg:', message)

#def on_data(ws, message, ABNF.OPCODE_TEXT, 1):


def on_error(ws, error):
    print (error)

def on_close(ws):
    print ("### closed ###")

def on_open(ws):
    def run(*args):
        while True:
            time.sleep(5)
            ws.send(AA)
        time.sleep(1)
        print ("### closedjjjjjjjjjjjjjjj ###")
        ws.close()
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:" + port + "/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
