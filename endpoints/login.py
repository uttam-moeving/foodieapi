from datetime import datetime, timedelta
from app import app
from flask import Flask, jsonify, request
import json
from auth.utils import create_access_token
from db_helpers import run_query
from flask_cors import CORS
import os
import bcrypt
import uuid
from endpoints import client
from auth.utils import (
    current_user
)



@app.post('/api/login')
def client_login():
    request_payload = request.get_json()
    query = 'SELECT * FROM client WHERE email=?'

    email = request_payload.get('email')
    password = request_payload.get('password')

    
    result =run_query(query, [email])


    
    if bcrypt.checkpw(password.encode(), result[0][3].encode()):
        # check for existing token
        tokencheck = f'SELECT * FROM client_session WHERE client_Id={result[0][0]}'
        oldtoken = run_query(tokencheck)
        newtoken=create_access_token()
        if(len(oldtoken)>0): # if old token exist
            updatequery = f"UPDATE client_session SET token = '{newtoken}' WHERE client_Id = {result[0][0]}"
            run_query(updatequery)
        else:
            run_query(f"INSERT INTO client_session (token, client_Id) VALUES ('{newtoken}',{result[0][0]})")

        return jsonify({'clientId':result[0][0],'token':newtoken}), 200
    else:
        return jsonify(result, 401)



@app.post('/api/restaurant_login')
def restaurant_login():
    request_payload = request.get_json()
    query = 'SELECT * FROM restaurant WHERE email=?'

    email = request_payload.get('email')
    password = request_payload.get('password')

    
    result =run_query(query, [email])

    
    if bcrypt.checkpw(password.encode(), result[0][3].encode()):

        token=str(uuid.uuid4())
        run_query( 'INSERT INTO restaurant_session (token, restuarant_Id) VALUES (?,?)', [token, result[0][0]])
        restuarant_Id= result[0][0]
        
        return jsonify({restuarant_Id:result[0][0],token:token}), 200
    else:
        return jsonify(result, 401)
