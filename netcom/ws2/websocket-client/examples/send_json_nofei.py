import websocket
import _thread as thread
import time
import sys
import json

#export PYTHONPATH=$PYTHONPATH:/home/cf/project/pydb/ws2/websocket-client:/home/cf/project/pydb/ws2/python-websocket-server

port = sys.argv[1]

AA = json.dumps({
	#"event": "subscribe",
	"sender": "dongdong",
	"event": "send",
	"channel": "1",
	"msg": "i will follow it2-1",
	#"subscription": {"name": "com"}
     })
print (AA)

def on_message(ws, message):
    print (message)

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
