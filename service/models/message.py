from service import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(250), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_palindrome = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        d = {
            'id': self.id,
            'body': self.body,
            'sender_id': self.sender_id,
            'recipient_id': self.recipient_id,
            'is_palindrome':  self.is_palindrome 
        }
        return d
