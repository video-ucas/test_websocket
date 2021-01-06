from flask import Flask,request,render_template,session,redirect
import uuid
import json
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer

from flask_cors import *
 
app = Flask(__name__)
CORS(app, supports_credentials=True)

app.secret_key = 'asdfasdf'



if __name__ == '__main__':
   http_server = WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
   http_server.serve_forever()
