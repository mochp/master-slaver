# coding=utf-8

import os
import sys
import json
import tornado.web
import tornado.ioloop
import utils



class FileUploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        path = self.get_query_argument('path', 'None')
        _, res = model.detect_image(path)
        respon = str(res)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(respon)
        self.finish()


if __name__ == '__main__':
    
    pid = os.getpid()
    port, model_path, labels,device = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    #预先锁定
    os.environ["CUDA_VISIBLE_DEVICES"] = str(device)
    from yolo3.yolo import YOLO
    
    model = YOLO(model_path=model_path, labels=labels)
    utils.set_port(port=port, pids=pid, modelPath=model_path, status=-1)
    app = tornado.web.Application([(r'/yolo', FileUploadHandler), ])
    app.listen(port)
    tornado.ioloop.IOLoop.instance().start()
