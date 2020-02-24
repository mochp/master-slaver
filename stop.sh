echo "Stoping ... "

echo "stop slaver..."
python utils.py stop

echo "stop master..."
ps -ef | grep 'python master.py' | grep -v 'grep'| awk '{print $2}' | xargs kill -9

echo "stop app..."
ps -ef | grep 'python app.py' | grep -v 'grep'| awk '{print $2}' | xargs kill -9