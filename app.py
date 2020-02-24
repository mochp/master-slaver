# coding=utf-8

import os
import time
import json
import yaml
import tornado.web
import tornado.ioloop
import utils
from random import choices
from conf import config

class FileUploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

        modelId = self.get_query_argument('modelId', 'None') 
        picture_path = self.get_query_argument('path', 'None') 
        if_master_slaver = self.get_query_argument('if', '0') 

        assert int(modelId)>0

        port = choices(config.PORTS_SLAVERS)[0]

        if int(if_master_slaver) == 1:
            _ = utils.query_master(modelId,port)
        
        res = utils.predict(port,picture_path)
        respon = {"res":res}

        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(respon))
        self.finish()

class StartSlaverHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        utils.start_all_app()
        respon = {"res":"ok"}

        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(respon))
        self.finish()

class StopSlaverHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        utils.stop_all_app()
        respon = {"res":"ok"}

        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(respon))
        self.finish()

app = tornado.web.Application([
    (r'/app', FileUploadHandler),
    (r'/start', StartSlaverHandler),
    (r'/stop', StopSlaverHandler)
])

if __name__ == '__main__': 
    server = tornado.httpserver.HTTPServer(app)
    server.bind(config.PORTS_INTERFACE)
    server.start(0) 
    tornado.ioloop.IOLoop.instance().start()
