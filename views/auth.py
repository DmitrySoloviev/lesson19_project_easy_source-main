from flask_restx import Resource, Namespace
from flask import request, abort
from setup_db import db
from models import User
import hashlib
import datetime
import calendar
import jwt
from constants import secret, algo
import config

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        uid = req_json.get("id")
        username = req_json.get("username")
        password = req_json.get("password")
        role = req_json.get("role")
        if None in [uid, username, password, role]:
            abort(400)
        user = db.session.query(User).filter(User.id == uid).first()
        if user is None:
            return {"error": "Неверные учетные данные"}, 401
        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
        if user.get_hash() != password_hash:
            return {"error": "Неверные учётные данные"}, 401

        data = {
            "id": uid,
            "username": user.username,
            "role": user.role
        }
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)
        day130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(day130.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens, 201

    def put(self):
        req_json = request.json
        refresh_token = req_json.get("refresh_token")
        if refresh_token is None:
            abort(400)
        try:
            data = jwt.decode(jwt=refresh_token, key=secret, algorithm=[algo])
        except Exception as e:
            abort(400)

        uid = data.get("id")

        user = db.session.query(User).filter(User.id == uid).first()

        data = {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)

        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens, 201