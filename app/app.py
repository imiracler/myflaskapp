from flask import Flask


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
    register_plugin(app)
    reg_bp(app)
    return app

