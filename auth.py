#  Created by btrif Trif on 04-07-2022 , 10:41 PM.
from models import app, Users
from functools import wraps
import jwt
from flask import request, json, jsonify

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid! Please authenticate with a valid user in order to proceed.'})

        return f(current_user, *args, **kwargs)
    return decorator

