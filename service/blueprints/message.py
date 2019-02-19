from flask import Blueprint, request, jsonify
from service.models import interface

message_blueprint = Blueprint('message', __name__)

@message_blueprint.route('/user/<user_name>/message', methods=['GET'])
def user_get_received(user_name):
    user = interface.get_user(user_name)
    if not user:
        data = {
            'error': 'No user by the name %s' % user_name
        }
        return (jsonify(data), 404)
    messages = interface.get_received_by(user)
    data = {
        'received': [msg.to_dict() for msg in messages]
    }
    return (jsonify(data), 200)


@message_blueprint.route('/user/<user_name>/message', methods=['POST'])
def user_post_message(user_name):
    sender = interface.get_user(user_name)
    if not sender:
        data = {
            'error': 'No user by the name %s' % user_name
        }
        return (jsonify(data), 404)
    payload = request.get_json()
    to = payload.get('name')
    recipient = interface.get_user(to)
    if not recipient:
        data = {
            'error': 'No user by the name %s' % to
        }
        return (jsonify(data), 404)
    body = payload.get('message')
    message = interface.send_message(sender, recipient, body)
    if not message:
        data = {
            'error': 'Message not created.'
        }
        return (jsonify(data), 500)
    data = {
        'sent': message.to_dict()
    }
    return (jsonify(data), 200)


@message_blueprint.route('/user/<user_name>/message/<message_id>', methods=['GET'])
def user_get_message_by_id(user_name, message_id):
    user = interface.get_user(user_name)
    if not user:
        data = {
            'error': 'No user by the name %s' % user_name
        }
        return (jsonify(data), 404)
    try:
        message_id = int(message_id)
    except:
        data = {
            'error': 'Invalid message id %s.' % message_id
        }
        return (jsonify(data), 400)
    message = interface.get_message_by_user_and_id(user, message_id)
    if not message:
        data = {
            'error': 'No message found with id %s.' % message_id
        }
        return (jsonify(data), 404)
    data = {
        'message': message.to_dict()
    }
    return (jsonify(data), 200)


@message_blueprint.route('/user/<user_name>/message/<message_id>', methods=['DELETE'])
def user_del_message_by_id(user_name, message_id):
    user = interface.get_user(user_name)
    if not user:
        data = {
            'error': 'No user by the name %s' % user_name
        }
        return (jsonify(data), 404)
    try:
        message_id = int(message_id)
    except:
        data = {
            'error': 'Invalid message id %s.' % message_id
        }
        return (jsonify(data), 400)
    message = interface.get_message_by_user_and_id(user, message_id)
    if not message:
        data = {
            'error': 'No message found with id %s.' % message_id
        }
        return (jsonify(data), 404)
    rv = interface.del_message_by_user_and_id(message)
    if not rv:
        data = {
            'error': 'Message %s not deleted.' % message_id
        }
        return (jsonify(data), 500)
    data = {
        'response': 'Message %s deleted.' % message_id
    }
    return (jsonify(data), 200)


@message_blueprint.route('/user/<user_name>/message/sent', methods=['GET'])
def user_get_sent_messages(user_name):
    user = interface.get_user(user_name)
    if not user:
        data = {
            'error': 'No user by the name %s' % user_name
        }
        return (jsonify(data), 404)
    messages = interface.get_sent_by(user)
    data = {
        'sent': [msg.to_dict() for msg in messages]
    }
    return (jsonify(data), 200)
