from flask import jsonify, request
from flask_restful import reqparse, abort, Resource
from . import db_session
from .users import User
from .parsers import user_parser


class UsersResource(Resource):

    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify(
            {
                'user':
                    user.to_dict(
                        only=(
                            'surname', 'name', 'age', 'position', 'speciality', 'address', 'city_from',
                            'email'))
            }
        )

    def post(self, user_id):
        abort_if_user_not_found(user_id)
        args = user_parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        user.surname = request.json['surname']
        user.name = request.json['name']
        user.age = request.json['age']
        user.position = request.json['position']
        user.speciality = request.json['speciality']
        user.address = request.json['address']
        user.email = request.json['email']
        user.city_from = request.json['city_from']
        user.set_password(request.json['password'])
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):

    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify(
            {
                'users':
                    [item.to_dict(
                        only=(
                            'surname', 'name', 'age', 'position', 'speciality', 'address', 'city_from',
                            'email'))
                        for item in users]
            }
        )

    def post(self):
        args = user_parser.parse_args()
        session = db_session.create_session()
        user = User(
            surname=request.json['surname'],
            name=request.json['name'],
            age=request.json['age'],
            position=request.json['position'],
            speciality=request.json['speciality'],
            address=request.json['address'],
            city_from=request.json['city_from'],
            email=request.json['email']
        )
        user.set_password(request.json['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")