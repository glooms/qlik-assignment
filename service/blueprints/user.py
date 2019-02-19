from flask import Blueprint, request, jsonify, url_for, current_app
from service.models import interface


user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/', methods=['GET'])
def index():
    urls = {
        'GET': [],
        'DELETE': [],
        'POST': []
    }
    filter_methods = {'GET', 'DELETE', 'POST'}
    for rule in current_app.url_map.iter_rules():
        if not 'static' in rule.rule:
            methods = filter_methods.intersection(rule.methods)
            for m in methods:
                urls[m] += [rule.rule]
    data = {
        'message': 'Hello! These are the available routes.',
        'routes': urls
    }
    return jsonify(data, 200)


@user_blueprint.route('/user', methods=['GET'])
def users_get():
    users = interface.get_all_users()
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
    user = interface.get_user(user_name)
    if user:
        data = {
            'error': 'Duplicate user with name: %s' % user_name
        }
        return (jsonify(data), 400)
    user = interface.create_user(user_name)
    if not user:
        data = {
            'error': 'User %s not created.' % user_name
        }
        return (jsonify(data), 500)
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
