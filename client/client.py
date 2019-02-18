import requests
import json

class Client(object):
    base_url = 'https://qlik-assignment.appspot.com'

    def __init__(self, local=False):
        if local:
            self.base_url = 'http://127.0.0.1:5000'

    def print_response(self, r):
        print(json.dumps(r.json(), indent=4))

    def get(self, path):
        url = '/'.join([self.base_url] + path)
        print('GET: %s' % url)
        r = requests.get(url)
        self.print_response(r)
        return r 
    
    def post(self, path, payload):
        url = '/'.join([self.base_url] + path)
        print('POST: %s' % url)
        r = requests.post(url, json=payload)
        self.print_response(r)
        return r 

    def delete(self, path):
        url = '/'.join([self.base_url] + path)
        print('DELETE: %s' % url)
        r = requests.delete(url)
        self.print_response(r)
        return r

    def help(self):
        print('Available methods:\n')
        exclude = ['base_url', 'print_response', 'get', 'post', 'delete']
        methods = []
        for attr in dir(self):
            if not attr in exclude and not '__' in attr:
                methods += [attr]
        print(', '.join(methods))
        print('\nUsers are identified by their names and have sent and received messages.')
        print('Messages are spceified by their ids and have senders and recipients.')
        print('Example: Sending a message with \'post_message\' ' +
                'requires a sending and a receiving user as well as ' +
                'the actual text message, in that order.')

    def get_users(self):
        path = ['user']
        return self.get(path)

    def get_user(self, name):
        path = ['user', name]
        return self.get(path)

    def create_user(self, name):
        path = ['user']
        payload = {'name': name}
        return self.post(path, payload)

    def post_message(self, from_name, to_name, body):
        path = ['user', from_name, 'message']
        payload = {'name': to_name, 'message': body}
        return self.post(path, payload)

    def get_received(self, name):
        path = ['user', name, 'message']
        return self.get(path)

    def get_sent(self, name):
        path = ['user', name, 'message', 'sent']
        return self.get(path)

    def get_message(self, name, msg_id):
        msg_id = str(msg_id)
        path = ['user', name, 'message', msg_id]
        return self.get(path)
    
    def del_message(self, name, msg_id):
        msg_id = str(msg_id)
        path = ['user', name, 'message', msg_id]
        return self.delete(path)
