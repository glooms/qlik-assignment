from flask import Blueprint, request, jsonify
from service.models import interface


user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/', methods=['GET'])
def index():
    return 'Hello World!'


@user_blueprint.route('/user', methods=['GET'])
def users_get():
    data = {
        'users': [user.to_dict() for user in users]
    }
    return (jsonify(data), 200)


@user_blueprint.route('/user', methods=['POST'])
def user_create():
    payload = request.get_json()
    user_name = payload.get('name')
    if not user_name:
        return ('Error: No user name specified.', 400)
    user = interface.create_user(user_name)
    if not user:
        data = {
            'error': 'Duplicate user with name: %s' % user_name
        }
        return (jsonify(data), 400)
    data = {
        'user': user.to_dict()
    }
    return (jsonify(data), 200)


@user_blueprint.route('/user/<user_name>', methods=['GET'])
def user_get(user_name):
    user = interface.get_user(user_name)
    if not user:
        data = {
            'error': 'No user by the name %s' % user_name
        }
        return (jsonify(data), 404)
    data = {
        'user': user.to_dict()
    }
    return (jsonify(data), 200)
