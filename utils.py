#!/usr/bin/python

import os
import sys
import json
import time
import requests
from conf import config


def create_json(ports, devices):
    total = {}
    for i, port in enumerate(ports):
        unit = {}
        unit.update(pid=-2)
        unit.update(status=-2)
        unit.update(device=devices[i])
        unit.update(modelPath=config.INIT_MODEL_LIAN_PATH)
        total[str(port)] = unit
    with open("conf/config.json", "w") as f:
        json.dump(total, f, sort_keys=True, indent=2)
    return total


def read_json():
    with open("conf/config.json", "r") as f:
        res = json.load(f)
    return res


def start_all_app():
    create_json(config.PORTS_SLAVERS, config.DEVICE_SLAVERS)
    data = read_json()
    for key in data:
        print(key, str(data[key]["device"]))
        cmd = ("nohup python slaver.py" + " " + key + " " + str(data[key]["modelPath"]) + " "
               + config.LABELS_LIAN + " " + str(data[key]["device"])+" &")
        print("start...", cmd)
        os.system(cmd)
        time.sleep(0.1)


def stop_all_app():
    data = read_json()
    for key in data:
        pids = data[key]["pid"]
        if pids > 0:
            res = os.system("kill -9 " + str(pids))
            if res == 0:
                set_port(port=key, pids=-1, status=-2)


def stop_port(port):
    data = read_json()
    pids = data[str(port)]["pid"]
    if pids > 0:
        res = os.system("kill -9 " + str(pids))
        time.sleep(0.1)
        if res == 0:
            set_port(port=port, pids=-1, status=-2)


def check_port_is_modelId(port, modelId):
    data = read_json()
    new_model_path = modelId2path(str(modelId))
    if data[str(port)]["modelPath"] == new_model_path:
        return True
    else:
        return False


def shift_port_to_modelId(port, modelId):
    data = read_json()
    if str(data[str(port)]["modelPath"]) != modelId2path(modelId):
        stop_port(port)
        new_model_path = modelId2path(str(modelId))
        new_model_labels = modelId_to_labels(modelId)
        cmd = ("nohup python slaver.py" + " "
               + str(port) + " "
               + new_model_path + " "
               + new_model_labels + " "
               + str(data[str(port)]["device"])+" &")
        print("cmding:", cmd)
        os.system(cmd)


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


def waiting_port_ready(port):
    while True:
        data = read_json()
        if data[str(port)]["status"] == -1:
            break
        time.sleep(1)
        print("waiting_port_ready...", port)


def waiting_port_success(port):
    while True:
        data = read_json()
        if data[str(port)]["status"] == 1:
            break
        time.sleep(1)
        print(f"waiting_{port}_success...", port)


def waiting_port_success_or_ready(port):
    while True:
        data = read_json()
        if data[str(port)]["status"] == 1:
            break
        if data[str(port)]["status"] == -1:
            break
        time.sleep(1)
        print("waiting_port_success...", port)


def modelId2path(ids):
    return config.INIT_MODEL_LIAN_PATH.replace("600", str(ids))


def path2modelId(path):
    ids = os.path.splitext(os.path.split(path)[-1])[0]
    return ids


def setting_port_working(port):
    set_port(port, status=0)


def setting_port_success(port):
    set_port(port, status=1)


def modelId_to_labels(modelID):
    if int(modelID) == 600:
        return config.LABELS_LIAN
    if int(modelID) == 400:
        return config.LABELS_SIFANG


def predict(port, path):
    url = "http://localhost:"+str(port) + "/yolo?path="+path
    res = requests.get(url)
    return res.text


def query_master(modelId, port):
    payload = {'modelId': modelId, 'port': port, "if": "0"}
    ret = requests.get("http://localhost:" +
                       str(config.PORTS_MASTER)+"/master", params=payload)
    print(ret.text)


def command(status):
    if status == "start":
        start_all_app()
        print("start ok ~~~")
    elif status == "stop":
        stop_all_app()
        print("stop ok ~~~")
    else:
        print("wrong command")


if __name__ == '__main__':
    command(sys.argv[1])
