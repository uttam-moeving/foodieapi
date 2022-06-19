from flask import Flask, request, jsonify
import db_helpers 
import sys 

app = Flask(__name__)

@app.post('/api/animals')]