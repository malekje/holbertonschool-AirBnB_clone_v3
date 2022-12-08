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
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200

@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def touch_state():
    """ create a state """
    sta = request.get_json(silent=True)
    if sta is None:
        abort(400, "Not a JSON")
    elif "name" not in sta.keys():
        abort(400, "Missing name")
    else:
        new_sta = state.State(**sta)
        storage.new(new_sta)
        storage.save()
        return jsonify(new_sta.to_dict()), 201

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
