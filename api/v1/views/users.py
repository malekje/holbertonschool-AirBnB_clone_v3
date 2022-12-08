#!/usr/bin/python3
"""
users
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users',
                 strict_slashes=False,
                 methods=['GET'])
def view_users():
    """ view all users """
    users = storage.all(User).values()

    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['GET'])
def get_user(user_id):
    """ get user """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def del_user(user_id):
    """ delete user fully """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@app_views.route('/users',
                 strict_slashes=False,
                 methods=['POST'])
def touch_user():
    """ create user """
    try:
        body = request.get_json()

        if body is None:
            abort(400, description="Not a JSON")
        elif body.get('email') is None:
            abort(400, description='Missing email')
        elif body.get('password') is None:
            abort(400, description='Missing password')
        else:
            obj = User(**body)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
    except ValueError:
        abort(400, desciption="Not a JSON")


@app_views.route('/users/<user_id>', methods=["PUT"])
def update_user(user_id):
    """ update user """
    found = storage.get(User, user_id)
    if not found:
        abort(404)

    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
        else:
            invalid = ['id', 'created_at', 'updated_at', 'email']
            for key, value in req.items():
                if key not in invalid:
                    setattr(found, key, value)
            storage.save()
            return jsonify(found.to_dict()), 200
    except ValueError:
        abort(400, description="Not a JSON")
