import re

from service.models.user import User
from service.models.message import Message
from service import db


def try_commit():
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return False
    return True


def get_all_users():
    return User.query.all()


def create_user(name):
    user = User(name=name)
    db.session.add(user)
    if try_commit():
        return user
    return None


def get_user(name):
    query = User.query.filter_by(name=name)
    return query.first()


def get_sent_by(user):
    query = Message.query.filter_by(sender_id=user.id)
    return query.all()


def get_received_by(user):
    query = Message.query.filter_by(recipient_id=user.id)
    return query.all()


def get_messages_for(user):
    return get_sent_by(user).all() + get_received_by(user).all()


def send_message(sender, recipient, text):
    data = {
        'body': text,
        'sender_id': sender.id,
        'recipient_id': recipient.id,
        'is_palindrome': is_palindrome(text)
    }
    message = Message(**data)
    db.session.add(message)
    if try_commit():
        return message
    return None


def get_all_messages():
    return Message.query.all()


def get_message_by_id(msg_id):
    message = Message.query.get(msg_id)
    return message


def get_message_by_user_and_id(user, msg_id):
    query = Message.query.filter_by(sender_id=user.id, id=msg_id)
    message = query.first()
    if not message:
        query = Message.query.filter_by(recipient_id=user.id, id=msg_id)
        message = query.first()
    return message


def del_message_by_user_and_id(user, msg_id):
    message = get_message_by_user_and_id(user, msg_id) 
    db.session.delete(message)
    return try_commit()


def is_palindrome(text):
    regex = re.compile('[^a-z]')
    string = regex.sub('', text.lower())
    l = int(len(string) / 2)
    for i in range(l):
        if string[i] != string[-i -1]:
            return False
    return True
    
