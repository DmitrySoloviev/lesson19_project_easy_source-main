from flask_restx import Resource, Namespace

from models import Genre, GenreSchema
from setup_db import db
from flask import request
from wraps import auth_required, admin_required

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = db.session.query(Genre).all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)

        db.session.add(new_genre)
        db.session.commit()
        return "", 201, {"location": f"/genres/{new_genre.id}"}



@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    @auth_required
    def get(self, rid):
        r = db.session.query(Genre).get(rid)
        #genre_schema = GenreSchema(many=True)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, rid):
        req_json = request.json
        r = db.session.query(Genre).get(rid)
        r.id = req_json.get("id")
        r.name = req_json.get("name")

        db.session.add(r)
        db.session.commit()
        return "", 201, {"location": f"/genres/{r.id}"}

    @admin_required
    def delete(self, rid):
        r = db.session.query(Genre).get(rid)

        db.session.delete(r)
        db.session.commit()
        return "", 204
