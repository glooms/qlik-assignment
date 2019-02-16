import requests

base_url = "http://127.0.0.1:5000"

def create_user(name):
    payload = {'name': name}
    path = 'user'
    url = base_url + '/' + path
    r = requests.post(url, json=payload)
    return r


def list_users():
    path = 'user'
    url = base_url + '/' + path
    r = requests.get(url)
    return r


def send(sender, receiver, msg):
    path = [base_url, 'user', sender, 'message']
    url = '/'.join(path)
    payload = {'name': receiver, 'message': msg}
    r = requests.post(url, json=payload)
    return r


def list_messages(name):
    path = [base_url, 'user', name, 'message']
    url = '/'.join(path)
    r = requests.get(url)
    return r


def get_message(name, msg_id):
    path = [base_url, 'user', name, 'message', str(msg_id)]
    url = '/'.join(path)
    r = requests.get(url)
    return r


def del_message(name, msg_id):
    path = [base_url, 'user', name, 'message', str(msg_id)]
    url = '/'.join(path)
    r = requests.delete(url)
    return r


def test(f, args, exp):
    r = f(*args)
    if 'code' in exp:
        assert r.status_code == exp['code'], r.status_code
    if 'text' in exp:
        for s in exp['text']:
            assert s in r.text, r.text
    if 'not-text' in exp:
        for s in exp['not-text']:
            assert not s in r.text, r.text


if __name__ == '__main__':
    sender = 'Alice'
    receiver = 'Bob'
    test(create_user, [sender], {'code': 200})
    test(create_user, [sender], {'code': 400})
    test(create_user, [receiver], {'code': 200})
    test(list_users, [], {'code': 200, 'text': [sender, receiver]})
    message = 'Hi Bob!'
    test(send, [sender, receiver, message], {'code': 200})
    test(list_messages, [receiver], {'code': 200, 'text': [message]})
    test(get_message, [receiver, 0], {'code': 200, 'text': [message]})
    test(del_message, [receiver, 0], {'code': 200})
    test(list_messages, [receiver], {'code': 200, 'not-text': [message]})
    test(get_message, [receiver, 0], {'code': 404})
    test(del_message, [receiver, 0], {'code': 404})
    test(get_message, [receiver, 's'], {'code': 400})
