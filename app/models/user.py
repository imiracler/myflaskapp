from sqlalchemy import Column, Integer, String, SmallInteger, Boolean
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.base import Base, db
from app.app import login_manager
from flask import current_app

class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(24), unique=True)
    auth = Column(SmallInteger, default=1)
    confirmed = Column(Boolean, default=False)
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

    def generate_token(self, expiration=6000):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))

@login_manager.unauthorized_handler
def unauthorized():     #自定义返回一个还没有登录认证结果
    return "unauthorized", 401

@login_manager.request_loader
def load_user_from_request(request):
    token = request.headers.get('token')
    # import pdb
    # pdb.set_trace()
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token.encode('utf-8'))  #loads方法里面包含了对时间是否过期的验证
    except:
        return False
    user = db.session.query(User).filter(User.id == data["id"]).first()
    user.confirmed = True
    db.session.add(user)

    return user if user else None
