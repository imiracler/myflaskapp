from flask import Blueprint, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app.models.user import User
from app.models import db
from ..forms.auth import RegisterForm, LoginForm

user = Blueprint("user", __name__)


@user.route("/user", methods= ["GET"])
def create_user():
    return "create an user"


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        user.set_attrs(form.data)
        db.session.add(user)
        db.session.commit()

        login_user(user, False)
        return "registe success", 201
    return "false", 402


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter(User.email==form.email.data).first()
        if user and user.check_passsword(form.password.data):
            login_user(user, remember=True)
            return jsonify(token=user.generate_token())
        else:
            return 'error password or account not exists', 401


@user.route("/logout", methods=['GET', 'POST'])
#@login_required
def logout():
    logout_user()
    return "logout success", 203