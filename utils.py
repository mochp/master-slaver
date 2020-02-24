#!/usr/bin/python

import os
import json
import time
import requests
from conf import config


def create_json(ports):
    total = {}
    for i, port in enumerate(ports):
        unit = {}
        unit.update(pid=-2)
        unit.update(status=-2)
        unit.update(modelPath=config.INIT_MODELPATH)
        total[str(port)] = unit
    with open("conf/config.json", "w") as f:
        json.dump(total, f, sort_keys=True, indent=4)
    return total

def modelId2path(ids):
    return config.INIT_MODELPATH.replace("600",str(ids))


def start_app():
    data = read_json()
    print(data)
    for key in data:
        print(key, data[key]["modelPath"])
        cmd = ("nohup python slaver.py" + " "
               + key + " "
               + str(data[key]["modelPath"]) + " "
               + config.INIT_LABELS + " &")
        print("start...", cmd)
        os.system(cmd)
        time.sleep(0.5)


def stop_port(port):
    data = read_json()
    pids = data[str(port)]["pid"]
    if pids>0:
        res = os.system("kill -9 " + str(pids))
        time.sleep(0.1)
        if res == 0:
            set_port(port=port, pids=-1, status=-2)


def stop_all():
    data = read_json()
    for key in data:
        pids = data[key]["pid"]
        if pids > 0:
            res = os.system("kill -9 " + str(pids))
            if res == 0:
                set_port(port=key, pids=-1, status=-2)


def read_json():
    with open("conf/config.json", "r") as f:
        res = json.load(f)
    return res


def set_port(port, pids=None, status=None, modelPath=None):
    port = str(port)
    data = read_json()
    if pids is not None:
        data[port]["pid"] = pids
    if status is not None:
        data[port]["status"] = status
    if modelPath is not None:
        data[port]["modelPath"] = modelPath
    with open("conf/config.json", "w") as f:
        json.dump(data, f, sort_keys=True, indent=4)
    return data

def modelId_to_labels(modelID):
    if int(modelID) == 600:
        return "1,2,3,4,5,6,7,8,9,10,11,12,13,14"
    if int(modelID) == 400:
        return "1,2,3,4,5"

def waiting_port_ready(port):
    while True:
        data = read_json()
        if data[str(port)]["status"]==-1:
            break
        time.sleep(1)
        print("waiting_port_ready...",port)

def waiting_port_success(port):
    while True:
        data = read_json()
        if data[str(port)]["status"]==1:
            break
        time.sleep(1)
        print(f"waiting_{port}_success...",port)

def waiting_port_success_or_ready(port):
    while True:
        data = read_json()
        if data[str(port)]["status"]==1:
            break
        if data[str(port)]["status"]==-1:
            break
        time.sleep(1)
        print("waiting_port_success...",port)

def setting_port_working(port):
    set_port(port,status=0)

def setting_port_success(port):
    set_port(port,status=1)

def check_port_is_modelId(port,modelID):
    data = read_json()
    new_model_path = config.INIT_MODELPATH.replace("600",str(modelID))
    if data[str(port)]["modelPath"] == new_model_path:
        return True
    else:
        return False

def shift_port_to_modelId(port,modelId):
    data = read_json()
    if str(data[str(port)]["modelPath"]) != modelId2path(modelId):
        set_port(port=port,status=-1)
        stop_port(port)
        new_model_path = config.INIT_MODELPATH.replace("600",str(modelId))
        new_model_labels = modelId_to_labels(modelId)
        cmd = ("nohup python slaver.py" + " " 
                + str(port) + " " 
                + new_model_path +" " 
                + new_model_labels + " &")
        print("cmding:",cmd)
        os.system(cmd)

def predict(port,path):
    url = "http://localhost:"+str(port) +"/yolo?path="+path
    res = requests.get(url)
    return res.text
    
def query_master(modelId,port):
    payload = {'modelId': modelId, 'port': port}
    ret = requests.get("http://localhost:8888/master", params=payload)
    print(ret.text)

if __name__ == '__main__':
    print("testing...")
    # stop_all()
    create_json(config.PORTS)
    start_app()
    # query_master(400,6610)
    
