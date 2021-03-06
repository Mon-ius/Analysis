
import os
import json
import time
import socket
import subprocess
import grequests

from Server_standalone import app
from datetime import datetime
from gevent.pywsgi import WSGIServer


def rs_get(urls=None):
    origin = 'http://127.0.0.1:4040/api/tunnels'
    if not urls:
        urls = [origin]
    rs = (grequests.get(u, timeout=3) for u in urls)
    
    return grequests.map(rs)


def rs_post(data,urls=None):
    headers = {'Content-Type': 'application/json'}
    remote = 'https://nvh.monius.top/api/ngrok'
    if not urls:
        urls = [remote]
    rs = (grequests.post(u, data=json.dumps(data), headers=headers, timeout=5) for u in urls)
    print(data)
    return grequests.map(rs)

def Ngrok_start():
    time = str(datetime.now())[:19]
    # list of strings representing the command
    args = ['/home/pi/ngrok', 'http', '5001']
    # logging.basicConfig(filename='run.log', level=logging.INFO)
    print(time+' Ngrok Start')
    try:
        # stdout = subprocess.PIPE lets you redirect the output
        res = subprocess.Popen(args, stdout=subprocess.PIPE)
    except OSError:
        print('error')
        exit(-1) # if the subprocess call failed, there's not much point in continuing

    # res.wait() # wait for process to finish; this also sets the returncode variable inside 'res'
    if res.returncode != 0:
        print("exit processer\n")
    else:
        print("wait processer:({},{})".format(res.pid, res.returncode))
    print('finished')
def get_loc():
    return (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or 
            [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

print("--------------------------------------------------------------------------------Start-----------------------------------------------------------------------------------------------------------------------------------------------------")

print("--------------------------------------------------------------------------------At {}          ".format(str(datetime.now())[:19]))

Ngrok_start()
origin_requset = rs_get()[0]
while(not origin_requset or origin_requset.status_code == 502):
    origin_requset = rs_get()[0]
    
else:
    time.sleep(5)
    origin_requset = rs_get()[0]
    print(origin_requset)
    if(not origin_requset.json()):
        print(2333)
    else:
        print(origin_requset.json())
        print(origin_requset.json().keys())
    loc = get_loc()
    pub = str(origin_requset.json()['tunnels'][0]['public_url'])
    print("----------Ngrok Location:---------")
    print("   loc:{}     pub:{}  ".format(loc,pub))
    print("-----------------------------")
    data = {"pub": pub, "loc": loc, "time": str(datetime.now())[:19]}

    remote_requset = rs_post(data)[0]

    if(remote_requset.status_code == 200):
        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()
        print("--------------------------------------------------------------------------------Close-----------------------------------------------------------------------------------------------------------------------------------------------------")
    else:
        print('error')

print(origin_requset.raise_for_status())


# ['', '/usr/lib/python2.7', '/usr/lib/python2.7/plat-arm-linux-gnueabihf', '/usr/lib/python2.7/lib-tk', '/usr/lib/python2.7/lib-old',
#     '/usr/lib/python2.7/lib-dynload', '/usr/local/lib/python2.7/dist-packages', '/usr/lib/python2.7/dist-packages', '/usr/lib/pymodules/python2.7']

# ['', '/usr/lib/python2.7', '/usr/lib/python2.7/plat-arm-linux-gnueabihf', '/usr/lib/python2.7/lib-tk', '/usr/lib/python2.7/lib-old', '/usr/lib/python2.7/lib-dynload',
#     '/home/pi/.local/lib/python2.7/site-packages', '/usr/local/lib/python2.7/dist-packages', '/usr/lib/python2.7/dist-packages', '/usr/lib/pymodules/python2.7']
# /usr/lib/arm-linux-gnueabihf/libproxychains.so.3

