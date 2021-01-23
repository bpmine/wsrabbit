from flask import Flask
from flask import request

from rabbit import RabbitMine
import threading
from queue import Queue
import sys
import json


class ServerConsumer (threading.Thread):
    rabbit=None;
    msgs=Queue()
    
    def __init__(self, rabbit):
        self.rabbit=rabbit
        threading.Thread.__init__(self)
        self.setDaemon(True)

    def run(self):
        def cb(topic,msg):
            print("%s: %s" % (topic,msg))
            self.msgs.put({'key':topic,'msg':msg})

        self.rabbit.start(cb)

    def get(self):
        res=[]
        
        while cons.msgs.empty()==False:
            elm=cons.msgs.get()
            res.append(elm)        

        return res 


with open('credentials.txt','r') as json_file:
    data = json.load(json_file)

IP=data['ip']
LOGIN=data['login']
PASS=data['pass']

r=RabbitMine(IP,LOGIN,PASS)
cons=ServerConsumer(r)
cons.start()

rr=RabbitMine(IP,LOGIN,PASS)
rr.publish(".minetest.gw",json.dumps({"src":"minesvce","msg":"Start server"}))

app = Flask(__name__)


ctr=0
@app.route('/test')
def test():
    global ctr
    ctr+=1
    rr.publish('.minetest.gw',json.dumps({'src':'minesvce','msg':'test'}))
    ret= {"result":True,"ctr":ctr}

    print("RETOUR: %s" % ret)

    return ret


@app.route('/poll', methods=['GET'])
def poll():
    lst=[]

    try:
        res=cons.get()
        print(res)
        return {"result":True,"msgs":res}

    except Exception as e:
        print("Erreur %s" % (str(e)))
        return {"result":False,"msg":str(e)}


@app.route('/send', methods=['POST'])
def send():

    try:       
        dta=request.get_json(force=True)
        if dta!=None and dta!=b'':
            try:
                print("Data: %s" % (dta))
                rr.publish('.minetest.gw',json.dumps(dta))
                return {"result":True}
            except Exception as e:
                print("Exception: %s" % ( e) )
                return {"result":False,"msg":str(e)}
    except Exception as e:
        return {"result":False,"msg":str(e)}

    return {"result":False,"msg":"Divers"}






