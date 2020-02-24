#!/bin/bash

echo "Starting ... "

echo "start slaver..."
python utils.py start

echo "start master..."
nohup python master.py &

echo "start interface ..."
nohup python app.py &