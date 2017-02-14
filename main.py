import threading

import tushare as ts
import time
import thread

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

        t = threading.Thread(target=update_tick_for, name='LoopThread',args=(tick, 2))
        t.start()

        # t.join()
# update_tick_for('000581',2)
# print(ts.get_today_all())
update_tick_today_for()

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