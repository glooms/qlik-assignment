from flask import Flask, request

app = Flask(__name__)

users = {}

@app.route('/clear')
def clear():
    users = {}
    return 'Users cleared.'

@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/user', methods=['GET'])
def user_get():
    message = ''
    if users: # If there are any users
        message = 'All users: ' + ' '.join(users)
    else:
        message = 'No users are yet created.'
    return (message, 200)


@app.route('/user', methods=['POST'])
def user_create():
    payload = request.get_json()
    user_name = payload.get('name')
    if not user_name:
        return ('Error: No user name specified.', 400)
    if user_name in users:
        return ('Error: Duplicate user name.', 400)
    users[user_name] = []
    return ('User ' + user_name + ' created.', 200)


@app.route('/user/<user_name>/message', methods=['GET'])
def user_get_message(user_name):
    if not user_name in users:
        return ('Error: No user by the name ' + user_name, 404)
    message = ''
    for i, msg in enumerate(users[user_name]):
        message += '%d: %s\n' % (i, msg)
    return (message, 200)


@app.route('/user/<user_name>/message', methods=['POST'])
def user_post_message(user_name):
    if not user_name in users:
        return ('Error: No user by the name ' + user_name, 404)
    payload = request.get_json()
    to = payload.get('name')
    if not to in users:
        return ('Error: No user by the name ' + user_name, 404)
    message = payload.get('message')
    users[to] += [message]
    return ('Message sent.', 200)


@app.route('/user/<user_name>/message/<message_id>', methods=['GET', 'DELETE'])
def user_get_message_by_id(user_name, message_id):
    if not user_name in users:
        return ('Error: No user by the name ' + user_name, 404)
    messages = users[user_name]
    try:
        message_id = int(message_id)
    except:
        return ('Invalid message id %d.', 400)
    if message_id >= len(messages):
        return ('Error: No message by the id %d' % message_id, 404)
    if request.method == 'DELETE':
        del messages[message_id]
        return ('Message %d deleted' % message_id, 200)
    return (messages[message_id], 200)

