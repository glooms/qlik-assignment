from service import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def to_dict(self):
        d = {
            'id': self.id,
            'name': self.name
        }
        return d
