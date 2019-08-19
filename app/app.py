from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()

def reg_bp(app):
    from app.api.music import music
    from app.api.user import user
    from app.api.client import client
    app.register_blueprint(music)
    app.register_blueprint(user)
    app.register_blueprint(client)

def after_request(resp):
    resp.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,session_id')
    resp.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def register_plugin(app):
    from app.models.base import db
    db.init_app(app)
    with app.app_context():
         db.create_all()


def create_app():
    app = Flask(__name__,template_folder="templates",static_folder="static",static_url_path="/app/static")
    app.config.from_object('app.config.secure')
    app.config.from_object('app.config.setting')
    app.after_request(after_request)

    register_plugin(app)


    login_manager.login_view = 'user.login'
    login_manager.login_message = 'please sign in'
    login_manager.init_app(app)


    reg_bp(app)

    return app

