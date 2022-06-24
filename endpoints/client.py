from app import app
from flask import Flask, jsonify, request
import json
import datetime
from db_helpers import run_query
from flask_cors import CORS
import os
import bcrypt
import uuid

from endpoints.login import client_login




@app.get('/api/client')
def get_clients():
    query = 'SELECT * FROM client'
    result = run_query(query)

    return jsonify(result)

@app.post('/api/client')
def create_client():
    request_payload = request.get_json()
    query = 'INSERT INTO client (email, username, password, first_name, last_name, picture_url) VALUES (?,?,?,?,?,?)'

    email = request_payload.get('email')
    username = request_payload.get('username')
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(request_payload.get('password').encode(), salt)
    first_name = request_payload.get('first_name')
    last_name = request_payload.get('last_name')
    picture_url = request_payload.get('picture_Url') or 'https://images.pexels.com/photos/2664216/pexels-photo-2664216.jpeg'
    
    result = run_query(query, (email, username, password, first_name, last_name, picture_url))

    return jsonify('client created', 200)

app.patch('/api/client')
def update_client():
    data=request.json
    token = data.get('token')
    
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    picture_url = data.get('picture_Url') 
    
    query = 'UPDATE client WHERE Id = ?'
    result = run_query(query, (client_id))
    
    
    return jsonify('client updated', 200) 