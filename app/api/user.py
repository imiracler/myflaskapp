from flask import Blueprint

user = Blueprint("user", __name__)

@user.route("/user")
def create_user():
    return "create an user"