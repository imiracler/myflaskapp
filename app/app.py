from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()

def reg_bp(app):
    from app.api.book import book
    from app.api.user import user
    from app.api.client import client
    app.register_blueprint(book)
    app.register_blueprint(user)
    app.register_blueprint(client)


def register_plugin(app):
    from app.models.base import db
    db.init_app(app)
    with app.app_context():
         db.create_all()  #要在app上下文中才能创建db


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.secure')
    app.config.from_object('app.config.setting')

    # 注册sqlalchemy
    register_plugin(app)

    # 注册login模块
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'

    # 注册蓝图
    reg_bp(app)

    return app

