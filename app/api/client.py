from flask import Blueprint, request

from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.forms import ClientForm

client = Blueprint("client", __name__)

@client.route("/register", methods=["post"])
def create_client():
    data = request.json
    form = ClientForm(data=data)   #json格式的数据需要以 data=data的方式 作为参数传进来
    if form.validate():
        promise = {
            ClientTypeEnum.USER_EMAIL: __register_user_by_email

        }
    return 1

def __register_user_by_email(form):
     User.register_by_email(form.account.data)