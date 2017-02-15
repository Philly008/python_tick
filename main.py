import threading
import tushare as ts
import time
import thread
import websocket
from websocket import create_connection

# print(ts.__version__)
#ts.get_k_data('600000', ktype='W', autype='hfq')

# df = ts.get_tick_data('600848',date='2014-01-09')
# print(df.head(10))
# print(ts.get_k_data('600000', ktype='W', autype='hfq'))

#print(ts.get_today_all())
#not suppost cn
# print('a')
# time.sleep(2)
# print('b')

#map of tick points;
Tick_Point={}
Today_All={}
# d['00']=1
# print(d)
# print(ts.get_realtime_quotes('000581').price[0])
# print(float(24.490))
def tick_change(tick,interval):
    price1=ts.get_realtime_quotes(tick).price[0]
    time.sleep(interval)
    price2 = ts.get_realtime_quotes(tick).price[0]
    return  float(price2) - float(price1)

def tick_up(tick,interval):
    change=tick_change(tick,interval)
    # print('tick',change)
    point = tick_point(change)
    # print(point)
    return point

def tick_point(change):
    if change>0:
        return 1
    elif change<0:
        return -1
    else:
        return 0

def getTickPoint(tick):
    return Tick_Point.get(tick,0)

def setTickPoint(tick,newPoints):
    Tick_Point[tick] = newPoints

def update_tick_point(tick,point):
    setTickPoint(tick,getTickPoint(tick)+point)
    return getTickPoint(tick)

# print(update_tick_point('d', 1))
# print(update_tick_point('d', -1))

 # print(ts.get_realtime_quotes('000581').price)
# print(tick_up('000581',2))

def update_tick_for(tick,interval):
    update_tick_point(tick, tick_up(tick,interval))
    print('for', tick, Tick_Point[tick])
    ws_send(tick+'|'+'%d' % Tick_Point[tick])
    update_tick_for(tick,interval)

def update_tick_today_for():
    todayAll = ts.get_today_all()['code']
    #print(todayAll['code'])
    # pandas.core.series.Series
    # print(type(todayAll))
    # print(todayAll[0])
    # print(todayAll.values)

    for tick in todayAll.values:
        # print(tick)
        # thread.start_new_thread(update_tick_for,(tick, 2))
        # update_tick_for(tick, 2)

        t = threading.Thread(target=update_tick_for, name='LoopThread',args=(tick, 10))
        t.start()

        # t.join()
# update_tick_for('000581',2)
# print(ts.get_today_all())

# main
# update_tick_today_for()

# t = threading.Thread(target=update_tick_for, name='LoopThread',args=('000581', 10))
# t.start()
# print('000581')
# # t.join()
# t2 = threading.Thread(target=update_tick_for, name='LoopThread',args=('603999', 10))
# print('603999')
# t2.start()
# t2.join()

# thread.start_new_thread(tick_up,('000581', 2))
# t = threading.Thread(target=tick_up, name='LoopThread',args=('000581', 2))
# t.start()
# t.join()
# def loop():
#     print('thread %s is running...')
#     n = 0
#     while n < 5:
#         n = n + 1
#         print 'thread %s >>> %s' % (threading.current_thread().name, n)
#         time.sleep(1)
#     print 'thread %s ended.' % threading.current_thread().name
#
# print 'thread %s is running...' % threading.current_thread().name
# t = threading.Thread(target=loop, name='LoopThread')
# t.start()
# t.join()
# print 'thread %s ended.' % threading.current_thread().name



# ws = create_connection("ws://echo.websocket.org/")
#Short-lived one-off send-receive
#This is if you want to communicate a short message and disconnect immediately when done.
# ws = create_connection("ws://localhost:2017/")
# print "Sending 'Hello, World'..."
# ws.send("Hello, World")
def shortWs():
    ws = create_connection("ws://localhost:2017/")
    print "Sending 'Hello, World'..."
    ws.send("Hello, World")

def on_ws_message(ws, message):
    print message

def on_ws_error(ws, error):
    print error

def on_ws_close(ws):
    print "### closed ###"


def tickSendThead():
    update_tick_today_for()



def ws_main(ws):
    ws.send("main start...")
    thread.start_new_thread(tickSendThead, ())

wsTick={}

def getWs():
    return wsTick['tick']

def initWs(webSocket):
    wsTick['tick']=webSocket

def ws_send(message):
    ws = getWs()
    ws.send(message)


# def on_open(ws):
#     def run(*args):
#         for i in range(3):
#             time.sleep(1)
#             ws.send("Hello %d" % i)
#         time.sleep(1)
#         ws.close()
#         print "thread terminating..."
#     thread.start_new_thread(ws_send, ())

# Long-lived connection
# This example is similar to how WebSocket code looks in browsers using JavaScript.
def tickWsMain():
    if __name__ == "__main__":
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("ws://ytlala.cc:2017/",
                                  on_message = on_ws_message,
                                  on_error = on_ws_error,
                                  on_close = on_ws_close)
        # ws.on_open = on_open
        ws.on_open = ws_main
        initWs(ws)
        # ws_send(123)
        ws.run_forever()#still run not other till close or thread.start_new_thread


tickWsMain()
