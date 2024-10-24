from flask import Blueprint, request, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt
import json

orders = Blueprint('orders', __name__)

@orders.get('/')
def get_hello():
    return {"message": "Hello World"}, 200


@orders.post('/')
def echo_post():
    body = request.get_json()
    return {"echo": body}, 200