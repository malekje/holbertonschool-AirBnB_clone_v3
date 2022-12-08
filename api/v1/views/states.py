#!/usr/bin/python3
"""
states view for api
"""


from flask import request, jsonify , abort
from models import storage
from models.state import State
from api.v1.views import app_views

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_of_states():
    """ Retrieves the list of all State objects """
    result = []
    for i in storage.all("State").values():
        result.append(i.to_dict())

    return jsonify(result)

@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def view_state(state_id):
    """ get state """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id=None):
    """ delete a state """
    str = storage.get("State", state_id)
    if str is None:
        abort(404)
    else:
        storage.delete(str)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def touch_state():
    """ create a state """
    try:
        body = request.get_json()

        if body is None:
            abort(400, description="Not a JSON")
        elif body.get('name') is None:
            abort(400, description='Missing name')
        else:
            obj = State(**body)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
    except ValueError:
        abort(400, desciption="Not a JSON")


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """ update state """
    object = storage.get("State", state_id)
    if object is None:
        abort(404)

    storg = request.get_json(silent=True)
    if storg is None:
        abort(400, "Not a JSON")
    else:
        for key, value in storg.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(object, key, value)
        storage.save()
        res = object.to_dict()
        return jsonify(res), 200
