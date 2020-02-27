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

class FileSizeHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        modelSize = self.get_query_argument("modelSize", "none")
        modelPath = self.get_query_argument("modelPath", "none")
        rate = int(os.path.getsize(modelPath))/int(modelSize)
        rate = '%.2f' % rate
        result = {
            "status": 1,
            "result": rate
        }
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(result))
        self.finish()



class FileUploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

        modelId = self.get_query_argument('modelId', 'None') 
        picture_path = self.get_query_argument('path', 'None') 
        if_master_slaver = self.get_query_argument('if', '1') 

        assert int(modelId)>0

        port = choices(config.PORTS_SLAVERS)[0]

        if int(if_master_slaver) == 1:
            _ = utils.query_master(modelId,port)
        
        respon = utils.predict(port,picture_path)

        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(respon)
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
    (r'/stop', StopSlaverHandler),
    (r'/rate', FileSizeHandler)
])

if __name__ == '__main__': 
    server = tornado.httpserver.HTTPServer(app)
    server.bind(config.PORTS_INTERFACE)
    server.start(0) 
    tornado.ioloop.IOLoop.instance().start()
