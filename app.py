from flask import Flask, jsonify, request
import json
from db_helpers import run_query
from flask_cors import CORS
import os
import bcrypt
import uuid

# configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
# set environment
app.testing = True

# enable CORS
CORS(app, resources={ r'/*': { 'origins': '*' } })



@app.route('/api/client', methods=['GET'])
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

@app.delete('/api/client/<id>')
def delete_client():
    client_id = request.view_args['id']
    query = 'DELETE FROM client WHERE Id = ?'
    result = run_query(query, (client_id))
    
    return jsonify('client deleted', 200)

@app.route('/api/client/<id>', methods=['GET', 'POST'])
def update_client():
    client_id = request.view_args['id']
    query = 'UPDATE client WHERE Id = ?'
    result = run_query(query, (client_id))
    
    return jsonify('client updated', 200)


@app.get('/api/restaurant')
def get_restaurants():
    query = 'SELECT *, restaurant.name AS restaurant_name, city.name AS city_name FROM restaurant INNER JOIN city ON restaurant.city = city.id'
    result = run_query(query)

    formated_result = list(map(lambda x: {
        'address': x['address'],
        'bannerUrl': x['banner_url'],
        'bio': x['bio'],
        'city': x['city_name'],
        'email': x['email'],
        'name': x['restaurant_name'],
        'phoneNum': x['phone_number'],
        'profileUrl': x['profile_url'],
        'restaurantId': x['id']

    }, result))
    return jsonify(formated_result)


@app.post('/api/restaurant')
def create_restaurant():
    request_payload = request.get_json()
    query = 'INSERT INTO restaurant (email, name, address, phone_number, bio, password, city, banner_url, profile_url) VALUES (?, ?, ?,?, ?, ?, ?, ?)'

    name = request_payload.get('name')
    address = request_payload.get('address')
    banner_url = request_payload.get('bannerUrl') or 'https://images.pexels.com/photos/2664216/pexels-photo-2664216.jpeg'
    profile_url = request_payload.get('profileUrl') or 'https://images.pexels.com/photos/2664216/pexels-photo-2664216.jpeg'
    bio = request_payload.get('bio')
    city = request_payload.get('city')
    email = request_payload.get('email')
    phone_number = request_payload.get('phoneNum')
    password = request_payload.get('password')


    result = run_query(query, (email, name, address, phone_number, bio, password, city, banner_url, profile_url))

    return jsonify('client created', 200)

@app.delete('/api/restaurant/<id>')
def delete_restaurant():
    restaurant_id = request.view_args['id']
    query = 'DELETE FROM restaurant WHERE Id = ?'
    result = run_query(query, (restaurant_id))
    
    return jsonify('restaurant deleted', 200)


@app.route('/api/restaurant/<id>', methods=['GET', 'POST'])
def update_restaurant():
    restaurant_id = request.view_args['id']
    query = 'UPDATE restaurant WHERE Id = ?'
    result = run_query(query, (restaurant_id))
    
    return jsonify('restaurant updated', 200)


@app.post('/api/login')
def client_login():
    request_payload = request.get_json()
    query = 'SELECT * FROM client WHERE username=?'

    username = request_payload.get('username')
    password = request_payload.get('password')

    
    result =run_query(query, [username])

    
    if bcrypt.checkpw(password.encode(), result[0][3].encode()):
    
        token=uuid.uuid4()
        run_query( 'INSERT INTO client_session (token, client_Id) VALUES (?,?)', [token, result[0][0]])
        
        
        return jsonify({client_Id:result[0][0],token:token}), 200
    else:
        return jsonify(result, 401)

app.run()