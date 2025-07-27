from wtforms import StringField,ValidationError,IntegerField,BooleanField
from wtforms.validators import Email,EqualTo,Length,InputRequired
from exts import cache
from models.user import UserModel
from .baseform import BaseForm

class AddStaffForm(BaseForm):
        email = StringField(validators=[Email(message="请输入正确的邮箱格式!")])
        role = IntegerField(validators=[InputRequired(message="请选择角色")])

class EditStaffForm(BaseForm):
        is_staff = BooleanField(validators=[InputRequired(message="请选择是否为员工")])
        role = IntegerField(validators=[InputRequired(message="请选择角色")])


