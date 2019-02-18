from flask import Blueprint, request
from service.models import interface


user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/user', methods=['GET'])
def users_get():
    users = map(str, interface.get_all_users())
    message = ' '.join(users)
    return (message, 200)


@user_blueprint.route('/user', methods=['POST'])
def user_create():
    payload = request.get_json()
    user_name = payload.get('name')
    if not user_name:
        return ('Error: No user name specified.', 400)
    user = interface.create_user(user_name)
    if not user:
        return ('Error: Duplicate user name.', 400)
    return (str(user), 200)


@user_blueprint.route('/user/<user_name>', methods=['GET'])
def user_get(user_name):
    user = interface.get_user(user_name)
    if not user:
        return ('Error: No user by the name ' + user_name, 404)
    return (str(user), 200)
