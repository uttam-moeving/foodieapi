from flask import Flask, jsonify, request
import json
from db_helpers import run_query
from flask_cors import CORS

# configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
# set environment
app.testing = True

# enable CORS
CORS(app, resources={ r'/*': { 'origins': '*' } })


@app.route('/api/restaurant', methods=['GET'])
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
    return jsonify(formated_result);


@app.route('/api/restaurant', methods=['POST'])
def create_restaurant():
    request_payload = request.get_json()
    query = 'INSERT INTO restaurant (email, name, address, phone_number, bio, password, city, banner_url, profile_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

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

    return

@app.route('/api/restaurant', methods=['DELETE'])
def delete_restaurant():
    pass


@app.route('/api/client', methods=['GET'])
def get_clients():
    query = 'SELECT * FROM client'
    result = run_query(query)

    formated_result = list(map(lambda x: {
        'clientId': x['id'],
        'createdAt': x['created_at'],
        'email': x['email'],
        'firstName': x['first_name'],
        'lastName': x['last_name'],
        'pictureUrl': x['picture_url'],
        'username': x['username']
    }, result))

    return jsonify(formated_result)


app.run()
