from app import app
from flask import Flask, jsonify, request
import json
from db_helpers import run_query
from flask_cors import CORS
import os
import bcrypt
import uuid
from auth.utils import (
    current_user,
    generate_password
) 



@app.get('/api/restaurant')
def get_restaurants():
    query = 'SELECT *, restaurant.name AS restaurant_name, city.name AS city_name FROM restaurant INNER JOIN city ON restaurant.city = city.id'
    result = run_query(query)

    formated_result = list(map(lambda x: {
        'address': x[3],
        'bannerUrl': x[6],
        'bio': x[5],
        'city': x[11],
        'email': x[1],
        'name': x[2],
        'phoneNum': x[4],
        'profileUrl': x[7],
        'restaurantId': x[9]

    }, result))
    
    return jsonify(formated_result)


@app.post('/api/restaurant')
def create_restaurant():
    request_payload = request.get_json()
    query = 'INSERT INTO restaurant (email, name, address, phone_number, bio, password, city, banner_url, profile_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'

    name = request_payload.get('name')
    address = request_payload.get('address')
    banner_url = request_payload.get('bannerUrl') or 'https://images.pexels.com/photos/2664216/pexels-photo-2664216.jpeg'
    profile_url = request_payload.get('profileUrl') or 'https://images.pexels.com/photos/2664216/pexels-photo-2664216.jpeg'
    bio = request_payload.get('bio')
    city = request_payload.get('city')
    email = request_payload.get('email')
    phone_number = request_payload.get('phoneNum')
    password = generate_password(request_payload.get('password'))

    result = run_query(query, (email, name, address, phone_number, bio, password, city, banner_url, profile_url))

    return jsonify('client created', 200)



@app.patch('/api/restaurant')
def update_restaurant():
    
    data=request.json
    name = data.get('name')
    address = data.get('address')
    phone_number = data.get('phoneNum')
    bio = data.get('bio')
    profile_url = data.get('profile_url')
    banner_url = data.get('banner_url')
    city = data.get('city')

    query = f"""UPDATE restaurant SET name='{name}', address='{address}', phone_number='{phone_number}' , bio='{bio}', profile_url='{profile_url}', banner_url='{banner_url}',city='{city}' WHERE id={current_user()}"""
    result = run_query(query)

    
    return jsonify('restaurant updated', 200)
