import json
import websocket
import time
try:
    import thread
except ImportError:
    import _thread as thread
import threading

# step_a 관련 함수
def on_open_a(ws):
    def run_a(*args):
        subscribe_message = {
            "method": "SUBSCRIBE",
            "params":
            [
            "btcusdt@depth5@100ms",
            "btcusdt@trade"
            ],
            "id": 1
            }
        ws.send(json.dumps(subscribe_message))
        time.sleep(10)
        ws.close()
    thread.start_new_thread(run_a,())

def on_message_a(ws, message):    
    result=json.loads(message)
    if 'bids' in result:
        file.write('btcusdt@orderbook, '+'bids:'+str(result['bids'])+', asks:'+str(result['asks'])+'\n')
    if 'p' in result:
        file.write('btcusdt@trade, '+'p:'+result['p']+', q:'+result['q']+'\n')

def on_close_a(ws):
    print("closed connection")


# step_b 관련 함수
def on_message_b(ws, message):
    result = json.loads(message.decode('utf-8'))
    if 'orderbook_units' in result:
        file.write(('btckrw@orderbook,  '+str(result['orderbook_units']))+'\n')

def on_error_b(ws, error):
    print(error)

def on_close_b(ws):
    print("close")

def on_open_b(ws):
    def run_b(*args):
        sendData = '[{"ticket":"UNIQUE_TICKET"},{"type":"orderbook","codes":["KRW-BTC"]}]'
        ws.send(sendData)
        time.sleep(10)

        ws.close()
    thread.start_new_thread(run_b, ())



# step_a,b,c 실행 함수
def step_a():
    ws = websocket.WebSocketApp('wss://stream.binance.com:9443/ws', on_open=on_open_a, on_message=on_message_a, on_close=on_close_a)
    ws.run_forever()

def step_b():
    ws = websocket.WebSocketApp("wss://api.upbit.com/websocket/v1",on_message = on_message_b, on_error = on_error_b, on_open=on_open_b)
    ws.run_forever()

def step_c():
    th_a=threading.Thread(target=step_a,args=())
    th_b=threading.Thread(target=step_b,args=())
    th_a.start()
    th_b.start()
    th_a.join()
    th_b.join()


#step_a
file = open('stream-data-binance.txt','w')
step_a()
file.close()

# step_b
file = open('stream-data-upbit.txt','w')
step_b()
file.close()

# step_c
file = open('stream-data-multi.txt','w')
step_c()
file.close()

