from flask import Flask, jsonify, request
import json
from db_helpers import run_query
from flask_cors import CORS
import os
import bcrypt
import uuid
from endpoints import client, login, order, restaurant, menu 
# configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
# set environment
app.testing = True

# enable CORS
CORS(app, resources={ r'/*': { 'origins': '*' } })



app.run()