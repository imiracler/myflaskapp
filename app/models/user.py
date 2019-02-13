from sqlalchemy import Column, Integer, String, SmallInteger
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.base import Base, db
from app.app import login_manager
from flask import current_app

class User(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(24), unique=True)
    auth = Column(SmallInteger, default=1)
    _password = Column('password', String(100))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_email(nickname, account, secret):
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.email = account
            user.password = secret
            db.session.add(user)

    def check_passsword(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('id') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_token(self, expiration=6000):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))