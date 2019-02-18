import unittest
import requests
from service import db
from service.models import init_db, drop_db


class BlueprintTests(unittest.TestCase):
    base_url = "http://127.0.0.1:5000"
    
    def setUp(self):
        try:
            init_db()
        except:
            db.session.rollback()
            drop_db()
        init_db()

    def tearDown(self):
        db.session.rollback()
        drop_db()

    def get(self, path):
        url = '/'.join([self.base_url] + path)
        return requests.get(url)
    
    def post(self, path, payload):
        url = '/'.join([self.base_url] + path)
        return requests.post(url, json=payload)

    def delete(self, path):
        url = '/'.join([self.base_url] + path)
        return requests.delete(url)

    def create_users(self, names):
        path = ['user']
        rvs = []
        for name in names:
            payload = {'name': name}
            rvs += [self.post(path, payload)]
            self.assertEqual(rvs[-1].status_code, 200, rvs[-1].text)
        return rvs

    def post_message(self, sender, recipient, body):
        path = ['user', sender, 'message']
        payload = {'name': recipient, 'message': body}
        return self.post(path, payload)

    def test_post_message(self):
        names = ['Emilia', 'Janne']
        body = 'Hello'
        self.create_users(names)
        r = self.post_message(*names, body)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data['sent']['body'], body)

    def test_get_received(self):
        names = ['Emilia', 'Janne']
        self.create_users(names)
        for i in range(1, 6):
            self.post_message(*names, 'Hello number %d' % i)
        path = ['user', names[1], 'message']
        r = self.get(path)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(len(data['received']), 5)
        path[1] = names[0]
        r = self.get(path)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertFalse(data['received'])

    def test_get_message(self):
        names = ['Emilia', 'Janne']
        self.create_users(names)
        self.post_message(*names, 'Hello')
        path = ['user', names[0], 'message', '1']
        r = self.get(path)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertFalse(data['received']['is_palindrome'])
    
    def test_del_message(self):
        names = ['Emilia', 'Janne']
        self.create_users(names)
        self.post_message(*names, 'Hello')
        path = ['user', names[0], 'message', '1']
        r = self.delete(path)
        self.assertEqual(r.status_code, 200)
