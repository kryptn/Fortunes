from random import choice

from flask_sqlalchemy import SQLAlchemy

from fortunate import utils
from fortunate.exceptions import ApiException

db = SQLAlchemy()

class SqlFortune(utils.Fortune):
    def commit(self, model):
        db.session.add(model)
        db.session.commit()
        return model

    def return_or_raise(self, result, message):
        if result:
            return result
        raise ApiException(message)

    def get_user(self, ip):
        result = User.query.filter_by(ip=ip).first()
        if result:
            return result
        raise ApiException('IP Not Found')

    def create_user(self, ip):
        return self.commit(User(ip))

    def get_key(self, token):
        result = Key.query.filter_by(token=token).first()
        if result:
            return result
        raise ApiException('Invalid Token')

    def create_key(self, user):
        return self.commit(Key(user, self.new_token()))

    def random_fortune(self, token):
        result = Fortune.query.filter(Fortune.key.has(token=token))\
                        .order_by(db.func.random()).limit(1).first()
        if result:
            return result
        raise ApiException('Invalid Token or No Fortunes On Token')

    def add_fortune(self, token, text):
        result = Key.query.filter_by(token=token).first()
        if result:
            return self.commit(Fortune(result, text))
        raise ApiException('Invalid Token')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15))

    def __init__(self, ip):
        self.ip = ip


class Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(16), unique=True)
    private = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('keys', lazy='joined'))

    def __init__(self, user, token):
        self.user = user
        self.token = token

class Fortune(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    pulls = db.Column(db.Integer)

    key_id = db.Column(db.Integer, db.ForeignKey('key.id'))
    key = db.relationship('Key', backref=db.backref('fortunes', lazy='joined'))

    def __init__(self, key, text):
        self.text = text
        self.key = key