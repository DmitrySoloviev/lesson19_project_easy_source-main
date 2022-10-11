from flask_restx import Resource, Namespace

from models import User, UserSchema
from setup_db import db
from flask import request

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        user_schema = UserSchema(many=True)
        users = db.session.query(User).all()
        return user_schema.dump(users), 200

    def post(self):
        req_json = request.json
        new_user = User(**req_json)
        new_user.password = User.create_hash(User, new_user.password)

        db.session.add(new_user)
        db.session.commit()
        return "", 201, {"location": f"/users/{new_user.id}"}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        #user_schema = UserSchema(many=True)
        user = db.session.query(User).get(uid)
        return UserSchema().dump(user), 200

    def put(self, uid):
        req_json = request.json
        user = db.session.query(User).get(uid)
        user.id = req_json.get("id")
        user.username = req_json.get("username")
        user.password = req_json.get("password")
        user.password = User.create_hash(User, user.password)
        user.role = req_json.get("role")
        db.session.add(user)
        db.session.commit()
        return "", 201, {"location": f"/users/{user.id}"}

    def delete(self, uid):
        user = db.session.query(User).get(uid)

        db.session.delete(user)
        db.session.commit()
        return "", 204

