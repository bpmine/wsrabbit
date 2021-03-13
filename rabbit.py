#!/usr/bin/python3
import pika


class RabbitMine:
    ip=None
    login=None
    passe=None

    conn=None
    ch=None

    def connect(self):
        credentials = pika.PlainCredentials(self.login, self.passe)

        self.conn = pika.BlockingConnection(
            pika.ConnectionParameters(self.ip,
                                      5672,
                                      '/',
                                      credentials)
            )
        self.ch = self.conn.channel()
        
    
    def __init__(self,ip,login,passe):
        self.ip=ip
        self.login=login
        self.passe=passe

        self.connect()

    def publish(self,topic,msg):
        print("send %s: %s" % (topic,msg) )
        try:
            if self.ch.is_closed==True:
                self.connect()

            self.ch.basic_publish(exchange='minetest',
                              routing_key=topic,
                              body=msg)
        except Exception as e:
            print("Except: %s" % (e))


    def close(self):
        self.ch.close()
        self.conn.close()

    def intern_cb(self,ch, method, properties, body):
        key=method.routing_key
        msg=body.decode()
        if (self.callback!=None):
            self.callback(key,msg);

        self.ch.basic_ack(delivery_tag=method.delivery_tag)
        
    def start(self,callback):
        self.callback=callback;
        self.ch.basic_consume(queue='minetest_server', on_message_callback=self.intern_cb)

        self.ch.start_consuming()




