from flask import Flask, jsonify, request, make_response
import json
from db_helpers import run_query
from flask_cors import CORS
import os
import bcrypt
import uuid
from flask_http_middleware import MiddlewareManager, BaseHTTPMiddleware
from flask import abort
from auth.utils import validate_token

class SecureRoutersMiddleware(BaseHTTPMiddleware):
    def __init__(self, secured_routers = []):
        super().__init__()
        self.secured_routers = secured_routers

    def dispatch(self, request, call_next):
        if request.path in self.secured_routers:
            if(validate_token(request.headers.get('token'))):
                return call_next(request)
            else:
                abort(401)
                return jsonify({"message": "invalid token"})

        else:
            return call_next(request)

secured_routers = ["/api/client"]

# configuration

app = Flask(__name__)
app.testing = True


app.wsgi_app = MiddlewareManager(app)
app.wsgi_app.add_middleware(SecureRoutersMiddleware, secured_routers=secured_routers)

# enable CORS
CORS(app, resources={ r'/*': { 'origins': '*' } })

from endpoints import client, login, menu_item, order, restaurant 

