import unittest
from service import db
from service.models import init_db, drop_db, User, Message
from sqlalchemy.exc import IntegrityError


class DatabaseTests(unittest.TestCase):
    
    def setUp(self):
        db.session.rollback()
        drop_db()
        init_db()

    def add_users(self, names):
        for name in names:
            db.session.add(User(name=name))

    def send_message(self, body, sender_id, recipient_id):
        data = {
            'body': body,
            'sender_id': sender_id,
            'recipient_id': recipient_id
        }
        m = Message(**data)
        db.session.add(m)
        
    def test_initial_state(self):
        self.assertFalse(User.query.all())
        self.assertFalse(Message.query.all())

    def test_add_user(self):
        names = ['Lars']
        self.add_users(names)
        db.session.commit()
        self.assertEqual(names[0], User.query.get(1).name)

    def test_add_users(self):
        names = ['Frida', 'Rosa', 'Maria']
        self.add_users(names)
        db.session.commit()
        for i, name in enumerate(names):
            self.assertEqual(name, User.query.get(i + 1).name)

    def test_add_same_user(self):
        names = ['Lars', 'Lars']
        self.add_users(names)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_send_message(self):
        names = ['Sofia', 'Lisa']
        self.add_users(names)
        self.send_message('Hejsan', 1, 2)
        db.session.commit()
        self.assertTrue(Message.query.get(1))

    def test_message_sent_received(self):
        names = ['Sofia', 'Lisa']
        self.add_users(names)
        self.send_message('Hejsan', 1, 2)
        self.send_message('Hejsan igen!', 1, 2)
        db.session.commit()
        sender = User.query.filter_by(name=names[0]).first()
        recipient = User.query.filter_by(name=names[1]).first()
        self.assertEqual(len(Message.query.filter_by(sender_id=sender.id).all()), 2)
        self.assertEqual(len(Message.query.filter_by(recipient_id=recipient.id).all()), 2)
