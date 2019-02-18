from service import db
from service.models.user import User
from service.models.message import Message


def init_db():
    db.create_all()
    db.session.commit()


def drop_db():
    db.drop_all()
    db.session.commit()
