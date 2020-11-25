from flask import Flask,request,render_template,session,redirect
import uuid
import json
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer

from flask_cors import *
 
app = Flask(__name__)
CORS(app, supports_credentials=True)

app.secret_key = 'asdfasdf'

GENTIEMAN = {
   '1':{'name':'钢弹','count':0},
   '2':{'name':'铁锤','count':0},
   '3':{'name':'闫帅','count':0},
}

WEBSOCKET_DICT = {

}


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        uid = str(uuid.uuid4())
        session['user_info'] = {'id':uid,'name':request.form.get('user')}
        print(session)
        return redirect('/index')

@app.route('/index')
def index():
    return render_template('index.html',users=GENTIEMAN)

@app.route('/message')
def message():
   # 1. 判断到底是否是websocket请求？
    ws = request.environ.get('wsgi.websocket')
    if not ws:
        return "请使用WebSocket协议"
   # ----- ws连接成功 -------
    current_user_id=1
    WEBSOCKET_DICT[current_user_id] = ws
    print(current_user_id)
    while True:
       # 2. 等待用户发送消息，并接受
        message = ws.receive() # 帅哥ID
       # 关闭：message=None
        if not message:
            del WEBSOCKET_DICT[current_user_id]
            break

       # 3. 获取用户要投票的帅哥ID,并+1
        if message=='play':
            data = {'user_id': message,'type':'play'}
            for conn in WEBSOCKET_DICT.values():
                conn.send(json.dumps(data))# 4. 给所有客户端推送消息
        elif message=='pause':
            data = {'user_id': message,'type':'pause'}
            for conn in WEBSOCKET_DICT.values():
                conn.send(json.dumps(data))# 4. 给所有客户端推送消息
    return 'close'

@app.route('/notify')
def notify():
   data = {'data': "你的订单已经生成，请及时处理；", 'type': 'alert'}
   print(WEBSOCKET_DICT)
   for conn in WEBSOCKET_DICT.values():
       conn.send(json.dumps(data))
   return '发送成功'

if __name__ == '__main__':
   http_server = WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
   http_server.serve_forever()
