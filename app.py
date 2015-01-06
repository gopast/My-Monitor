from flask import Flask, render_template,request
from flask.ext.socketio import SocketIO, emit
import tailer
from monitor import Monitor

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
follow_resp_chan = 'follow-response'
tail_resp_chan='tail-response'
_monitor=Monitor('E:\\test.txt')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/monitor')
def monitor():
    return render_template('monitor.html')
    

@socketio.on('connect', namespace='/monitor')
def on_connect():
    emit('connect-response', {'data': 'Connected'})
    
@socketio.on('disconnect', namespace='/monitor')
def on_disconnect():
    print('Client disconnected')
    
@socketio.on('follow-request', namespace='/monitor')
def follow_monitor(msg):
    try:
        last_pos=0
        if msg['data']=='0':
            last_pos=_monitor.get_max_position()
            emit(follow_resp_chan,{'pos':last_pos,'data':''})
        else:
            last_pos=int(msg["data"])
            for line,cur_pos in _monitor.follow(last_pos):
                emit(follow_resp_chan, {'data': line,'pos':cur_pos})
    except Exception as ex:
        last_pos=_monitor.get_max_position()
        err='<Mornitor Error> '.format(ex.message)
        emit(follow_resp_chan, {'data': err,'pos':last_pos})
            
@socketio.on('tail-request', namespace='/monitor')
def tail_monitor(msg):
    try:
        if msg.get('lines'):
            num=int(msg['lines'])
        else:
            num=100
        key=msg.get("key","")
        ret =_monitor.tail(num,key)
        ret=reversed([x for x in ret])
        for line in ret:
            emit(tail_resp_chan, {'data': line})
    except Exception as ex:
        err='<Mornitor Error> '.format(ex.message)
        emit(tail_resp_chan, {'data': err})    
            
if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=5000)