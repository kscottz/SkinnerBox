#!/usr/bin/env python
import sys, os, signal, time
from bottle import route, run, static_file, template, view, post, get
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
import datetime as dt
import gevent
from modules.HardwareInterface import *
from modules.CameraInterface import *
from modules.DataInterface import *
from modules.ProtocolRunner import *
import picamera
import json


def send_msg(name,value,color=None):
    now = dt.datetime.now()
    msg = {}
    msg['time'] = "{0} {1}".format(now.date(),now.time())
    msg['data'] = '{0}'.format(name)
    msg['value'] = '{0}'.format(value)
    msg['color'] = '{0}'.format(color)
    for u in users:
        u.send(json.dumps(msg))

def notify_buzz():
    send_msg("Buzzer Sound",None)

def notify_feed():
    send_msg("Food Dispensed",None,"success")

def notify_click():
    send_msg("Button Press",None,"warning")

def notify_motion(change):
    send_msg("Activity",change,None)
    
myData = DataInterface()
myhw = HardwareInterface()
myci = CameraInterface('./img/live.png')
mypr = ProtocolRunner(myhw,myData)

myhw.on_button_up(notify_click)
myhw.on_button_up(myData.log_press)

myhw.on_buzz(myData.log_buzz)
myhw.on_buzz(notify_buzz)

myhw.on_feed(myData.log_food)
myhw.on_feed(notify_feed)

myci.set_motion_callback(notify_motion)
myci.set_motion_callback(myData.log_activity)
myhw.on_button_up(mypr.button_callback)
myci.start()
myhw.start()
mypr.start()

@route('/js/<filename>')
def js_static(filename):
    return static_file(filename, root='./js')

@route('/img/<filename>')
def img_static(filename):
    return static_file(filename, root='./img')

@route('/css/<filename>')
def img_static(filename):
    return static_file(filename, root='./css')


@post("/merp")
def merp():
    myhw.power_down()
    myhw.join()
    myci.shutdown()
    myhw.join()

@post("/buzz")
def buzz():
    myhw.buzz_once()
    for u in users:
        u.send("buzz")

@post("/feed")
def dispense():
    myhw.dispense()
    for u in users:
        u.send("feed")


@route("/pics")
@view("live")
def live():
    return dict(title = "Hello", button="derp2", content = '''
    Hello from Python!

    ''')

@route("/activity")
@view("activity")
def activity():
    myData.generateActivity('./img/activity.png')
    return dict(title = "Activity Monitor", button="derp2", content = '''
    Check out what the wee beasties are doing!

    ''')

@route("/presses")
@view("plot")
def live():
    myData.generateActivity('./img/activity.png')
    return dict(title = "Food Request Monitor",
                image = '/img/activity.png',
                route = '/presses',
                content = '''

    '''
                )



@route("/")
@view("main")
def hello():
    return dict(title = "Hello", button="derp2", content = '''
    Hello from Python!

    ''')

users = set()
@get('/websocket', apply=[websocket])
def chat(ws):
    users.add(ws)
    while True:
        msg = ws.receive()
        print msg
        if msg is not None:
            for u in users:
                u.send(msg)
        else: 
            break
    users.remove(ws)    

def signal_handler(signal, frame):
    mypr.shutdown()
    time.sleep(2)
    mypr.join()
    myci.shutdown()
    time.sleep(2)
    myci.join()
    myhw.shutdown()
    time.sleep(2)
    myhw.join()
    sys.exit(0)

if __name__ == "__main__":
    # on ctrl-c try to exit clean
    signal.signal(signal.SIGINT, signal_handler)
    port = int(os.environ.get("PORT", 5000))
    run(host='0.0.0.0', port=port, server=GeventWebSocketServer)
     

