from flask import Blueprint, request
#from flask_login import login_user, login_required, logout_user, current_user
from app.models.user import User
from app.models import db
from ..forms.auth import RegisterForm

user = Blueprint("user", __name__)


@user.route("/user", methods= ["GET"])
def create_user():
    return "create an user"


@user.route('/user/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    import pdb
    pdb.set_trace()
    if request.method == 'POST' and form.validate():
        user = User()
        user.set_attrs(form.data)
        db.session.add(user)
        db.session.commit()

        return "registe success", 201
    return "false"
