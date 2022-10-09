import jwt
from flask import request, abort
from constants import secret, algo


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        try:
            jwt.decode(token, key=secret, algorithms=[algo])
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['AUTHORIZATION']
        token = data.split("Bearer ")[-1]
        try:
            user = jwt.decode(token, key=secret, algorithms=[algo])
            role = user.get("role")
            if role != "admin":
                abort(400)
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper

