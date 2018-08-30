from wtforms import Form, StringField, IntegerField
from wtforms.validators import DataRequired, length

from app.libs.enums import ClientTypeEnum


class ClientForm(Form):  #可以接收客户端穿过来的参数
    account = StringField(validators=[DataRequired(), length(min=5, max=32)])
    secret = StringField()
    type = IntegerField()

    def validate_type(self, value):  #这个是自定义的一个验证器
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e